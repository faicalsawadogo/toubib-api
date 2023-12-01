from pytest import fixture


@fixture
def list_patients_no(faker, session):
    from datetime import datetime

    from toubib.sqla import Patient

    patients = [
        Patient(
            email="fake@example.com",
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            date_of_birth=datetime.strptime(faker.date(), "%Y-%m-%d").date(),
            sex_at_birth=faker.bs(),
        )
        for _ in range(2)
    ]
    session.add_all(patients)
    session.flush()
    return patients

    async def create_patient_success(client, list_patients_no):
        res = await client.post(
            "/v1/patients",
            json={
                "email": list_patients_no[0].email,
                "first_name": list_patients_no[0].first_name,
                "last_name": list_patients_no[0].last_name,
                "date_of_birth": list_patients_no[0].date_of_birth,
                "sex_at_birth": list_patients_no[0].sex_at_birth,
            },
        )

    async def test_create_email_already_exists(client, list_patients_no):
        res = await client.post(
            "/v1/patients",
            json={
                "email": list_patients_no[1].email,
                "first_name": list_patients_no[1].first_name,
                "last_name": list_patients_no[1].last_name,
                "date_of_birth": list_patients_no[1].date_of_birth,
                "sex_at_birth": list_patients_no[1].sex_at_birth,
            },
        )
        assert res.status_code == 400
        assert res.json()["detail"] == "Email already registered."
