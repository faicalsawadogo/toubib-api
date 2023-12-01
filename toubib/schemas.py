from datetime import date

from pydantic import BaseModel


class DoctorIn(BaseModel):
    first_name: str
    last_name: str
    hiring_date: date
    specialization: str


class DoctorModel(DoctorIn):
    id: int

    class Config:
        orm_mode = True


class PatientIn(BaseModel):
    email: str
    first_name: str
    last_name: str
    date_of_birth: date
    sex_at_birth: str


class PatientModel(PatientIn):
    id: int

    class Config:
        orm_mode = True
