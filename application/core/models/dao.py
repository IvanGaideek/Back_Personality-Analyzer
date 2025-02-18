from application.crud.base import BaseDAO
from application.core.models.user import User


class UsersDAO(BaseDAO):
    model = User
