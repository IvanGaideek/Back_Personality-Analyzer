from typing import Any, Optional, TypeVar, List,  Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field
import sys

from fastapi_users import models
class UserBase(BaseModel):
    name: str

class User(UserBase):
    id: models.ID


class UserCreate(User):
    name: Annotated[str, Field(..., title = 'Имя', min_length=1, max_length=30)]  # имя
    email: Annotated[str, Field(..., title = 'Email', min_length=1, max_length=90)]  # почта


    class Config:
        model_config = ConfigDict(from_attributes=True)

PYDANTIC_V2 = sys.version_info >= (3, 10)

if not PYDANTIC_V2:
    raise Exception("This code is intended to be used with Pydantic v2 and above")

SCHEMA = TypeVar("SCHEMA", bound=BaseModel)

if PYDANTIC_V2:  # pragma: no cover

    def model_dump(model: BaseModel, *args, **kwargs) -> dict[str, Any]:
        return model.model_dump(*args, **kwargs)  # type: ignore

    def model_validate(schema: type[SCHEMA], obj: Any, *args, **kwargs) -> SCHEMA:
        return schema.model_validate(obj, *args, **kwargs)  # type: ignore

else:  # pragma: no cover  # type: ignore

    def model_dump(model: BaseModel, *args, **kwargs) -> dict[str, Any]:
        return model.model_dump(*args, **kwargs)  # type: ignore

    def model_validate(schema: type[SCHEMA], obj: Any, *args, **kwargs) -> SCHEMA:
        return schema.model_validate(obj)  # type: ignore


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return model_dump(
            self,
            exclude_unset=True,
            exclude={
                "id",
                "is_superuser",
                "is_active",
                "is_verified",
                "oauth_accounts",
            },
        )

    def get_update_dict_superuser(self):
        """Return the data as a dictionary for superuser updates, excluding the ID."""
        return model_dump(self, exclude_unset=True, exclude={"id"})


class BaseUser(CreateUpdateDictModel, BaseModel):
    """Base User model."""

    id: models.ID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class BaseUserCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class BaseUserUpdate(CreateUpdateDictModel):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


U = TypeVar("U", bound=BaseUser)
UC = TypeVar("UC", bound=BaseUserCreate)
UU = TypeVar("UU", bound=BaseUserUpdate)


class BaseOAuthAccount(BaseModel):
    """Base OAuth account model."""

    id: models.ID
    oauth_name: str
    access_token: str
    expires_at: Optional[int] = None
    refresh_token: Optional[str] = None
    account_id: str
    account_email: str

    model_config = ConfigDict(from_attributes=True)


class BaseOAuthAccountMixinManual(BaseModel):
    """Adds OAuth accounts list to a User model."""
    oauth_accounts: List[BaseOAuthAccount] = None
    def __init__(self, **data):
      if "oauth_accounts" not in data or data['oauth_accounts'] is None:
          super().__init__(oauth_accounts=[])
      else:
        super().__init__(**data)