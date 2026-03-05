# app/users — Phase 2

User model, CRUD routes, and auth dependency.

## Files to create

```
app/users/
├── models.py    # User model: id, email (unique), name, created_at, updated_at, deleted_at
├── routes.py    # GET /users/me, PATCH /users/me
├── schemas.py   # UserDTO, UpdateUserRequest (msgspec structs)
└── service.py   # get_by_email(), get_by_id(), create(), update()
```

## Model

```python
class User(BaseDBModel):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str | None]
```

## Routes

All routes require auth guard from `app.auth.guards`.

| Method | Path | Description |
|--------|------|-------------|
| GET | /users/me | Return current user |
| PATCH | /users/me | Update name, etc. |

## Notes

- Soft delete inherited from `BaseDBModel` (`deleted_at`)
- Email uniqueness enforced at DB level (unique constraint)
- `UserDTO` is the safe serialization struct (excludes internal fields)
