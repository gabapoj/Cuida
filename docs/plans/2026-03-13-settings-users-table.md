# Settings Users Table Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a user management table to the Settings page showing all org users with an Edit action per row.

**Architecture:** Add `GET /users` list endpoint to the backend (org-scoped), regenerate the frontend API client via orval codegen, then build the Settings page using shadcn's plain `Table` with per-row action menus wired to the existing actions framework.

**Tech Stack:** Litestar (Python), SQLAlchemy async, TanStack Query (orval-generated hooks), shadcn `Table` + `Avatar` + `DropdownMenu`, `useActionExecutor` + `useActionFormRenderer`

---

### Task 1: Add `GET /users` list endpoint (backend)

**Files:**
- Modify: `backend/app/users/queries.py`
- Modify: `backend/app/users/routes.py`

**Step 1: Add query function to `queries.py`**

Add below the existing `get_user_by_id` function:

```python
async def get_users_by_org(db: AsyncSession, organization_id: int) -> list[User]:
    result = await db.execute(
        select(User).where(User.organization_id == organization_id)
    )
    return list(result.scalars().all())
```

**Step 2: Add list route to `routes.py`**

Add a new `list_users` handler and wire it into the router. The full updated file:

```python
from litestar import Router, get
from litestar.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession

from app.actions.enums import ActionGroupType
from app.actions.registry import ActionRegistry
from app.auth.guards import requires_session
from app.users.models import User
from app.users.queries import get_users_by_org
from app.users.schemas import UserSchema


@get("/{user_id:int}")
async def get_user(
    user_id: int,
    transaction: AsyncSession,
    action_registry: ActionRegistry,
) -> UserSchema:
    result = await transaction.get(User, user_id)
    if result is None:
        raise NotFoundException()

    action_group = action_registry.get_class(ActionGroupType.UserActions)
    actions = action_group.get_available_actions(obj=result)

    return UserSchema(
        id=result.id,
        name=result.name,
        email=result.email,
        email_verified=result.email_verified,
        phone=result.phone,
        created_at=result.created_at,
        updated_at=result.updated_at,
        actions=actions,
    )


@get("")
async def list_users(
    request,
    transaction: AsyncSession,
    action_registry: ActionRegistry,
) -> list[UserSchema]:
    users = await get_users_by_org(transaction, request.user.organization_id)
    action_group = action_registry.get_class(ActionGroupType.UserActions)

    return [
        UserSchema(
            id=u.id,
            name=u.name,
            email=u.email,
            email_verified=u.email_verified,
            phone=u.phone,
            created_at=u.created_at,
            updated_at=u.updated_at,
            actions=action_group.get_available_actions(obj=u),
        )
        for u in users
    ]


user_router = Router(
    path="/users",
    route_handlers=[get_user, list_users],
    guards=[requires_session],
    tags=["users"],
)
```

**Step 3: Verify the backend runs**

```bash
cd backend
uv run litestar --app app.index:app run -p 8000
# In another terminal:
curl -s http://localhost:8000/users -H "Cookie: <session>" | python -m json.tool
# Or just verify the server starts without error
```

**Step 4: Commit**

```bash
git add backend/app/users/queries.py backend/app/users/routes.py
git commit -m "feat: add GET /users list endpoint"
```

---

### Task 2: Regenerate frontend API client

**Files:**
- Auto-generated: `web/src/openapi/users/users.ts`

**Step 1: Ensure backend is running at :8000**

```bash
cd backend && uv run litestar --app app.index:app run -p 8000
```

**Step 2: Run codegen**

```bash
cd web && pnpm run codegen
```

Expected: `web/src/openapi/users/users.ts` now contains `usersGetUsers`, `getUsersGetUsersQueryKey`, `useUsersGetUsersSuspense`, etc.

**Step 3: Verify the generated hook exists**

```bash
grep "useUsersGetUsers" web/src/openapi/users/users.ts
```

Expected: lines matching `useUsersGetUsers` and `useUsersGetUsersSuspense`.

**Step 4: Commit**

```bash
git add web/src/openapi/
git commit -m "chore: regenerate openapi client with GET /users list"
```

---

### Task 3: Install shadcn `table` component

**Files:**
- Create: `web/src/components/ui/table.tsx`

**Step 1: Add the component**

```bash
cd web && pnpm dlx shadcn@latest add @shadcn/table
```

**Step 2: Verify**

```bash
ls web/src/components/ui/table.tsx
```

**Step 3: Commit**

```bash
git add web/src/components/ui/table.tsx
git commit -m "chore: add shadcn table component"
```

---

### Task 4: Build the Settings page

**Files:**
- Modify: `web/src/pages/settings/settings-page.tsx`

**Step 1: Write the component**

Replace the contents of `web/src/pages/settings/settings-page.tsx`:

```tsx
import { useUsersGetUsersSuspense } from "@/openapi/users/users"
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
  return name
    .split(" ")
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

  const availableActions = user.actions.filter((a) => a.available !== false)

  return (
    <>
      <TableRow>
        <TableCell>
          <div className="flex items-center gap-3">
            <Avatar className="h-9 w-9">
              <AvatarFallback>{getInitials(user.name)}</AvatarFallback>
            </Avatar>
            <span className="font-medium">{user.name}</span>
          </div>
        </TableCell>
        <TableCell className="w-12">
          {availableActions.length > 0 && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="h-8 w-8 p-0">
                  <span className="sr-only">Open menu</span>
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                {availableActions.map((action) => (
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
  const { data } = useUsersGetUsersSuspense()
  const users = data.data as UserSchema[]

  return (
    <PageTopBar title="Settings">
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
    </PageTopBar>
  )
}
```

**Step 2: Check for TypeScript errors**

```bash
cd web && pnpm tsc --noEmit
```

Fix any import or type errors before continuing.

**Step 3: Commit**

```bash
git add web/src/pages/settings/settings-page.tsx
git commit -m "feat: add users table to settings page"
```

---

## Notes

- The `UpdateUser` action (`user_actions__update`) is only available when `obj.id == deps.user.id` — so the Edit menu item will only appear on the current user's own row. This is intentional for now and can be relaxed when roles/permissions are added.
- The `data.data` cast follows the same pattern used in `dashboard-page.tsx`.
- If `useUsersGetUsersSuspense` is named differently after codegen, check `web/src/openapi/users/users.ts` for the actual export name.
