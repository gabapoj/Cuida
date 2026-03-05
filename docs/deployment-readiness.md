# Deployment Readiness

The Terraform and CI/CD pipeline are well-written and cover the full stack, but
several things need manual setup before the first push to `main` will succeed.

---

## What's in place

- VPC, subnets, security groups, IAM
- ECS Fargate — API service + worker service
- Aurora Serverless v2 (PostgreSQL 17, scale-to-zero)
- ElastiCache Redis 7
- ALB + ACM certificate + Route53
- Secrets Manager
- S3 (audio recordings + transcripts)
- Vercel projects (landing + web app)
- GitHub Actions pipeline: detect changes → test → build image → terraform apply → ECS deploy

---

## Blockers before first deploy

### 1. AWS bootstrap resources (manual, one-time)

The pipeline assumes two resources exist in AWS before it ever runs. Neither is
created by Terraform — they need to be set up manually first.

**S3 state bucket**

Terraform stores its state in S3. The bucket is named `tf-state-cuida`.
Create it before running any `terraform init`:

```bash
aws s3api create-bucket \
  --bucket tf-state-cuida \
  --region us-east-1
aws s3api put-bucket-versioning \
  --bucket tf-state-cuida \
  --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption \
  --bucket tf-state-cuida \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

**GitHub Actions OIDC role**

The workflows authenticate to AWS via OIDC (no long-lived keys). The IAM
provider and role must exist before CI runs. Create them once:

```bash
# 1. Create the OIDC identity provider
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1

# 2. Create the IAM role (replace owner/repo)
# Trust policy — scope to your repo only
cat > /tmp/trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/token.actions.githubusercontent.com"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringLike": {
        "token.actions.githubusercontent.com:sub": "repo:gabapoj/Cuida:*"
      },
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
      }
    }
  }]
}
EOF

aws iam create-role \
  --role-name cuida-github-actions \
  --assume-role-policy-document file:///tmp/trust-policy.json

# 3. Attach permissions (AdministratorAccess for initial setup — tighten later)
aws iam attach-role-policy \
  --role-name cuida-github-actions \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# 4. Note the role ARN — you'll need it for the GitHub secret
aws iam get-role --role-name cuida-github-actions --query Role.Arn --output text
```

---

### 2. DNS / ACM certificate deadlock

`terraform apply` creates the Route53 zone and immediately tries to validate
the ACM certificate via DNS. But you don't know the Route53 nameservers until
*after* the zone is created — so you can't point your domain registrar at them
first. The apply will hang for up to 45 minutes waiting for cert validation,
then time out.

**Fix — two-phase first apply:**

```bash
# Phase A: apply everything except the cert validation
cd infra
terraform apply -target=aws_route53_zone.main

# Get the nameservers
terraform output route53_nameservers

# → Go to your domain registrar and point the domain at those nameservers.
# → Wait for DNS propagation (minutes to hours depending on registrar).

# Phase B: apply the rest
terraform apply
```

After the first deploy this is no longer an issue — subsequent applies run
through without any manual steps.

---

### 3. GitHub repository secrets

Set these in **GitHub → repo → Settings → Secrets and variables → Actions**
before pushing to `main`:

| Secret | Where to get it |
|---|---|
| `OIDC_ROLE_ARN` | Output of the OIDC role setup above |
| `VERCEL_API_TOKEN` | vercel.com → Account Settings → Tokens |
| `DB_PASSWORD` | Choose a strong password (replaces the `"postgres"` default) |

---

### 4. DB migrations not wired into CI/CD

There is no `alembic upgrade head` step in the deploy pipeline. This is fine
for Phase 1 (trivial schema), but will cause downtime in Phase 2 when real
migrations ship.

**Fix needed in `_deploy.yml`:** add an ECS `run-task` step that runs
`alembic upgrade head` against the production DB before the rolling ECS
service update. This can be deferred until just before Phase 2 ships.

---

## Post-first-deploy checklist

- [ ] Rotate `DB_PASSWORD` via Secrets Manager (the value used in Terraform
      becomes visible in state — change it immediately after first apply)
- [ ] Set real secret values in Secrets Manager for `SECRET_KEY`,
      `OPENAI_API_KEY`, etc. (they are initialised to `""` / `"replace-me"`)
- [ ] Verify `curl https://api.<domain>/health` returns `{"status":"ok","db":"ok"}`
- [ ] Confirm Vercel projects are connected and deploying from the correct
      branches

---

## Summary

| Item | Status |
|---|---|
| Terraform — infrastructure | Ready |
| CI/CD pipeline | Ready |
| S3 state bucket | Needs manual creation |
| GitHub Actions OIDC role | Needs manual creation |
| DNS two-phase apply | Needs awareness on first run |
| GitHub secrets | Needs configuration |
| DB migration step in CI | Deferred to Phase 2 |
