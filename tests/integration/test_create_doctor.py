async def test_it(client, faker):
    body = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "hiring_date": faker.date(),
        "specialization": faker.bs(),
    }
    res = await client.post("/v1/doctors", json=body)
    assert res.status_code == 201
    data = res.json()["data"]
    assert data["id"] is not None
    assert data["first_name"] == body["first_name"]
    assert data["last_name"] == body["last_name"]
    assert data["hiring_date"] == body["hiring_date"]
    assert data["specialization"] == body["specialization"]
