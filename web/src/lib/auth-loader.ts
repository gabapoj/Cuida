import { redirect } from "@tanstack/react-router"
import { queryClient } from "@/lib/query-client"
import { getAuthMeMeQueryOptions } from "@/openapi/auth/auth"

export async function requireAuth() {
  try {
    const user = await queryClient.ensureQueryData(getAuthMeMeQueryOptions())
    return { user }
  } catch {
    throw redirect({ to: "/auth", replace: true })
  }
}
