from pydantic import BaseModel, field_validator, Field, ConfigDict
from enum import Enum
import datetime as dt


class WeatherFields(Enum):
    temperature = "temperature"
    humidity = 'humidity'
    wind_speed = "wind_speed"
    rain = "rain"


class CitySchema(BaseModel):
    latitude: float
    longitude: float
    name: str

    model_config = ConfigDict(from_attributes=True)


class CityWeatherFiltersSchema(BaseModel):
    name: str
    time: dt.time
    weather_fields: str = Field(
        default="temperature,humidity,wind_speed,rain"
    )

    @field_validator('weather_fields')
    @classmethod
    def validate_weather_fields(cls, value):
        if not isinstance(value, str):
            raise ValueError("Invalid weather_fields type")
        fields = value.split(',')
        for field in fields:
            if field not in list(map(lambda i: i.value, list(WeatherFields))):
                raise ValueError("Invalid field in weather_fields: " + field)
        return value

    def fields(self):
        return self.weather_fields.split(',')
