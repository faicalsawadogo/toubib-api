from datetime import date
from importlib.metadata import version
from fastapi.middleware.cors import CORSMiddleware

import fastapi_sqla
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi_sqla import Item, List, Session
from pydantic import BaseModel
from sqlalchemy import func
from structlog import get_logger

from .schemas import DoctorIn, DoctorModel, PatientIn, PatientModel
from .sqla import Doctor, Patient

log = get_logger()

app = FastAPI(title="toubib", version=version("toubib"))

fastapi_sqla.setup(app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    "Return OK if app is reachable"
    return "OK"


@app.post("/v1/doctors", response_model=Item[DoctorModel], status_code=201)
def create_doctor(*, body: DoctorIn, session: Session = Depends()):
    doctor = Doctor(**body.dict())
    session.add(doctor)
    session.flush()
    return {"data": doctor}


@app.get("/v1/doctors/{doctor_id}", response_model=Item[DoctorModel])
def get_doctor(*, doctor_id: int, session: Session = Depends()):
    doctor = session.get(Doctor, doctor_id)
    if doctor is None:
        raise HTTPException(404, detail=f"Doctor with {doctor_id} not found")
    return {"data": doctor}


@app.get("/v1/patients", response_model=dict)
def list_patients(offset: int = 0, limit: int = 10, db: Session = Depends()):
    total_items = db.query(func.count(Patient.id)).scalar()

    patients = (
        db.query(Patient)
        .order_by(func.lower(Patient.last_name))  # Sorting alphabetically by last name
        .offset(offset)
        .limit(limit)
        .all()
    )

    data = [
        {
            "id": patient.id,
            "email": patient.email,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "date_of_birth": str(patient.date_of_birth),
            "sex_at_birth": patient.sex_at_birth,
        }
        for patient in patients
    ]

    total_pages = -(-total_items // limit)  # Calculate total pages

    meta = {
        "offset": offset,
        "total_items": total_items,
        "total_pages": total_pages,
        "page_number": (offset // limit) + 1,
    }

    response = {"data": data, "meta": meta}
    return response


@app.post("/v1/patients", response_model=Item[PatientModel], status_code=201)
def create_patient(*, body: PatientIn, session: Session = Depends()):
    # Check if the email already exists in the database
    existing_patient = (
        session.query(Patient).filter(Patient.email == body.email).first()
    )
    if existing_patient:
        raise HTTPException(400, detail="Email already registered.")

    # If the email is unique, proceed with creating the patient
    patient = Patient(**body.dict())
    session.add(patient)
    session.flush()
    return {"data": patient}


@app.get("/v1/patients/{patient_id}", response_model=Item[PatientModel])
def get_patient(*, patient_id: str, session: Session = Depends()):
    try:
        patient_id_int = int(patient_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid patient_id. Must be an integer.",
        )

    patient = session.get(Patient, patient_id_int)
    if patient is None:
        raise HTTPException(404, detail=f"Patient not found")

    return {"data": patient}
