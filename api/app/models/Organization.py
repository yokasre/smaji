from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Organization(SQLModel, table=True):
    __tablename__ = "organizations"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    address: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)

    tanks: list["Tank"] = Relationship(back_populates="organization")
    sensor_devices: list["SensorDevice"] = Relationship(back_populates="organization")
