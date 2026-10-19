from enum import Enum


class SalutationEnum(str, Enum):
    Mr = "Mr"
    Mrs = "Mrs"
    Miss = "Miss"

class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class MaritalStatusEnum(str, Enum):
    Married = "Married"
    Single = "Single"
    Divorced = "Divorced"
    Widowed = "Widowed"

class IdentificationTypeEnum(str, Enum):
    Passport = "Passport"
    Drivers_Licence = "Drivers_Licence"
    National_Id = "National_Id"

class EmploymentStatusEnum(str, Enum):
    Employed = "Employed"
    Self_Employed = "Self_Employed"
    Unemployed = "Unemployed"
    Student = "Student"
    Retired = "Retired"


class ImageTypeEnum(str, Enum):
    PROFILE_PHOTO = "profile_photo"
    ID_PHOTO = "id_photo"
    SIGNATURE_PHOTO = "signature_photo"
