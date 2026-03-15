import { useCallback } from "react";
import { getActionRenderer, type ActionType } from "@/lib/actions/registry";
import type { ActionFormRenderer } from "./use-action-executor";
import type { DomainObject } from "@/types/domain-objects";

/**
 * Hook that creates an ActionFormRenderer using the centralized action registry
 */
export function useActionFormRenderer(
  objectData?: DomainObject,
): ActionFormRenderer {
  return useCallback<ActionFormRenderer>(
    ({ action, onSubmit, onClose, isSubmitting, isOpen, actionLabel }) => {
      const actionType = action.action as ActionType;
      const render = getActionRenderer(actionType);

      // No render function registered - action will be executed directly
      if (!render) {
        return null;
      }

      // Call the render function with all parameters
      return render({
        objectData,
        onSubmit: (data) => {
          // Transform the form data into the action body format
          onSubmit({
            action: actionType,
            data,
          } as Parameters<typeof onSubmit>[0]);
        },
        onClose,
        isSubmitting,
        isOpen,
        actionLabel,
      });
    },
    [objectData],
  );
}
