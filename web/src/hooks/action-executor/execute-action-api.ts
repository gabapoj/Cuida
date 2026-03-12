import type {
  ActionDTO,
  ActionGroupType,
  ActionExecutionResponse,
  UpdateUserAction,
} from '@/openapi/cuidaAPI.schemas';

type ExecuteActionApiParams = {
  action: ActionDTO;
  actionGroup: ActionGroupType;
  objectId?: string;
  actionBody?: unknown;
  executeGroupActionMutation: {
    mutateAsync: (params: {
      actionGroup: ActionGroupType;
      data: UpdateUserAction;
    }) => Promise<{ data: ActionExecutionResponse }>;
  };
  executeObjectActionMutation: {
    mutateAsync: (params: {
      actionGroup: ActionGroupType;
      objectId: number;
      data: UpdateUserAction;
    }) => Promise<{ data: ActionExecutionResponse }>;
  };
};

/**
 * Execute action API call with proper typing based on whether we have an objectId
 */
export async function executeActionApi({
  action,
  actionGroup,
  objectId,
  actionBody,
  executeGroupActionMutation,
  executeObjectActionMutation,
}: ExecuteActionApiParams): Promise<ActionExecutionResponse> {
  // Use provided action body or build default one
  const requestBody =
    actionBody || ({ action: action.action, data: {} } as const);

  // Execute with proper typing based on whether we have an objectId
  if (objectId) {
    return (
      await executeObjectActionMutation.mutateAsync({
        actionGroup,
        objectId: Number(objectId),
        data: requestBody as UpdateUserAction,
      })
    ).data;
  } else {
    return (
      await executeGroupActionMutation.mutateAsync({
        actionGroup,
        data: requestBody as UpdateUserAction,
      })
    ).data;
  }
}
