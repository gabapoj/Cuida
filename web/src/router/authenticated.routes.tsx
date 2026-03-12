import { createRoute } from "@tanstack/react-router"
import { authenticatedLayoutRoute } from "@/router/layout.routes"
import { DashboardPage } from "@/pages/dashboard/dashboard-page"
import { ClientsPage } from "@/pages/clients/clients-page"
import { CallsPage } from "@/pages/calls/calls-page"
import { SettingsPage } from "@/pages/settings/settings-page"

export const indexRoute = createRoute({
  getParentRoute: () => authenticatedLayoutRoute,
  path: "/",
  component: DashboardPage,
})

export const clientsRoute = createRoute({
  getParentRoute: () => authenticatedLayoutRoute,
  path: "/clients",
  component: ClientsPage,
})

export const callsRoute = createRoute({
  getParentRoute: () => authenticatedLayoutRoute,
  path: "/calls",
  component: CallsPage,
})

export const settingsRoute = createRoute({
  getParentRoute: () => authenticatedLayoutRoute,
  path: "/settings",
  component: SettingsPage,
})
