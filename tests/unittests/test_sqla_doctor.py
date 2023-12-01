def test_add_doctor(session, faker):
    from toubib.sqla import Doctor

    doctor = Doctor(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        hiring_date=faker.date_object(),
        specialization=faker.bs(),
    )
    session.add(doctor)
    session.flush()
    assert doctor.id is not None


def test_get_doctor(session, faker):
    from toubib.sqla import Doctor

    doctor = Doctor(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        hiring_date=faker.date_object(),
        specialization=faker.bs(),
    )
    session.add(doctor)
    session.flush()
    assert doctor.id is not None

    doctor = session.get(Doctor, doctor.id)
    assert doctor.id == doctor.id
    assert doctor.first_name == doctor.first_name
    assert doctor.last_name == doctor.last_name
    assert doctor.hiring_date == doctor.hiring_date
    assert doctor.specialization == doctor.specialization
