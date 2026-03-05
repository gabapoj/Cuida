# backend/emails — React Email Templates (Phase 2)

Transactional email templates authored with React Email and Tailwind v4.
Compiled HTML output is consumed by the backend's Jinja2 renderer via SES.

## Bootstrap (do this once in Phase 2)

```bash
cd backend/emails
npm init -y
npm install react react-dom react-email @react-email/components @react-email/tailwind
npm install -D tsx typescript tailwindcss @types/react @types/node
```

## Directory layout (after bootstrap)

```
backend/emails/
├── templates/             # React Email source (.tsx)
│   ├── MagicLink.tsx
│   └── CallSummary.tsx
├── scripts/
│   ├── build.ts           # Compiles → backend/app/emails/templates/ (Jinja2 HTML)
│   └── watch.ts           # Watches + rebuilds on change
├── package.json           # npm (not pnpm — react-email CLI works better with npm)
├── tailwind.config.ts
└── tsconfig.json
```

## Dev workflow

```bash
# Preview emails in browser (port 3001)
npm run dev

# Compile to Jinja2 HTML (run before deploying)
npm run build
```

Add to the root Justfile:

```just
dev-emails:
    cd backend/emails && npm run dev

build-emails:
    cd backend/emails && npm run build
```

## Integration

The `build.ts` script compiles React Email templates to plain HTML with Tailwind
styles inlined, then writes them to `backend/app/emails/templates/`. At send time,
the Python backend renders them with Jinja2 to inject dynamic variables (user name,
magic link URL, etc.) before dispatching via AWS SES.
