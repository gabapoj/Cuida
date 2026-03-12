from typing import Any

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseDBModel(DeclarativeBase):
    """Declarative base — provides id, registry helpers, and instance utilities.

    Most models should also mix in OrgScopedMixin which adds the standard
    audit columns (created_at, updated_at, deleted_at) and organization_id.
    """

    _model_registry: set[type["BaseDBModel"]] = set()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "__tablename__"):
            BaseDBModel._model_registry.add(cls)

    @classmethod
    def get_all_models(cls) -> set[type["BaseDBModel"]]:
        return cls._model_registry

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def to_dict(self) -> dict[str, Any]:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
