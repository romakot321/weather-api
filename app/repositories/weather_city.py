from app.schemas.weather import WeatherForDaySchema, WeatherSchema
import datetime as dt

weather = {}


class WeatherCityRepository:
    def __init__(self):
        global weather
        self.cities_weather: dict[str, WeatherForDaySchema] = weather

    @classmethod
    def _find_time_index(cls, schema: WeatherForDaySchema, time: dt.time) -> int:
        for i, datetime in enumerate(schema.time):
            if datetime.time().hour == time.hour - 1:
                return i
        return 0

    async def store(self, city_name: str, schema: WeatherForDaySchema):
        self.cities_weather[city_name] = schema

    async def get(self, city_name: str, time: dt.time) -> WeatherSchema | None:
        schema = self.cities_weather.get(city_name)
        if schema is None:
            return None
        time_index = self._find_time_index(schema, time)
        return WeatherSchema(
            temperature=schema.temperature[time_index],
            wind_speed=schema.wind_speed[time_index],
            humidity=schema.humidity[time_index],
            rain=schema.rain[time_index]
        )
