from fastapi_sqla import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class Doctor(Base):
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hiring_date = Column(Date, nullable=False)
    specialization = Column(String, nullable=False)


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    sex_at_birth = Column(String, nullable=False)
    __table_args__ = (UniqueConstraint("email"),)
