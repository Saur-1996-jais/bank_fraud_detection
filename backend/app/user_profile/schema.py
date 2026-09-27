from enum import Enum
from sqlmodel import SQLModel, Field
from datetime import date
from pydantic_extra_types.country import CountryShortName
from pydantic_extra_types.phone_numbers import PhoneNumber


class SalutationSchema(str, Enum):
    Mr = "Mr"
    Mrs = "Mrs"
    Miss = "Miss"

class GenderSchema(str, Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class MaritalStatusSchema(str, Enum):
    Married = "Married"
    Single = "Single"
    Divorced = "Divorced"
    Widowed = "Widowed"

class IdentificationTypeSchema(str, Enum):
    Passport = "Passport"
    Drivers_Licence = "Drivers_Licence"
    National_Id = "National_Id"

class EmploymentStatusSchema(str, Enum):
    Employed = "Employed"
    Self_Employed = "Self_Employed"
    Unemployed = "Unemployed"
    Student = "Student"
    Retired = "Retired"

class ProfileBaseSchema(SQLModel):
    title: SalutationSchema
    gender: GenderSchema
    date_of_birth: date
    country_of_birth: CountryShortName
    place_of_birth: str
    means_of_identification: IdentificationTypeSchema
    marital_status: MaritalStatusSchema
    id_issue_date: date
    id_expiry_date: date
    passport_number: str
    nationality: str
    phone_number: PhoneNumber
    address: str
    city: str
    country: str
    employment_status: EmploymentStatusSchema
    employer_name: str
    employer_address: str
    employer_city: str
    employer_country: CountryShortName
    annual_income: float
    date_of_employment: date
    profile_photo_url: str | None = Field(default=None)
    id_photo_url: str | None = Field(default=None)
    signature_photo_url: str | None = Field(default=None)




