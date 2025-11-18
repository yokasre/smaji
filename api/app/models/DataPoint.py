from pydantic import BaseModel


class DataPoint(BaseModel):
    device_id: str
    temperature: str
    humidity: str
    battery: str
    timestamp: int
    level: str
