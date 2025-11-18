from fastapi import FastAPI, status, Request, Depends
from contextlib import asynccontextmanager

from sqlmodel import Session, select
from starlette.responses import JSONResponse

from app.db.mongodb import open_mongodb_connection, close_mongodb_connection, get_mongo_db
from app.db.postgres import open_postgres_connection, close_postgres_connection, get_db
from app.models import DataPoint, Tank
from app.services.analytics_service import calculate_water_level
from app.services.device_data_service import seed_sensor_data, get_last_data_point
from app.services.general_store_service import seed_organization_data
from app.tasks.scheduled_tasks import calculate_and_send_yesterday_usage


@asynccontextmanager
async def lifespan(app: FastAPI):
    open_mongodb_connection()
    open_postgres_connection()

    seed_organization_data()
    seed_sensor_data()

    yield

    close_postgres_connection()
    close_mongodb_connection()


app = FastAPI(lifespan=lifespan)


# Heartbeat
@app.get("/")
def ping():
    return {"message": "Smaji API is running."}


@app.get("/trigger-bg-task")
def trigger():
    calculate_and_send_yesterday_usage.delay()
    return {"message": "Task queued"}


@app.post("/datapoints/add", status_code=status.HTTP_201_CREATED)
def add_data_point(data_point: DataPoint):
    """
    Simulates adding a data point to the database.
    """
    try:
        data_point_dict = data_point.model_dump()

        db = get_mongo_db()
        collection = db["device_data"]
        collection.insert_one(data_point_dict)

        return {"message": "Data point added successfully."}
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error was encountered while processing request"})


@app.get("/analytics/get-current-water-level", status_code=status.HTTP_200_OK)
def get_current_water_level(tank_number: str, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Calculates current water level of a particular tank.
    """
    try:
        tank_number: int = int(tank_number)
        statement = select(Tank).where(Tank.tank_number == tank_number)
        tank = db.exec(statement).first()
        if tank is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "We did not find a tank with the specified tank number."})
        else:
            device_id: str = tank.sensor_device.device_id
            data_point = get_last_data_point(device_id)
            water_level: dict = calculate_water_level(tank, data_point['level'])
            return JSONResponse(status_code=status.HTTP_200_OK, content=water_level)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error was encountered while processing request", "log": str(e)})
