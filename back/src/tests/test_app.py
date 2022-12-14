
def test_users(test_app, api_url):
    response = test_app.post(api_url("users"))
    assert response.status_code == 422 

