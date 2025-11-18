from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Tank(SQLModel, table=True):
    __tablename__ = "tanks"

    id: int | None = Field(primary_key=True, default=None)
    organization_id: int = Field(foreign_key="organizations.id", index=True)
    tank_number: int
    capacity: int
    latitude: float
    longitude: float
    diameter: float
    capacity_height: float
    freeboard: float
    rounding_capacity: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(default=None)

    organization: "Organization" = Relationship(back_populates="tanks")
    sensor_device: Optional["SensorDevice"] = Relationship(back_populates="tank")
