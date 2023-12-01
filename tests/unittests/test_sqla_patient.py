def test_add_patient(session, faker):
    from toubib.sqla import Patient

    patient = Patient(
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        date_of_birth=faker.date_object(),
        sex_at_birth=faker.bs(),
    )
    session.add(patient)
    session.flush()
    assert patient.id is not None


def test_get_patient(session, faker):
    from toubib.sqla import Patient

    patient = Patient(
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        date_of_birth=faker.date_object(),
        sex_at_birth=faker.bs(),
    )
    session.add(patient)
    session.flush()
    assert patient.id is not None

    patient = session.get(Patient, patient.id)
    assert patient.id == patient.id
    assert patient.email == patient.email
    assert patient.first_name == patient.first_name
    assert patient.last_name == patient.last_name
    assert patient.date_of_birth == patient.date_of_birth
    assert patient.sex_at_birth == patient.sex_at_birth
