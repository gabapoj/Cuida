# Settings - Users Table Design

**Date:** 2026-03-13

## Overview

Add a user management table to the Settings page. Displays all users with avatar (initials) and name. Each row has an actions menu (`...`) powered by the existing actions framework, with an Edit action that opens a modal.

## Backend

### New endpoint: `GET /users`

- Added to `user_router` in `backend/app/users/routes.py`
- Queries all `User` rows, attaches available actions per user (same pattern as `GET /users/{user_id}`)
- Returns `list[UserSchema]`
- Protected by `requires_session` guard

**Note:** The existing `UpdateUser` action is only available when `obj.id == deps.user.id`. Other users will have an empty actions list until that guard is updated.

## Frontend

### Data fetching

- `useUsersSuspense` query hook (or equivalent) fetching `GET /users`
- Follows existing project patterns (TanStack Query)

### Settings page

- Plain shadcn `Table` (no TanStack Table abstraction — table is simple)
- Two columns:
  - **User**: `Avatar` (initials from name) + name
  - **Actions**: `DropdownMenu` (`...`) with items driven by the `actions` array from the API

### Edit flow

- Edit item in dropdown triggers the existing actions framework
- Opens an edit modal (consistent with rest of app)

## Out of scope

- Role/status/last active columns
- Search, filter, pagination
- Avatar images (initials only for now)
