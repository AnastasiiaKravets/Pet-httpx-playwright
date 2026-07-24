def test_message_invalid(api_client):
    # empty fields, phone with symbols, wrong email type
    response = api_client.post("/message")
    assert response.status_code == 400


def test_message_count(api_client):
    response = api_client.get("/message/count")
    assert response.status_code == 200
