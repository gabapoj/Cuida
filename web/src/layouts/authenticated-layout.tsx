import { Outlet } from "@tanstack/react-router"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { authenticatedLayoutRoute } from "@/router/layout.routes"

export function AuthenticatedLayout() {
  const { user } = authenticatedLayoutRoute.useLoaderData()
  const userData = user.data as { email?: string; name?: string }

  return (
    <SidebarProvider defaultOpen={true}>
      <AppSidebar user={userData} />
      <SidebarInset>
        <main className="flex flex-1 flex-col">
          <Outlet />
        </main>
      </SidebarInset>
    </SidebarProvider>
  )
}
