import math

from app.models import Tank


def calculate_water_level(tank: Tank, device_level: str) -> dict:
    offset_from_capacity_height: float = float(device_level) - tank.freeboard
    if offset_from_capacity_height <= 0:
        # Tank is full
        return {'level': tank.capacity, 'percentage': 100}

    capacity_height = tank.capacity_height - offset_from_capacity_height
    provisional_volume = math.floor((math.pi * ((tank.diameter / 2) ** 2) * capacity_height) / 1000)
    real_volume = provisional_volume + tank.rounding_capacity
    percentage = math.floor((real_volume / tank.capacity) * 100)

    return {'level': real_volume, 'percentage': percentage}
