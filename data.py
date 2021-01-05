import aiohttp
import asyncio
import sys
from requests.exceptions import HTTPError
import logging
import pandas as pd

logger = logging.getLogger('patients-monitor')
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(name)s - %(message)s')


PATIENTS_MONITOR_URL = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/"
PATIENTS_ID_LIST = [
    '1', '2', '3',
    '4', '5', '6',
]


def parse_patient_info(response, patient_id):
    patient = {}
    patient["ID"] = patient_id
    patient["Full Name"] = f"{response['firstname']} {response['lastname']}"
    patient["Name"] = response["firstname"]
    patient["Surname"] = response["lastname"]
    patient["Birthdate"] = response["birthdate"]
    patient["Disabled"] = response["disabled"]
    return patient


async def get_patient_details_async(patient_id, session):
    url = PATIENTS_MONITOR_URL + patient_id
    try:
        response = await session.request(method='GET', url=url)
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"An error ocurred: {err}")
    response_json = await response.json()
    return response_json


async def run_program(patient_id, session):
    try:
        response = await get_patient_details_async(patient_id, session)
        patients_df = parse_patient_info(response, patient_id)
    except Exception as err:
        logger.error(f"Exception occured: {err}")
    return patients_df


async def get_patients_df():
    async with aiohttp.ClientSession() as session:
        patients = await asyncio.gather(*[run_program(patient_id, session) for patient_id in PATIENTS_ID_LIST])
        patients_df = pd.DataFrame(patients)
        patients_df = patients_df.sort_values(by=['ID'], ignore_index=True)
        return patients_df


def get_patients_df_async():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    patients_df = loop.run_until_complete(get_patients_df())
    loop.close()
    return patients_df


if __name__ == '__main__':
    df = get_patients_df_async()
    print(df)
