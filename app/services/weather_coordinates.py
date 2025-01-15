import os
from fastapi import Depends

from app.repositories.weather import WeatherRepository
from app.schemas.coordinates import CoordinatesSchema
from app.schemas.weather import WeatherSchema


class WeatherCoordinatesService:
    def __init__(self, weather_repository: WeatherRepository = Depends()):
        self.weather_repository = weather_repository

    async def get(self, schema: CoordinatesSchema) -> WeatherSchema:
        data = await self.weather_repository.get_by_coordinates(
            schema.longitude, schema.latitude
        )
        return WeatherSchema.model_validate(data)

