from app.schemas.city import CitySchema
from app.schemas.weather import WeatherForDaySchema
from app.db.tables import City

from .base import BaseRepository

cities = []


class CityRepository(BaseRepository):
    base_table = City

    async def store(self, city: City):
        return await self._create(city)

    async def list(self, owner_id: int | None = None) -> list[City]:
        filters = {}
        if owner_id is not None:
            filters["owner_id"] = owner_id
        return list(await self._get_many(**filters))

    async def get(self, owner_id: int, name: str) -> City | None:
        return await self._get_one(owner_id=owner_id, name=name)

    async def delete(self, owner_id: int, name: str):
        model = await self._get_one(owner_id=owner_id, name=name)
        await self._delete_obj(model)

