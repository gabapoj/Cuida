import { useAuthMeMeSuspense } from "@/openapi/auth/auth"
import { PageTopBar } from "@/components/page-topbar"

export function DashboardPage() {
  const { data } = useAuthMeMeSuspense()
  const user = data.data as { email?: string; name?: string }

  return (
    <PageTopBar title="Dashboard">
      <div className="p-6">
        <p className="text-muted-foreground">Welcome, {user.email}</p>
      </div>
    </PageTopBar>
  )
}
