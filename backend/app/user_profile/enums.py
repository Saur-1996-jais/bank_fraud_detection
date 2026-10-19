from enum import Enum


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


class ImageTypeSchema(str, Enum):
    PROFILE_PHOTO = "profile_photo"
    ID_PHOTO = "id_photo"
    SIGNATURE_PHOTO = "signature_photo"
