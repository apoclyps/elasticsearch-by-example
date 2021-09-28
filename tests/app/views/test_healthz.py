def test_healthcheck(client):
    response = client.get("/healthz")

    assert response.json == {"success": True}
    assert response.status_code == 200


def test_public_healthcheck(client):
    response = client.get("/public")

    assert response.json == {"success": True}
    assert response.status_code == 200
