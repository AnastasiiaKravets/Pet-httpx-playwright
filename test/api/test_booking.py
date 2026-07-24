def test_booking_by_room_id(api_client):
    response = api_client.get("/booking?roomid=1")
    assert response.status_code == 200
