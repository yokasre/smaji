from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class SensorDevice(SQLModel, table=True):
    __tablename__ = "sensor_devices"

    id: int | None = Field(primary_key=True, default=None)
    organization_id: int = Field(foreign_key="organizations.id")
    tank_id: int | None = Field(foreign_key="tanks.id", index=True, unique=True)
    device_id: str = Field(max_length=255, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(default=None)

    organization: "Organization" = Relationship(back_populates="sensor_devices")
    tank: Optional["Tank"] = Relationship(back_populates="sensor_device")
