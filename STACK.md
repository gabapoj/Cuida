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

## Frontend — Landing (`landing/`)

| Concern | Choice |
|---|---|
| Framework | **Next.js** |
| Styling | **Tailwind v4** |
| Deployment | **Vercel** |

## Frontend — web (`web/`)

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
| Database | **Aurora Serverless v2** (PostgreSQL-compatible, scale-to-zero) |
| Cache / queue | **ElastiCache Redis** |
| Audio / transcript storage | **S3** |
| IaC | **Terraform** |
| CI/CD | **GitHub Actions** |
| Task runner | **Justfile** |

## Provider Abstraction

All AI and telephony integrations use the **adapter pattern** — each category defines a
`typing.Protocol` interface with concrete provider implementations behind a factory.
Switching providers is a config/env change, not a code change.

## Project Layout

```
Cuida/
├── backend/
│   ├── app/
│   │   ├── factory.py
│   │   ├── index.py
│   │   ├── base/              # BaseDBModel, mixins
│   │   ├── auth/              # magic link routes + models
│   │   ├── users/             # models, routes, schemas
│   │   ├── calls/             # call sessions, websocket handlers
│   │   ├── llm/               # LLM providers (OpenAI, Anthropic)
│   │   ├── voice/             # STT (Deepgram) + TTS (ElevenLabs)
│   │   ├── telephony/         # Telnyx + Twilio
│   │   ├── emails/            # SES client + Jinja2 compiled templates
│   │   ├── queue/             # SAQ workers
│   │   └── utils/             # config, logging
│   ├── alembic/
│   ├── emails/                # React Email source (.tsx) + build scripts
│   ├── tests/
│   ├── pyproject.toml         # uv
│   ├── Dockerfile
│   └── docker-compose.dev.yml
├── landing/                   # Next.js marketing site
│   ├── app/
│   ├── components/
│   └── package.json           # pnpm
├── web/                       # Vite React webapp
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── openapi/           # Orval-generated
│   │   ├── hooks/
│   │   └── router/
│   ├── vite.config.ts
│   └── package.json           # pnpm
├── infra/
│   └── main.tf
├── .github/workflows/
└── Justfile
```
