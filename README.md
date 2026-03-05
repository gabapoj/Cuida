# Cuida

AI-powered care companion — voice-first, real-time support.

## Quick Start

```bash
# 0. Install Just
brew install just

# 1. Install backend deps
just install

# 2. Start postgres + redis
just db-start

# 3. Run migrations
just db-upgrade

# 4. Start API server
just dev-backend
# → http://localhost:8000
# → http://localhost:8000/schema  (OpenAPI)
```

## Dev Ports

| Service        | Port  |
|----------------|-------|
| Backend API    | 8000  |
| React App      | 5173  |
| Landing (Next) | 3000  |
| PostgreSQL dev | 5432  |
| PostgreSQL test| 5433  |
| Redis          | 6379  |

## Project Layout

```
Cuida/
├── backend/          # Litestar API (Python 3.13 + uv)
├── app/              # React 19 + Vite webapp
├── landing/          # Next.js marketing site
├── emails/           # React Email templates
├── infra/            # Terraform (ECS/RDS/Redis)
├── .github/          # CI/CD workflows
└── Justfile          # Task runner
```

## Release Phases

| Phase | Scope | Status |
|-------|-------|--------|
| 1 | Backend scaffold, `/health`, core config/DB | **Current** |
| 2 | Auth (magic link), Users, Calls, SAQ queue, Emails | Planned |
| 3 | AI/Voice adapters (LLM, STT, TTS, Telephony) | Planned |
| 4 | Infra (Terraform ECS/RDS/Redis), CI/CD | Planned |

## Stack

See [`STACK.md`](STACK.md) for full tech decisions.
