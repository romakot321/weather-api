from pydantic import BaseModel, Field, AliasChoices
import datetime as dt


class WeatherSchema(BaseModel):
    temperature: float | None = Field(default=None, alias=AliasChoices('temperature', 'temperature_2m'))
    humidity: float | None = Field(default=None, alias=AliasChoices('humidity', 'relative_humidity_2m'))
    wind_speed: float | None = Field(default=None, alias=AliasChoices('wind_speed', 'wind_speed_10m'))
    pressure: float | None = Field(default=None, alias=AliasChoices('pressure', 'surface_pressure'))
    rain: float | None = None


class WeatherForDaySchema(BaseModel):
    temperature: list[float] = Field(..., alias=AliasChoices('temperature', 'temperature_2m'))
    humidity: list[float] = Field(..., alias=AliasChoices('humidity', 'relative_humidity_2m'))
    wind_speed: list[float] = Field(..., alias=AliasChoices('wind_speed', 'wind_speed_10m'))
    rain: list[float]
    time: list[dt.datetime]

