import datetime
import logging
import sys
from time import sleep

import requests

from database.db import Database

logger = logging.getLogger('patients-monitor')
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(name)s - %(message)s')

DB_FILE = 'database/history.sqlite'
PATIENTS_MONITOR_URL = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/"
PATIENTS_ID_LIST = [
    '1', '2', '3',
    '4', '5', '6',
]


def get_patients_df():
    db = Database(DB_FILE)
    df = db.fetch_patients_table()
    return df


def get_all_patient_sensors(patient_id):
    db = Database(DB_FILE)
    df = db.fetch_all_patient_sensors(patient_id)
    return df


def get_patient_sensors(patient_id):
    db = Database(DB_FILE)
    df = db.fetch_patient_sensors(patient_id)
    return df


def store_all_patients_data(db):
    for patient_id in PATIENTS_ID_LIST:
        response = requests.get(PATIENTS_MONITOR_URL + patient_id)
        response = response.json()
        store_patient_data(db, response, patient_id)
        store_sensors_data(db, response, patient_id)


def store_patient_data(db, response, patient_id):
    patient = {}
    patient["ID"] = patient_id
    patient["Full Name"] = f"{response['firstname']} {response['lastname']}"
    patient["Name"] = response["firstname"]
    patient["Surname"] = response["lastname"]
    patient["Birthdate"] = response["birthdate"]
    patient["Disabled"] = response["disabled"]
    db.insert_patient(patient)


def store_sensors_data(db, response, patient_id):
    sensors = {}
    sensors['Patient ID'] = patient_id
    sensors_list = response["trace"]["sensors"]
    sensors["L0 value"] = sensors_list[0]["value"]
    sensors["L0 anomaly"] = sensors_list[0]["anomaly"]
    sensors["L1 value"] = sensors_list[1]["value"]
    sensors["L1 anomaly"] = sensors_list[1]["anomaly"]
    sensors["L2 value"] = sensors_list[2]["value"]
    sensors["L2 anomaly"] = sensors_list[2]["anomaly"]
    sensors["R0 value"] = sensors_list[3]["value"]
    sensors["R0 anomaly"] = sensors_list[3]["anomaly"]
    sensors["R1 value"] = sensors_list[4]["value"]
    sensors["R1 anomaly"] = sensors_list[4]["anomaly"]
    sensors["R2 value"] = sensors_list[5]["value"]
    sensors["R2 anomaly"] = sensors_list[5]["anomaly"]
    sensors['Datetime'] = datetime.datetime.now()
    db.insert_sensors(sensors)


if __name__ == '__main__':
    db = Database(DB_FILE)
    db.drop_tables()
    db.create_tables()
    while True:
        db.drop_outdated_sensors_data(10)
        store_all_patients_data(db)
        sleep(0.8)
