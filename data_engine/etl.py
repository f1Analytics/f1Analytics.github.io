from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from base_tables import Driver, Lap

import pandas as pd


# Define your SQLAlchemy base
Base = declarative_base()

directory_of_this_file = Path(__file__).parent


def get_data_from_excel(filepath="drivers.xlsx"):
    df = pd.read_excel(directory_of_this_file / "etl_races" / filepath)
    return df


if __name__ == "__main__":
    # Your code goes here
    engine = create_engine("sqlite:///testf1.db", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    drivers_data = get_data_from_excel("drivers.xlsx")
    laps_data = get_data_from_excel("laps.xlsx")

    for driver in drivers_data.to_dict(orient="records"):
        session.add(Driver(**driver))

    for lap in laps_data.to_dict(orient="records"):
        session.add(Lap(**lap))

    session.commit()
