from pydantic import BaseModel


class CoordinatesSchema(BaseModel):
    longitude: float
    latitude: float

