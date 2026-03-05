# app/auth — Phase 2

Magic link authentication. No passwords — users receive a one-time login link via email.

## Files to create

```
app/auth/
├── models.py        # MagicLinkToken model (token, user_id, expires_at, used_at)
├── routes.py        # POST /auth/magic-link/request, GET /auth/magic-link/verify
├── schemas.py       # Request/response msgspec structs
├── service.py       # Token generation, email dispatch, session creation
└── guards.py        # session_guard() — dependency for protected routes
```

## Flow

1. `POST /auth/magic-link/request` — user submits email, receive a token → SES sends link
2. `GET /auth/magic-link/verify?token=<token>` — validates token, creates server-side session
3. `POST /auth/logout` — clears session

## Key decisions

- Tokens: `secrets.token_urlsafe(32)`, hashed before storage (SHA-256)
- Expiry: 15 minutes, single-use
- Sessions: Litestar `ServerSideSessionConfig`, stored in Redis (Phase 2 adds Redis store)
- Auth guard: `provide_session_user` dependency — raises 401 if no session

## Dependencies

- `litestar.middleware.session.server_side.ServerSideSessionConfig`
- `litestar.security.session_auth.SessionAuth`
- `app.emails` (for sending the magic link)
- `app.users` (for looking up / creating users)
