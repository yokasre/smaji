from sqlmodel import Session, delete

from app.db.postgres import get_engine
from app.models import Organization, Tank, SensorDevice


def seed_organization_data() -> None:
    """
    Seeds organization and tank data into database
    """

    engine = get_engine()
    with Session(engine) as session:
        try:
            session.exec(delete(SensorDevice))
            session.exec(delete(Tank))
            session.exec(delete(Organization))

            organization: Organization = Organization(name="Nairobi Water Project", address="Nairobi, Kenya")
            session.add(organization)
            session.flush()

            tank: Tank = Tank(organization_id=organization.id, tank_number=10, capacity=5000, latitude=-1.312629, longitude=36.825813, diameter=172, capacity_height=215, freeboard=30, rounding_capacity=5)
            session.add(tank)
            session.flush()

            sensor_device: SensorDevice = SensorDevice(organization_id=organization.id, tank_id=tank.id, device_id="100200300400500")
            session.add(sensor_device)

            session.commit()

            print("Organization data seeded successfully.")
        except Exception as e:
            session.rollback()
            print("Organization data failed to seed.")
            raise
