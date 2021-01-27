import asyncio
import datetime
import logging
import sys
from time import sleep

import aiohttp
import pandas as pd
from requests.exceptions import HTTPError

from database.db import Patient, Sensors, db_session, init_db

logger = logging.getLogger("patients-monitor")
logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(name)s - %(message)s"
)

PATIENTS_MONITOR_URL = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/"
PATIENTS_ID_LIST = [
    "1", "2", "3",
    "4", "5", "6",
]


def get_patients_df():
    patients = pd.read_sql_table(
        'patients',
        db_session.bind,
        index_col='id'
    )
    return patients


def get_all_patient_sensors(patient_id):
    sensors = pd.read_sql_query(
        db_session.query(Sensors).filter_by(patient_id=patient_id).statement,
        db_session.bind,
        index_col='id'
    )
    return sensors


def get_patient_sensors(patient_id):
    sensors = (db_session.query(Sensors).filter_by(patient_id=patient_id)
               .order_by(Sensors.measured_at.desc())
               .first())
    sensors = pd.Series(sensors)
    return sensors


def create_patient_object(response, patient_id):
    response["id"] = patient_id  # Fixing patient id

    patient = {}
    columns = Patient.metadata.tables["patients"].columns.keys()
    for c in columns:
        patient[c] = response[c]

    new_patient = Patient(**patient)
    return new_patient


def create_sensors_object(response, patient_id):
    sensors = {}
    sensors["patient_id"] = patient_id
    sensors_list = response["trace"]["sensors"]
    for sensor in sensors_list:
        sensors[f"{sensor['name']}_val"] = sensor["value"]
        sensors[f"{sensor['name']}_anom"] = sensor["anomaly"]

    new_sensors = Sensors(**sensors)
    return new_sensors


def drop_outdated(minutes=10):
    datetime_threshold = datetime.datetime.utcnow() - datetime.timedelta(
        minutes=minutes
    )
    db_session.query(Sensors).filter(
        Sensors.measured_at < datetime_threshold
    ).delete()
    db_session.commit()


async def get_patient_data_async(patient_id, session):
    url = PATIENTS_MONITOR_URL + patient_id
    try:
        response = await session.request(method="GET", url=url)
        response_json = await response.json()
        return response_json
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"An error ocurred: {err}")


async def fetch_patient_data(patient_id, session):
    try:
        response = await get_patient_data_async(patient_id, session)
    except Exception as err:
        logger.error(f"Exception occured: {err}")
        pass
    patient = create_patient_object(response, patient_id)
    return patient


async def fetch_sensors_data(patient_id, session):
    try:
        response = await get_patient_data_async(patient_id, session)
    except Exception as err:
        logger.error(f"Exception occured: {err}")
        pass
    sensors = create_sensors_object(response, patient_id)
    return sensors


async def store_all_patients_data():
    async with aiohttp.ClientSession() as session:
        while True:
            drop_outdated()

            patients = await asyncio.gather(
                *[
                    fetch_patient_data(patient_id, session)
                    for patient_id in PATIENTS_ID_LIST
                ]
            )
            sensors = await asyncio.gather(
                *[
                    fetch_sensors_data(patient_id, session)
                    for patient_id in PATIENTS_ID_LIST
                ]
            )

            db_session.add_all(patients)
            db_session.add_all(sensors)
            db_session.commit()
            sleep(0.9)


if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(store_all_patients_data())
