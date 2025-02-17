from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, Base):
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)  # уникальный username
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)  # уникальный email
    password: Mapped[str] = mapped_column(String, nullable=False)
