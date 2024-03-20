from abc import ABC, abstractmethod
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import pandas as pd


# Define your SQLAlchemy base
Base = declarative_base()

directory_of_this_file = Path(__file__).parent


def get_data_from_excel(filepath="drivers.xlsx"):
    df = pd.read_excel(directory_of_this_file / "etl_races" / filepath)
    return df


class F1Base(Base, ABC):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    _identification_keys = []

    @abstractmethod
    def check_if_it_exists(self):
        raise NotImplementedError


class Driver(Base):
    __tablename__ = "drivers"

    name = Column(String)
    abbr = Column(String)

    laps = relationship("Lap", back_populates="driver")

    _identification_fields = []


class Lap(Base):
    __tablename__ = "laps"

    lap_number = Column(Integer)
    driver_id = Column(Integer, ForeignKey("drivers.id"))

    driver = relationship("Driver", back_populates="laps")

    _identification_fields = []


def get_drivers_cleaned_data():
    drivers_data = get_data_from_excel("drivers.xlsx")

    driver_interesting_columns = [
        "DriverNumber",
        "BroadcastName",
        "Abbreviation",
        "DriverId",
        "TeamName",
        "TeamColor",
        "TeamId",
        "FirstName",
        "LastName",
        "FullName",
        "CountryCode",
    ]
    return drivers_data[driver_interesting_columns]


def get_laps_cleaned_data():
    data = get_data_from_excel("laps.xlsx")

    laps_interesting_columns = [
        "Time",
        "DriverNumber",
        "LapTime",
        "LapNumber",
        "Stint",
        "PitOutTime",
        "PitInTime",
        "Compound",
        "TyreLife",
        "LapStartTime",
        "LapStartDate",
        "TrackStatus",
        "Position",
        "Deleted",
        "IsAccurate",
    ]

    return data[laps_interesting_columns]


if __name__ == "__main__":
    engine = create_engine("sqlite:///testf1.db", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    drivers_data = get_drivers_cleaned_data()
    laps_data = get_laps_cleaned_data()

    merged_df = pd.merge(
        left=laps_data,
        right=drivers_data,
        on="DriverNumber",
        how="left",
    )

    drivers = []
    laps = []

    for _, row in merged_df.iterrows():
        driver_abbr = row["Abbreviation"]

        # Check if the driver already exists in the database
        driver = session.query(Driver).filter_by(abbr=driver_abbr).first()

        if not driver:
            driver_abbrs = [driver.abbr for driver in drivers]
            if driver_abbr not in driver_abbrs:
                # If the driver doesn't exist, create a new one
                driver = Driver(name=row["FullName"], abbr=driver_abbr)
                drivers.append(driver)
            else:
                driver = [driver for driver in drivers if driver.abbr == driver_abbr][0]

    # Add the lap to the driver's laps
    laps.append(
        Lap(
            lap_number=row["LapNumber"],
            driver=driver,
        )
    )

    # Bulk save drivers and laps
    session.bulk_save_objects(drivers)
    session.bulk_save_objects(laps)

    # Commit changes to the database
    session.commit()
