import { createRoute, redirect } from "@tanstack/react-router"
import { rootRoute } from "@/router/root.route"
import { publicLayoutRoute } from "@/router/layout.routes"
import { queryClient } from "@/lib/query-client"
import { getAuthMeMeQueryOptions } from "@/openapi/auth/auth"
import { AuthPage } from "@/pages/auth/auth-page"
import { MagicLinkVerifyPage } from "@/pages/auth/magic-link-verify-page"

export const homeRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  loader: async () => {
    try {
      await queryClient.ensureQueryData(getAuthMeMeQueryOptions())
      throw redirect({ to: "/dashboard", replace: true })
    } catch (err) {
      if (err instanceof Error && "to" in (err as object)) throw err
      throw redirect({ to: "/auth", replace: true })
    }
  },
})

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
