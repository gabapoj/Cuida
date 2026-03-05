# app/emails — Phase 2

Transactional email via AWS SES with React Email templates.

## Files to create

```
app/emails/
├── client.py        # SES boto3 client, provide_email_client() dependency
├── service.py       # send_magic_link(), send_call_summary()
└── templates/       # Jinja2 HTML (compiled from React Email in emails/ dir)
```

## Stack

- **AWS SES** for delivery
- **React Email** (`backend/emails/`) for template authoring
- **Jinja2** for server-side rendering (React Email compiles to HTML with Tailwind inlined)

## Flow

1. Author templates in `backend/emails/` using React Email + Tailwind v4
2. Run `just build-emails` → compiles to `backend/app/emails/templates/`
3. Jinja2 renders the compiled HTML with dynamic variables at send time
4. SES sends via boto3

## Sending an email

```python
from app.emails.service import send_magic_link

await send_magic_link(to_email="user@example.com", magic_link="https://...")
```

## Config (Phase 2 env vars)

```
AWS_REGION=us-east-1
SES_FROM_EMAIL=noreply@cuida.app
SES_FROM_NAME=Cuida
```
