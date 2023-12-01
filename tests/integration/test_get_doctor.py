from pytest import fixture


@fixture
def doctor_no(faker, session):
    from toubib.sqla import Doctor

    doctor = Doctor(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        hiring_date=faker.date_object(),
        specialization=faker.bs(),
    )
    session.add(doctor)
    session.flush()
    return doctor


async def test_get_doctor(client, doctor_no):
    res = await client.get(f"/v1/doctors/{doctor_no.id}")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["id"] == doctor_no.id
    assert data["first_name"] == doctor_no.first_name
    assert data["last_name"] == doctor_no.last_name
    assert data["hiring_date"] == doctor_no.hiring_date.isoformat()
    assert data["specialization"] == doctor_no.specialization
