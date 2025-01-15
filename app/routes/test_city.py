import pytest

from app.schemas.city import CitySchema, CityWeatherFiltersSchema
from app.schemas.weather import WeatherSchema

city1 = CitySchema(longitude=0.01, latitude=0.01, name="Test city")
city2 = CitySchema(longitude=0.01, latitude=0.01, name="Another test city")


@pytest.fixture
def token(client) -> str:
    resp = client.post(
        '/auth/register',
        json={"email": "testuser@romakot321.github.io", "password": "test"}
    )
    assert resp.status_code == 201 or resp.status_code == 400 and 'REGISTER_USER_ALREADY_EXISTS' in resp.text, resp.text
    resp = client.post(
        '/auth/login',
        data={"username": "testuser@romakot321.github.io", "password": "test"}
    )
    assert resp.status_code == 200, resp.text
    return "Bearer " + resp.json()["access_token"]


@pytest.fixture
def another_token(client) -> str:
    resp = client.post(
        '/auth/register',
        json={"email": "testuser2@romakot321.github.io", "password": "test"}
    )
    assert resp.status_code == 201 or resp.status_code == 400 and 'REGISTER_USER_ALREADY_EXISTS' in resp.text, resp.text
    resp = client.post(
        '/auth/login',
        data={"username": "testuser2@romakot321.github.io", "password": "test"}
    )
    assert resp.status_code == 200, resp.text
    return "Bearer " + resp.json()["access_token"]


@pytest.mark.asyncio
async def test_city_add(client, token):
    resp = client.post(
        '/city',
        json=city1.model_dump(),
        headers={"Authorization": token}
    )
    assert resp.status_code in (201, 409), resp.text


@pytest.mark.asyncio
async def test_cities_get(client, token):
    resp = client.get(
        '/city',
        headers={"Authorization": token}
    )
    assert resp.status_code == 200, resp.text
    assert city1.name in [i["name"] for i in resp.json()], "Cannot find added city"


@pytest.mark.asyncio
async def test_users_cities_list_not_intersect(client, another_token):
    resp = client.post(
        '/city',
        json=city2.model_dump(),
        headers={"Authorization": another_token}
    )
    assert resp.status_code in (201, 409), resp.text
    resp = client.get(
        '/city',
        headers={"Authorization": another_token}
    )
    assert resp.status_code == 200, resp.text
    assert city1.name not in [i["name"] for i in resp.json()], "Founded city from another user"
    assert city2.name in [i["name"] for i in resp.json()], "Cannot find added city"


@pytest.mark.asyncio
async def test_city_weather_get(client, token):
    filters = CityWeatherFiltersSchema(name=city1.name, time="12:23")
    resp = client.get(
        '/city/weather',
        params=filters.model_dump(),
        headers={"Authorization": token}
    )
    assert resp.status_code == 200, resp.text
    WeatherSchema.model_validate(resp.json())


@pytest.mark.asyncio
async def test_another_user_city_weather_get(client, token):
    filters = CityWeatherFiltersSchema(name=city2.name, time="12:23")
    resp = client.get(
        '/city/weather',
        params=filters.model_dump(),
        headers={"Authorization": token}
    )
    assert resp.status_code == 404, resp.text


@pytest.mark.asyncio
async def test_city_weather_get_specified_fields(client, token):
    filters = CityWeatherFiltersSchema(name=city1.name, time="12:23", weather_fields="temperature,humidity")
    resp = client.get(
        '/city/weather',
        params=filters.model_dump(),
        headers={"Authorization": token}
    )
    assert resp.status_code == 200, resp.text
    schema = WeatherSchema.model_validate(resp.json())
    assert (
        schema.temperature is not None \
        and schema.humidity is not None \
        and schema.wind_speed is None \
        and schema.pressure is None \
        and schema.rain is None
    ), "Some fields from response is unexpected: " + schema.model_dump_json()


@pytest.mark.asyncio
async def test_city_delete(client, token):
    resp = client.delete(
        '/city',
        params={"name": city1.name},
        headers={"Authorization": token}
    )
    assert resp.status_code == 204, resp.text


@pytest.mark.asyncio
async def test_city_is_deleted(client, token):
    resp = client.get(
        '/city',
        headers={"Authorization": token}
    )
    assert resp.status_code == 200, resp.text
    assert city1.name not in [i["name"] for i in resp.json()], "Deleted city founded in cities list"

