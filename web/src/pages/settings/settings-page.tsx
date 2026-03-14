import { useQueryClient } from "@tanstack/react-query"
import { useUsersListUsersSuspense, getUsersListUsersQueryKey } from "@/openapi/users/users"
import { useActionsActionGroupListActionsSuspense } from "@/openapi/actions/actions"
import { useActionExecutor } from "@/hooks/use-action-executor"
import { useActionFormRenderer } from "@/hooks/use-action-form-renderer"
import { PageTopBar } from "@/components/page-topbar"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { MoreHorizontal } from "lucide-react"
import type { UserSchema } from "@/openapi/cuidaAPI.schemas"

function getInitials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean)
  if (parts.length === 0) return "?"
  return parts
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2)
}

function UserRow({ user }: { user: UserSchema }) {
  const renderActionForm = useActionFormRenderer(user)
  const executor = useActionExecutor({
    actionGroup: "user_actions",
    objectId: String(user.id),
    renderActionForm,
  })

  return (
    <>
      <TableRow>
        <TableCell>
          <div className="flex items-center gap-3">
            <Avatar size="lg">
              <AvatarFallback>{getInitials(user.name)}</AvatarFallback>
            </Avatar>
            <span className="font-medium">{user.name}</span>
          </div>
        </TableCell>
        <TableCell className="w-12">
          {user.actions.length > 0 && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="h-8 w-8 p-0">
                  <span className="sr-only">Open menu</span>
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                {user.actions.map((action) => (
                  <DropdownMenuItem
                    key={action.action}
                    onClick={() => executor.initiateAction(action)}
                  >
                    {action.label}
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </TableCell>
      </TableRow>
      {executor.showForm &&
        executor.pendingAction &&
        executor.renderActionForm?.({
          action: executor.pendingAction,
          onSubmit: executor.executeWithData,
          onClose: executor.cancelAction,
          isSubmitting: executor.isExecuting,
          isOpen: executor.showForm,
          actionLabel: executor.pendingAction.label,
        })}
    </>
  )
}

export function SettingsPage() {
  const queryClient = useQueryClient()
  const { data } = useUsersListUsersSuspense()
  const users = data.data

  const { data: orgActionsData } = useActionsActionGroupListActionsSuspense("org_actions")
  const orgActions = orgActionsData.data.actions

  const renderInviteForm = useActionFormRenderer()
  const orgExecutor = useActionExecutor({
    actionGroup: "org_actions",
    renderActionForm: renderInviteForm,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: getUsersListUsersQueryKey() })
    },
  })

  return (
    <PageTopBar
      title="Settings"
      actions={orgActions.map((action) => (
        <Button key={action.action} onClick={() => orgExecutor.initiateAction(action)}>
          {action.label}
        </Button>
      ))}
    >
      <div className="p-6">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>User</TableHead>
              <TableHead className="w-12" />
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.map((user) => (
              <UserRow key={user.id} user={user} />
            ))}
          </TableBody>
        </Table>
      </div>
      {orgExecutor.showForm &&
        orgExecutor.pendingAction &&
        orgExecutor.renderActionForm?.({
          action: orgExecutor.pendingAction,
          onSubmit: orgExecutor.executeWithData,
          onClose: orgExecutor.cancelAction,
          isSubmitting: orgExecutor.isExecuting,
          isOpen: orgExecutor.showForm,
          actionLabel: orgExecutor.pendingAction.label,
        })}
    </PageTopBar>
  )
}
