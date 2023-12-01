from pytest import fixture


@fixture
def patient_no(faker, session):
    from datetime import datetime

    from toubib.sqla import Patient

    patient = Patient(
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        date_of_birth=datetime.strptime(faker.date(), "%Y-%m-%d").date(),
        sex_at_birth=faker.bs(),
    )
    session.add(patient)
    session.flush()
    return patient


# Get patient by existing ID
async def test_get_patient(client, patient_no):
    res = await client.get(f"/v1/patients/{patient_no.id}")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["id"] == patient_no.id
    assert data["email"] == patient_no.email
    assert data["first_name"] == patient_no.first_name
    assert data["last_name"] == patient_no.last_name
    assert data["date_of_birth"] == patient_no.date_of_birth.isoformat()
    assert data["sex_at_birth"] == patient_no.sex_at_birth


# Get patient by none existing ID
async def test_get_patient_not_found(client):
    res = await client.get(f"/v1/patients/9999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Patient not found"


# Get patient by invalid ID
async def test_get_patient_invalid_id(client):
    res = await client.get(f"/v1/patients/abc")
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid patient_id. Must be an integer."
