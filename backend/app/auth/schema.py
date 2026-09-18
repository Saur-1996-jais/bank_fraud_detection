from enum import Enum
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from fastapi import status, HTTPException

class SecurityQuestionsSchema(str, Enum):
    MOTHER_MAIDEN_NAME = "mother_maiden_name"
    CHILDHOOD_FRIEND = "childhood_friend"
    FAVORITE_COLOR = "favorite_color"
    BIRTH_CITY = "birth_city"

    @classmethod
    def get_description(cls, value: "SecurityQuestionsSchema") -> str:
        description = {
            cls.MOTHER_MAIDEN_NAME: "what is the name of your mother?",
            cls.CHILDHOOD_FRIEND: "what is the name of your childhood friend?",
            cls.FAVORITE_COLOR: "what is your favorite color?",
            cls.BIRTH_CITY: "what is your birth city?",
        }
        return description.get(value, "Unknown security question")

class AccountsStatusSchema(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    PENDING = "pending"

class RolChoicesSchema(str, Enum):
    CUSTOMER = "customer"
    ACCOUNT_EXECUTIVE = "account_executive"
    BRANCH_MANAGER = "branch_manager"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    TELLER = "teller"

class BaseUserSchema(SQLModel):
    username: str | None = Field(default=None, max_length=12)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    first_name: str = Field(max_length=30)
    middle_name : str | None = Field(max_length=30, default=None)
    last_name: str = Field(max_length=30)
    id_no: int = Field(unique=True, gt=0)
    is_active: bool = False
    is_superuser: bool = False
    security_questions: SecurityQuestionsSchema = Field(max_length=30)
    security_answer: str = Field(max_length=30)
    account_status: AccountsStatusSchema = Field(default=AccountsStatusSchema.INACTIVE)
    role: RolChoicesSchema = Field(default=RolChoicesSchema.CUSTOMER)

class UserCreateSchema(BaseUserSchema):
    password: str = Field(min_length=8, max_length=40)
    confirm_password: str = Field(min_length=8, max_length=40)

    @field_validator("confirm_password")
    def validate_confirm_password(cls,v,values):
        if "password" in values.data and v!= values.data["password"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = {
                    "status" : "error",
                    "message" : "Please ensure that the passwords you entered match",
                    }
            )
        return v



