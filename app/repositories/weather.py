from aiohttp import ClientSession
import os


class WeatherRepository:
    BASE_URL = os.getenv("WEATHER_API_URL", "https://api.open-meteo.com")

    @classmethod
    def _weather_parameters(cls) -> str:
        return ','.join((
            'temperature_2m',
            'surface_pressure',
            'wind_speed_10m',
            'relative_humidity_2m',
            'rain'
        ))

    async def _get(self, **query_params) -> dict:
        async with ClientSession(self.BASE_URL) as session:
            async with session.get("/v1/forecast", params=query_params) as response:
                assert response.status == 200, "Invalid api response: " + (await response.text())
                return await response.json()

    async def get_by_coordinates(self, latitude: float, longitude: float) -> dict:
        return (
            await self._get(latitude=latitude, longitude=longitude, current=self._weather_parameters())
        )["current"]

    async def get_for_day(self, latitude: float, longitude: float) -> dict:
        return (
            await self._get(
                latitude=latitude,
                longitude=longitude,
                hourly=self._weather_parameters(),
                forecast_days=1
            )
        )["hourly"]

