import { ObjectActions } from '@/components/object-detail/object-actions';
import { useActionsActionGroupListActionsSuspense } from '@/openapi/actions/actions';
import type { ActionGroupType } from '@/openapi/cuidaAPI.schemas';

interface TopLevelActionsProps {
  actionGroup: ActionGroupType;
}

/**
 * Component that fetches and renders top-level actions for an action group.
 * Uses the list_actions endpoint to get available actions without object context.
 */
export function TopLevelActions({ actionGroup }: TopLevelActionsProps) {
  // Fetch available top-level actions
  // Note: data.data wraps the response (orval response shape)
  const { data } = useActionsActionGroupListActionsSuspense(actionGroup);

  return (
    <ObjectActions
      actions={data.data.actions}
      actionGroup={actionGroup}
    />
  );
}
