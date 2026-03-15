import { ObjectActions } from "@/components/object-detail/object-actions";
import { useActionsActionGroupListActionsSuspense } from "@/openapi/actions/actions";
import type {
  ActionDTO,
  ActionGroupType,
  ActionListResponse,
} from "@/openapi/cuidaAPI.schemas";

interface TopLevelActionsProps {
  actionGroup: ActionGroupType;
  onInvalidate?: () => void;
  onActionComplete?: (action: ActionDTO, response: unknown) => void;
}

/**
 * Component that fetches and renders top-level actions for an action group.
 * Uses the list_actions endpoint to get available actions without object context.
 */
export function TopLevelActions({
  actionGroup,
  onInvalidate,
  onActionComplete,
}: TopLevelActionsProps) {
  const { data } = useActionsActionGroupListActionsSuspense(actionGroup);

  return (
    <ObjectActions
      actions={(data.data as ActionListResponse).actions}
      actionGroup={actionGroup}
      onInvalidate={onInvalidate}
      onActionComplete={onActionComplete}
    />
  );
}
