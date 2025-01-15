import pytest

user = {"email": "user@test.com", "password": "test"}


@pytest.mark.asyncio
async def test_register(client):
    resp = client.post(
        "/auth/register",
        json=user
    )
    assert resp.status_code == 201 or resp.status_code == 400 and 'REGISTER_USER_ALREADY_EXISTS' in resp.text, resp.text


@pytest.mark.asyncio
async def test_login(client):
    resp = client.post(
        "/auth/login",
        data={"username": user['email'], 'password': user['password']}
    )
    assert resp.status_code == 200, resp.text
    access_token = resp.json().get("access_token")
    assert access_token is not None and isinstance(access_token, str) and len(access_token) > 0


@pytest.mark.asyncio
async def test_login_with_invalid_password(client):
    resp = client.post(
        "/auth/login",
        data={"username": user['email'], 'password': "invalid"}
    )
    assert resp.status_code == 400, resp.text

