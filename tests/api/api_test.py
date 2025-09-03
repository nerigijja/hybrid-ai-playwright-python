def test_get_users(api_client):
    r = api_client.get('/users')
    assert r.status_code == 200
    assert isinstance(r.json(), (list, dict))
