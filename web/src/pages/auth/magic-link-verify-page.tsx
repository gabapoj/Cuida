import { useEffect } from "react"
import { useSearch, useNavigate } from "@tanstack/react-router"

export function MagicLinkVerifyPage() {
  const navigate = useNavigate()
  const search = useSearch({ from: "/_public/auth/magic-link/verify" })

  useEffect(() => {
    const verifyToken = async () => {
      const token = search.token

      if (!token) {
        void navigate({ to: "/auth", replace: true })
        return
      }

      try {
        const response = await fetch(
          `/api/auth/magic-link/verify?token=${encodeURIComponent(token)}`,
          { method: "GET", credentials: "include" },
        )

        if (response.ok) {
          window.location.href = "/"
        } else {
          void navigate({ to: "/auth", replace: true })
        }
      } catch {
        void navigate({ to: "/auth", replace: true })
      }
    }

    void verifyToken()
  }, [search.token, navigate])

  return (
    <div className="bg-auth flex min-h-svh flex-col items-center justify-center gap-4">
      <p className="font-display text-2xl tracking-wide text-foreground">Nearwise</p>
      <p className="text-sm text-muted-foreground">Verifying your link&hellip;</p>
    </div>
  )
}
