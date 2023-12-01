async def test_get_health_return_ok(client):
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json() == "OK"
