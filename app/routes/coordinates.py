from fastapi import APIRouter, Depends

from app.schemas.coordinates import CoordinatesSchema
from app.schemas.weather import WeatherSchema
from app.services.weather_coordinates import WeatherCoordinatesService

router = APIRouter(prefix="/coordinates", tags=["Coordinates"])


@router.get("/weather", response_model=WeatherSchema)
async def get_weather_by_coordinates(
        schema: CoordinatesSchema = Depends(),
        service: WeatherCoordinatesService = Depends()
):
    return await service.get(schema)

