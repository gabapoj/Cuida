import { createRoute } from "@tanstack/react-router"
import { authenticatedLayoutRoute } from "@/router/layout.routes"
import { DashboardPage } from "@/pages/dashboard/dashboard-page"

export const dashboardRoute = createRoute({
  getParentRoute: () => authenticatedLayoutRoute,
  path: "/dashboard",
  component: DashboardPage,
})
