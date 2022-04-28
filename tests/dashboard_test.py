"""this tests access denied to dashboard and upload"""

def test_deny_access(client):
    response = client.get("/browse_songs")
    assert response.status_code == 404

    response = client.get("/upload")
    assert response.status_code == 404
