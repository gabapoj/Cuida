import { createRouter } from "@tanstack/react-router"
import { rootRoute } from "@/router/root.route"
import { publicLayoutRoute, authenticatedLayoutRoute } from "@/router/layout.routes"
import { authRoute, magicLinkVerifyRoute } from "@/router/public.routes"
import { indexRoute, clientsRoute, callsRoute, settingsRoute } from "@/router/authenticated.routes"

const routeTree = rootRoute.addChildren([
  publicLayoutRoute.addChildren([authRoute, magicLinkVerifyRoute]),
  authenticatedLayoutRoute.addChildren([indexRoute, clientsRoute, callsRoute, settingsRoute]),
])

export const router = createRouter({ routeTree })

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router
  }
}
