import React from "react";
import { UpdateUserForm } from "@/components/actions/update-user-form";
import { InviteUserForm } from "@/components/actions/invite-user-form";
import type {
  UserSchema,
  InviteUserAction,
  UpdateUserAction,
} from "@/openapi/cuidaAPI.schemas";
import type { DomainObject } from "@/types/domain-objects";

/**
 * Registry entry for an action
 * @template TData - The data type for the action (from the action's data field)
 * @template TObject - The object type this action operates on
 */
export interface ActionRegistryEntry<TData = unknown, TObject = DomainObject> {
  /**
   * Render function that returns the self-contained modal form component for this action.
   * If returns null, the action will be executed directly without a form.
   */
  render: (params: {
    objectData?: Partial<TObject>;
    onSubmit: (data: TData) => void;
    onClose: () => void;
    isSubmitting: boolean;
    isOpen: boolean;
    actionLabel: string;
  }) => React.ReactElement | null;
}

/** Extract the action discriminant string from a union member */
type ExtractActionType<T> = T extends { action: infer A } ? A : never;

/** Extract the data payload type from a union member */
type ExtractDataType<T> = T extends { data: infer D } ? D : unknown;

/** Combined discriminated union of all action bodies the backend accepts */
export type ActionBodyUnion = InviteUserAction | UpdateUserAction;

/**
 * All possible action type strings — derived from the discriminated union
 */
export type ActionType = ExtractActionType<ActionBodyUnion>;

/**
 * Map each action type string to its data payload type — derived automatically
 */
export type ActionDataTypeMap = {
  [K in ActionType]: ExtractDataType<Extract<ActionBodyUnion, { action: K }>>;
};

/**
 * Map action keys to their corresponding object types
 */
export type ActionToObjectMap = {
  user_actions__update: UserSchema;
};

/**
 * Type-safe action registry
 */
export type ActionRegistry = Partial<{
  [K in ActionType]: ActionRegistryEntry<
    ActionDataTypeMap[K],
    K extends keyof ActionToObjectMap ? ActionToObjectMap[K] : DomainObject
  >;
}>;

/**
 * The central action registry
 */
export const actionRegistry: ActionRegistry = {
  user_actions__update: {
    render: ({
      objectData,
      onSubmit,
      onClose,
      isSubmitting,
      isOpen,
      actionLabel,
    }) => {
      return (
        <UpdateUserForm
          isOpen={isOpen}
          onClose={onClose}
          defaultValues={objectData}
          onSubmit={onSubmit}
          isSubmitting={isSubmitting}
          actionLabel={actionLabel}
        />
      );
    },
  },
  org_actions__invite_user: {
    render: ({ onSubmit, onClose, isSubmitting, isOpen, actionLabel }) => {
      return (
        <InviteUserForm
          isOpen={isOpen}
          onClose={onClose}
          onSubmit={onSubmit}
          isSubmitting={isSubmitting}
          actionLabel={actionLabel}
        />
      );
    },
  },
};

/**
 * Get the render function for a given action type
 */
export function getActionRenderer(
  actionType: ActionType,
): ActionRegistryEntry<unknown, DomainObject>["render"] | undefined {
  const entry = actionRegistry[actionType];
  return entry?.render as
    | ActionRegistryEntry<unknown, DomainObject>["render"]
    | undefined;
}
