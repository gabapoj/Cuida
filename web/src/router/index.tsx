import { createRouter } from "@tanstack/react-router"
import { rootRoute } from "@/router/root.route"
import { publicLayoutRoute, authenticatedLayoutRoute } from "@/router/layout.routes"
import { homeRoute, authRoute, magicLinkVerifyRoute } from "@/router/public.routes"
import { dashboardRoute } from "@/router/authenticated.routes"

const routeTree = rootRoute.addChildren([
  homeRoute,
  publicLayoutRoute.addChildren([authRoute, magicLinkVerifyRoute]),
  authenticatedLayoutRoute.addChildren([dashboardRoute]),
])

export const router = createRouter({ routeTree })

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router
  }
}
