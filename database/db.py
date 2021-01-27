import datetime
from functools import wraps

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

engine = create_engine(
    "sqlite+pysqlite:///database/history.sqlite",
    connect_args={'check_same_thread': False},
    convert_unicode=True
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


class Patient(Base):
    __tablename__ = "patients"

    id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        sqlite_on_conflict_primary_key="REPLACE",
    )
    firstname = Column(String(32), nullable=False)
    lastname = Column(String(32), nullable=False)
    birthdate = Column(Integer, nullable=False)
    disabled = Column(Boolean, nullable=False)
    sensors = relationship("Sensors", backref="patients", lazy=False)

    def __init__(self, id=None, firstname=None, lastname=None,
                 birthdate=None, disabled=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.disabled = disabled

    def __repr__(self):
        return f"<Patient {self.firstname} {self.lastname}>"


class Sensors(Base):
    __tablename__ = "sensors"

    id = Column(Integer, nullable=False, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    L0_val = Column(Integer, nullable=False)
    L0_anom = Column(Boolean, nullable=False)
    L1_val = Column(Integer, nullable=False)
    L1_anom = Column(Boolean, nullable=False)
    L2_val = Column(Integer, nullable=False)
    L2_anom = Column(Boolean, nullable=False)
    R0_val = Column(Integer, nullable=False)
    R0_anom = Column(Boolean, nullable=False)
    R1_val = Column(Integer, nullable=False)
    R1_anom = Column(Boolean, nullable=False)
    R2_val = Column(Integer, nullable=False)
    R2_anom = Column(Boolean, nullable=False)
    measured_at = Column(DateTime, default=datetime.datetime.now)


def database_session(f):
    @wraps(f)
    def _use_session(*args, **kwargs):
        session = db_session()
        result = f(session, *args, **kwargs)
        db_session.remove()
        return result
    return _use_session


def init_db():
    Base.metadata.create_all(bind=engine)
