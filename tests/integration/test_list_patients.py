from pytest import fixture


@fixture
def list_patients_no(faker, session):
    from datetime import datetime

    from toubib.sqla import Patient

    patients = [
        Patient(
            email=faker.email(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            date_of_birth=datetime.strptime(faker.date(), "%Y-%m-%d").date(),
            sex_at_birth=faker.bs(),
        )
        for _ in range(20)
    ]
    session.add_all(patients)
    session.flush()
    return patients

    async def test_list_patients(client, list_patients_no):
        res = await client.get("/v1/patients")
        assert res.status_code == 200
        data = res.json()["data"]
        assert len(data) == len(list_patients_no)
        assert all(d["id"] == p.id for d, p in zip(data, list_patients_no))
        assert all(d["email"] == p.email for d, p in zip(data, list_patients_no))
        assert all(
            d["first_name"] == p.first_name for d, p in zip(data, list_patients_no)
        )
        assert all(
            d["last_name"] == p.last_name for d, p in zip(data, list_patients_no)
        )
        assert all(
            d["date_of_birth"] == str(p.date_of_birth)
            for d, p in zip(data, list_patients_no)
        )
        assert all(
            d["sex_at_birth"] == p.sex_at_birth for d, p in zip(data, list_patients_no)
        )
        assert res.json()["meta"]["total_items"] == len(list_patients_no)
        assert res.json()["meta"]["total_pages"] == -(-len(list_patients_no) // 10) + 1
        assert res.json()["meta"]["page_number"] == 1
        assert res.json()["meta"]["offset"] == 0
        assert res.json()["meta"]["limit"] == 10

    async def test_list_patients_page(client, list_patients_no):
        res = await client.get("/v1/patients?page=2")
        assert res.status_code == 200
        data = res.json()["data"]
        assert len(data) == len(list_patients_no)
        assert all(d["id"] == p.id for d, p in zip(data, list_patients_no))
        assert all(d["email"] == p.email for d, p in zip(data, list_patients_no))
        assert all(
            d["first_name"] == p.first_name for d, p in zip(data, list_patients_no)
        )
        assert all(
            d["last_name"] == p.last_name for d, p in zip(data, list_patients_no)
        )
        assert all(
            d["date_of_birth"] == str(p.date_of_birth)
            for d, p in zip(data, list_patients_no)
        )
        assert all(
            d["sex_at_birth"] == p.sex_at_birth for d, p in zip(data, list_patients_no)
        )
        assert res.json()["meta"]["total_items"] == len(list_patients_no)
        assert res.json()["meta"]["total_pages"] == -(-len(list_patients_no) // 10) + 1
        assert res.json()["meta"]["page_number"] == 2
        assert res.json()["meta"]["offset"] == 10
        assert res.json()["meta"]["limit"] == 10
