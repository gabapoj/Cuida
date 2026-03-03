# Cuida Stack

## Backend

| Concern | Choice |
|---|---|
| Framework | **Litestar** (ASGI) |
| Python | **3.13+** via **uv** |
| ORM | **SQLAlchemy 2.0** async |
| DB driver | **psycopg** (async) |
| Migrations | **Alembic** |
| Validation | **msgspec** (not Pydantic) |
| Auth | **Magic link** sessions |
| Email | **AWS SES** + **React Email** templates |
| Background jobs | **SAQ** + **Redis** |
| API docs | **Litestar OpenAPI** (built-in) |
| Real-time | **WebSockets** (Litestar built-in) |

## AI / Voice

| Concern | Choice |
|---|---|
| Foundation models | **OpenAI** + **Anthropic (Claude)** |
| Speech-to-text | **Deepgram** |
| Text-to-speech | **ElevenLabs** |
| Telephony | **Telnyx** + **Twilio** |
| Audio storage | **S3** (recordings + transcripts) |

## Frontend

| Concern | Choice |
|---|---|
| Framework | **React 19** + **Vite** |
| Routing | **TanStack Router** |
| Styling | **Tailwind v4** + **shadcn/ui** |
| Server state | **TanStack Query** |
| API client | **Orval** (generated from OpenAPI) |
| Deployment | **Vercel** |

## Infrastructure

| Concern | Choice |
|---|---|
| API containers | **ECS Fargate** |
| Container registry | **ECR** |
| Database | **RDS PostgreSQL 16** |
| Cache / queue | **ElastiCache Redis** |
| Audio / transcript storage | **S3** |
| IaC | **Terraform** |
| CI/CD | **GitHub Actions** |
| Task runner | **Justfile** |

## Project Layout

```
Cuida/
├── backend/
│   ├── app/
│   │   ├── factory.py
│   │   ├── index.py
│   │   ├── base/          # BaseDBModel, mixins
│   │   ├── auth/          # magic link routes + models
│   │   ├── users/         # models, routes, schemas
│   │   ├── calls/         # call sessions, websocket handlers
│   │   ├── voice/         # STT (Deepgram), TTS (ElevenLabs) clients
│   │   ├── llm/           # OpenAI + Anthropic clients, prompt management
│   │   ├── telephony/     # Telnyx + Twilio webhook handlers
│   │   ├── emails/        # React Email templates
│   │   ├── queue/         # SAQ workers
│   │   └── utils/         # config, logging
│   ├── alembic/
│   ├── tests/
│   ├── pyproject.toml     # uv
│   ├── Dockerfile
│   └── docker-compose.dev.yml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── openapi/       # Orval-generated
│   │   ├── hooks/
│   │   └── router/
│   ├── vite.config.ts
│   └── package.json       # pnpm
├── infra/
│   └── main.tf
├── .github/workflows/
└── Justfile
```
