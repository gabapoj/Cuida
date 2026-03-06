import { useNavigate } from "@tanstack/react-router"
import { useAuthMeMeSuspense, useAuthLogoutLogout } from "@/openapi/auth/auth"
import { Button } from "@/components/ui/button"

export function DashboardPage() {
  const { data } = useAuthMeMeSuspense()
  const navigate = useNavigate()

  const logout = useAuthLogoutLogout({
    mutation: {
      onSuccess: () => void navigate({ to: "/auth", replace: true }),
    },
  })

  const user = data.data as { email?: string; name?: string }

  return (
    <div className="flex min-h-svh flex-col items-center justify-center gap-4">
      <p className="text-foreground">Welcome, {user.email}</p>
      <Button variant="outline" onClick={() => logout.mutate()}>
        Sign out
      </Button>
    </div>
  )
}
