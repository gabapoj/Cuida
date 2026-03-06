import { createRoute } from "@tanstack/react-router"
import { publicLayoutRoute } from "@/router/layout.routes"
import { AuthPage } from "@/pages/auth/auth-page"
import { MagicLinkVerifyPage } from "@/pages/auth/magic-link-verify-page"

export const authRoute = createRoute({
  getParentRoute: () => publicLayoutRoute,
  path: "/auth",
  component: AuthPage,
})

export const magicLinkVerifyRoute = createRoute({
  getParentRoute: () => publicLayoutRoute,
  path: "/auth/magic-link/verify",
  validateSearch: (search: Record<string, unknown>) => ({
    token: String(search["token"] ?? ""),
  }),
  component: MagicLinkVerifyPage,
})
