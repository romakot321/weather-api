import pytest

from app.schemas.weather import WeatherSchema
from app.schemas.coordinates import CoordinatesSchema


@pytest.mark.asyncio
async def test_get_by_coordinates(client):
    resp = client.get(
        '/coordinates/weather',
        params=CoordinatesSchema(latitude=0.01, longitude=0.01).model_dump()
    )
    assert resp.status_code == 200
    WeatherSchema.model_validate(resp.json())

