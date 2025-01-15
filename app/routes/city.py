from fastapi import APIRouter, Depends, Query

from app.services.weather_city import WeatherCityService
from app.schemas.weather import WeatherSchema
from app.schemas.city import CitySchema, CityWeatherFiltersSchema
from app.dependencies import get_current_user
from app.db.tables import User

router = APIRouter(prefix="/city", tags=["City"])


@router.get("/weather", response_model=WeatherSchema)
async def get_weather_by_city(
        schema: CityWeatherFiltersSchema = Depends(),
        service: WeatherCityService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.get(schema, user.id)


@router.post("", status_code=201)
async def add_city(
        schema: CitySchema,
        service: WeatherCityService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.add_city(schema, user.id)


@router.get("", response_model=list[CitySchema])
async def get_cities_list(
        service: WeatherCityService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.list_cities(user.id)


@router.delete("", status_code=204)
async def delete_city(
        name: str = Query(...),
        service: WeatherCityService = Depends(),
        user: User = Depends(get_current_user)
):
    await service.delete_city(name, user.id)

