import React from 'react';
import { UpdateUserForm } from '@/components/actions/update-user-form';
import { InviteUserForm } from '@/components/actions/invite-user-form';
import type {
  UserSchema,
  UserUpdateSchema,
  InviteUserSchema,
} from '@/openapi/cuidaAPI.schemas';
import type { DomainObject } from '@/types/domain-objects';

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

/**
 * All possible action types in Cuida
 */
export type ActionType = 'user_actions__update' | 'org_actions__invite_user';

/**
 * Map action type to its data type
 */
export type ActionDataTypeMap = {
  user_actions__update: UserUpdateSchema;
  org_actions__invite_user: InviteUserSchema;
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
    render: ({
      onSubmit,
      onClose,
      isSubmitting,
      isOpen,
      actionLabel,
    }) => {
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
  actionType: ActionType
): ActionRegistryEntry<unknown, DomainObject>['render'] | undefined {
  const entry = actionRegistry[actionType];
  return entry?.render as
    | ActionRegistryEntry<unknown, DomainObject>['render']
    | undefined;
}
