import { useState } from "react"
import { toast } from "sonner"
import { MagicLinkForm } from "@/components/auth/magic-link-form"
import { MagicLinkSuccess } from "@/components/auth/magic-link-success"
import { useAuthMagicLinkRequestRequestMagicLink } from "@/openapi/auth/auth"

export function AuthPage() {
  const [email, setEmail] = useState("")
  const [magicLinkSent, setMagicLinkSent] = useState(false)

  const mutation = useAuthMagicLinkRequestRequestMagicLink({
    mutation: {
      onSuccess: () => setMagicLinkSent(true),
      onError: () => toast.error("Failed to send magic link. Please try again."),
    },
  })

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    mutation.mutate({ data: { email } })
  }

  function handleTryAgain() {
    setMagicLinkSent(false)
    setEmail("")
  }

  return (
    <div className="bg-auth flex min-h-svh flex-col items-center justify-center px-4 py-6">
      {/* Wordmark */}
      <div className="mb-10 text-center">
        <p className="font-display text-[28px] tracking-wide text-foreground mb-2">Nearwise</p>
        <p className="text-sm text-muted-foreground">A daily companion for your loved ones</p>
      </div>

      {/* Card */}
      <div className="w-full max-w-sm rounded-2xl border border-border bg-card p-10 shadow-sm">
        {magicLinkSent ? (
          <MagicLinkSuccess email={email} onTryAgain={handleTryAgain} />
        ) : (
          <>
            <h1 className="font-display mb-2 text-[22px] font-normal text-foreground">
              Sign in to your account
            </h1>
            <p className="mb-7 text-sm leading-relaxed text-muted-foreground">
              Enter your email and we'll send you a secure magic link.
            </p>
            <MagicLinkForm
              email={email}
              isSubmitting={mutation.isPending}
              onEmailChange={setEmail}
              onSubmit={handleSubmit}
            />
          </>
        )}
      </div>

      <p className="mt-6 text-xs text-muted-foreground/60">© 2026 Nearwise</p>
    </div>
  )
}
