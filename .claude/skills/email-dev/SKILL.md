
---
name: email-dev
description: Email template development with React Email. Use when creating or modifying email templates, testing email rendering, or building email HTML from React components.
---

# Email Template Development

## Commands

```bash
just dev-emails    # Start React Email dev server (http://localhost:3001)
just build-emails  # Compile React Email → Jinja2 templates
```

## Structure

```
backend/emails/
├── templates/                  # React Email source (.tsx)
│   ├── components.tsx          # Shared components (excluded from build)
│   ├── MagicLink.tsx
│   └── SignupConfirmation.tsx
├── scripts/
│   └── build.ts                # Build script (auto-generates Jinja2 vars from TS props)
└── package.json

backend/templates/emails-react/ # Compiled output (generated, committed)
├── magic_link/
│   ├── html.jinja2
│   └── text.jinja2
└── signup_confirmation/
    ├── html.jinja2
    └── text.jinja2
```

## Development Workflow

### 1. Start dev server

```bash
just dev-emails
```

Live preview at http://localhost:3001 with auto-reload.

### 2. Create or edit a template

Templates live in `backend/emails/templates/`. Files starting with `_` or named `components.tsx` are excluded from the build.

```tsx
import { Button, Html, Text, Section, Container } from '@react-email/components';

interface WelcomeEmailProps {
  userName: string;
  loginUrl: string;
}

export const WelcomeEmail = ({ userName, loginUrl }: WelcomeEmailProps) => (
  <Html>
    <Container>
      <Section>
        <Text>Hello {userName}!</Text>
        <Button href={loginUrl}>Log In</Button>
      </Section>
    </Container>
  </Html>
);

WelcomeEmail.PreviewProps = {
  userName: 'Jane Smith',
  loginUrl: 'https://app.cuida.com/login',
} as WelcomeEmailProps;

export default WelcomeEmail;
```

### 3. Build templates

```bash
just build-emails
```

The build script:
- Auto-discovers all `.tsx` files in `templates/` (excluding `_*` and `components.tsx`)
- Extracts prop names from the TypeScript `*Props` interface
- Converts each prop to a Jinja2 variable: `userName` → `{{ userName }}`
- Outputs `html.jinja2` + `text.jinja2` to `backend/templates/emails-react/<snake_case_name>/`
- PascalCase → snake_case: `WelcomeEmail` → `welcome_email/`

No TEMPLATE_VARIABLES registry needed — Jinja2 vars are derived automatically from TypeScript props.

### 4. Add a send method to EmailService

`backend/app/emails/service.py`:

```python
async def send_welcome_email(
    self,
    to_email: str,
    user_name: str,
    login_url: str,
) -> None:
    await self._send_email(
        template_name="welcome_email",
        to_email=to_email,
        subject="Welcome to Cuida!",
        template_vars={
            "userName": user_name,
            "loginUrl": login_url,
        },
    )
```

Call from a route handler by injecting `EmailService` as a dependency (registered in `factory.py`).

## Production

Before deploying:
1. Run `just build-emails` to compile templates
2. The compiled output in `backend/templates/emails-react/` is checked into git and baked into the Docker image — no Node.js needed at runtime
