import type {
  ActionDTO,
  ActionGroupType,
  ActionExecutionResponse,
} from "@/openapi/cuidaAPI.schemas";
import type { ActionBodyUnion } from "@/lib/actions/registry";

type ExecuteActionApiParams = {
  action: ActionDTO;
  actionGroup: ActionGroupType;
  objectId?: string;
  actionBody?: ActionBodyUnion;
  executeGroupActionMutation: {
    mutateAsync: (params: {
      actionGroup: ActionGroupType;
      data: ActionBodyUnion;
    }) => Promise<unknown>;
  };
  executeObjectActionMutation: {
    mutateAsync: (params: {
      actionGroup: ActionGroupType;
      objectId: number;
      data: ActionBodyUnion;
    }) => Promise<unknown>;
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
      (await executeObjectActionMutation.mutateAsync({
        actionGroup,
        objectId: Number(objectId),
        data: requestBody as ActionBodyUnion,
      })) as { data: ActionExecutionResponse }
    ).data;
  } else {
    return (
      (await executeGroupActionMutation.mutateAsync({
        actionGroup,
        data: requestBody as ActionBodyUnion,
      })) as { data: ActionExecutionResponse }
    ).data;
  }
}
