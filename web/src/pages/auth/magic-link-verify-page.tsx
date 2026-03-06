import { useEffect } from "react"
import { useSearch, useNavigate } from "@tanstack/react-router"

export function MagicLinkVerifyPage() {
  const { token } = useSearch({ from: "/_public/auth/magic-link/verify" })
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) {
      void navigate({ to: "/auth", replace: true })
      return
    }

    const url = `${import.meta.env.VITE_API_URL ?? "http://localhost:8000"}/auth/magic-link/verify?token=${encodeURIComponent(token)}`

    fetch(url, { credentials: "include" })
      .then((res) => {
        if (res.ok) {
          window.location.href = "/dashboard"
        } else {
          void navigate({ to: "/auth", replace: true })
        }
      })
      .catch(() => {
        void navigate({ to: "/auth", replace: true })
      })
  }, [token, navigate])

  return (
    <div className="bg-auth flex min-h-svh flex-col items-center justify-center gap-4">
      <p className="font-display text-2xl tracking-wide text-foreground">Nearwise</p>
      <p className="text-sm text-muted-foreground">Verifying your link&hellip;</p>
    </div>
  )
}
