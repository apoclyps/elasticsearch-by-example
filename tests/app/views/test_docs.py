def test_valid_docs(client):
    resp = client.get("/docs")
    assert resp.status_code == 200
