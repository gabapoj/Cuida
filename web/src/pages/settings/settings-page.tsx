import { useQueryClient } from "@tanstack/react-query";
import {
  useUsersListUsersSuspense,
  getUsersListUsersQueryKey,
} from "@/openapi/users/users";
import { ActionsMenu } from "@/components/actions-menu";
import { TopLevelActions } from "@/components/object-list/top-level-actions";
import { PageTopBar } from "@/components/page-topbar";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { UserSchema } from "@/openapi/cuidaAPI.schemas";

function getInitials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "?";
  return parts
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
}

function UserRow({ user }: { user: UserSchema }) {
  return (
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
          <ActionsMenu
            actions={user.actions}
            actionGroup="user_actions"
            objectId={String(user.id)}
            objectData={user}
          />
        )}
      </TableCell>
    </TableRow>
  );
}

export function SettingsPage() {
  const queryClient = useQueryClient();
  const { data } = useUsersListUsersSuspense();
  const users = data.data;

  return (
    <PageTopBar
      title="Settings"
      actions={
        <TopLevelActions
          actionGroup="org_actions"
          onInvalidate={() =>
            void queryClient.invalidateQueries({
              queryKey: getUsersListUsersQueryKey(),
            })
          }
        />
      }
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
    </PageTopBar>
  );
}
