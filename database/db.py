import datetime
import logging
import sys

import pandas as pd
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Table, UniqueConstraint, create_engine)
from sqlalchemy.sql.schema import MetaData

logger = logging.getLogger('patients-monitor')
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(name)s - %(message)s')


class Database:

    def __init__(self, db_file):
        self.engine = create_engine(f'sqlite:///{db_file}')

    def create_tables(self):
        metadata = MetaData()
        patients = Table('patients', metadata,
                         Column('id', Integer, primary_key=True, nullable=False),
                         Column('name', String, nullable=False),
                         Column('surname', String, nullable=False),
                         Column('birthdate', Integer),
                         Column('disabled', Boolean, nullable=False),
                         UniqueConstraint('id'))
        sensors = Table('sensors', metadata,
                        Column('patient_id', Integer, ForeignKey('patients.id'), nullable=False),
                        Column('l0_val', Integer, nullable=False),
                        Column('l0_anom', Boolean, nullable=False),
                        Column('l1_val', Integer, nullable=False),
                        Column('l1_anom', Boolean, nullable=False),
                        Column('l2_val', Integer, nullable=False),
                        Column('l2_anom', Boolean, nullable=False),
                        Column('r0_val', Integer, nullable=False),
                        Column('r0_anom', Boolean, nullable=False),
                        Column('r1_val', Integer, nullable=False),
                        Column('r1_anom', Boolean, nullable=False),
                        Column('r2_val', Integer, nullable=False),
                        Column('r2_anom', Boolean, nullable=False),
                        Column('created_at', DateTime, default=datetime.datetime.now))
        try:
            metadata.create_all(self.engine)
        except Exception as e:
            logger.error("Error occurred during Table creation!")
            logger.error(e)

    def drop_tables(self):
        query = 'DROP TABLE IF EXISTS patients'
        self.execute_query(query)
        query = 'DROP TABLE IF EXISTS sensors'
        self.execute_query(query)

    def insert_patient(self, patient):
        query = "INSERT OR IGNORE INTO patients " \
                "(id, name, surname, birthdate, disabled) " \
                "VALUES " \
                f"({patient['ID']}, " \
                f"'{patient['Name']}', " \
                f"'{patient['Surname']}', " \
                f"{patient['Birthdate']}, " \
                f"{patient['Disabled']});"
        self.execute_query(query)

    def insert_sensors(self, sensors):
        query = "INSERT INTO sensors " \
                "(patient_id, l0_val, l0_anom, " \
                "l1_val, l1_anom, l2_val, " \
                "l2_anom, r0_val, r0_anom, " \
                "r1_val, r1_anom, r2_val, " \
                "r2_anom, created_at) " \
                "VALUES " \
                f"({sensors['Patient ID']}, " \
                f"{sensors['L0 value']}, " \
                f"{sensors['L0 anomaly']}, " \
                f"{sensors['L1 value']}, " \
                f"{sensors['L1 anomaly']}, " \
                f"{sensors['L2 value']}, " \
                f"{sensors['L2 anomaly']}, " \
                f"{sensors['R0 value']}, " \
                f"{sensors['R0 anomaly']}, " \
                f"{sensors['R1 value']}, " \
                f"{sensors['R1 anomaly']}, " \
                f"{sensors['R2 value']}, " \
                f"{sensors['R2 anomaly']}, " \
                f"'{sensors['Datetime']}');"
        self.execute_query(query)

    def drop_outdated_sensors_data(self, mins_limit):
        time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=mins_limit)
        drop_old_data = f"DELETE FROM sensors WHERE created_at < '{time_threshold}'"
        self.execute_query(drop_old_data)

    def fetch_patients_table(self):
        query = 'SELECT * FROM patients'
        with self.engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                logging.error(e)
            else:
                rows = result.fetchall()
                df = pd.DataFrame(rows, columns=['ID',
                                                 'Name',
                                                 'Surname',
                                                 'Birthdate',
                                                 'Disabled'])
                result.close()
        return df

    def fetch_patient_sensors(self, patient_id):
        query = 'SELECT * ' \
                'FROM sensors ' \
                f'WHERE patient_id = {patient_id} ' \
                'ORDER BY created_at DESC ' \
                'LIMIT 1 '
        with self.engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                logging.error(e)
            else:
                rows = result.fetchall()
                df = pd.DataFrame(rows, columns=['Patient ID',
                                                 'L0 value',
                                                 'L0 anomaly',
                                                 'L1 value',
                                                 'L1 anomaly',
                                                 'L2 value',
                                                 'L2 anomaly',
                                                 'R0 value',
                                                 'R0 anomaly',
                                                 'R1 value',
                                                 'R1 anomaly',
                                                 'R2 value',
                                                 'R2 anomaly',
                                                 'Datetime'])
                result.close()
        return df

    def fetch_all_patient_sensors(self, patient_id):
        query = f'SELECT * FROM sensors WHERE patient_id = {patient_id}'
        with self.engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                logging.error(e)
            else:
                rows = result.fetchall()
                df = pd.DataFrame(rows, columns=['Patient ID',
                                                 'L0 value',
                                                 'L0 anomaly',
                                                 'L1 value',
                                                 'L1 anomaly',
                                                 'L2 value',
                                                 'L2 anomaly',
                                                 'R0 value',
                                                 'R0 anomaly',
                                                 'R1 value',
                                                 'R1 anomaly',
                                                 'R2 value',
                                                 'R2 anomaly',
                                                 'Datetime'])
                result.close()
        return df

    def select_all_data(self, table, query=''):
        query = query if query != '' else f'SELECT * FROM {table}'
        with self.engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                logging.error(e)
            else:
                for row in result:
                    logger.info(row)
                result.close()

    def execute_query(self, query=''):
        if query == '':
            return
        with self.engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                logger.error(e)
