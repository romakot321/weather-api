from fastapi import Depends, HTTPException
from fastapi_utils.tasks import repeat_every
from loguru import logger
import asyncio

from app.repositories.weather import WeatherRepository
from app.repositories.city import CityRepository
from app.repositories.weather_city import WeatherCityRepository
from app.schemas.city import CitySchema, CityWeatherFiltersSchema
from app.schemas.weather import WeatherForDaySchema, WeatherSchema
from app.db.tables import City
from app.db.base import get_session


class WeatherCityService:
    def __init__(
            self,
            weather_repository: WeatherRepository = Depends(),
            city_repository: CityRepository = Depends(),
            weather_city_repository: WeatherCityRepository = Depends(),
    ):
        self.weather_repository = weather_repository
        self.city_repository = city_repository
        self.weather_city_repository = weather_city_repository

    async def get(self, schema: CityWeatherFiltersSchema, owner_id: int) -> WeatherSchema:
        weather = await self.weather_city_repository.get(str(owner_id) + ":" + schema.name, schema.time)
        if weather is None:
            raise HTTPException(404)
        weather_dict = {k: v for k, v in weather.model_dump().items() if k in schema.fields()}
        logger.debug(weather_dict)
        return WeatherSchema.model_validate(weather_dict)

    async def add_city(self, schema: CitySchema, owner_id: int):
        model = City(**schema.model_dump(), owner_id=owner_id)
        await self.city_repository.store(model)
        city_weather = await self.weather_repository.get_for_day(schema.longitude, schema.latitude)
        await self.weather_city_repository.store(
            str(owner_id) + ":" + schema.name,
            WeatherForDaySchema.model_validate(city_weather)
        )

    async def list_cities(self, owner_id: int) -> list[CitySchema]:
        models = await self.city_repository.list(owner_id=owner_id)
        return [
            CitySchema.model_validate(model)
            for model in models
        ]

    async def delete_city(self, name: str, owner_id: int):
        await self.city_repository.delete(owner_id, name)

    @classmethod
    async def update_cities_weather(cls):

        async def city_load_task(self, city: City):
            city_weather = await self.weather_repository.get_for_day(city.longitude, city.latitude)
            await self.weather_city_repository.store(
                str(city.owner_id) + ":" + city.name,
                WeatherForDaySchema.model_validate(city_weather)
            )

        session_getter = get_session()
        db_session = await anext(session_getter)
        self = cls(
            weather_repository=WeatherRepository(),
            city_repository=CityRepository(session=db_session),
            weather_city_repository=WeatherCityRepository()
        )
        cities = await self.city_repository.list()

        tasks = [city_load_task(self, city) for city in cities]
        await asyncio.gather(*tasks)

        logger.info("Loaded weather for " + str(len(tasks)) + " cities.")
