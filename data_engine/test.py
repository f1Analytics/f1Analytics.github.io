from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import logging
from pathlib import Path
import pandas as pd
import os

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a declarative base class
Base = declarative_base()


# class Circuit(Base):
#     __tablename__ = "circuits"

#     circuit_id = Column(String, primary_key=True)
#     circuit_name = Column(String)
#     location = Column(String)
#     country = Column(String)
#     races = relationship("Race", back_populates="circuit")


class RaceResult(Base):
    __tablename__ = "race_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    points = Column(Integer)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    constructor_id = Column(Integer, ForeignKey("constructors.id"), nullable=False)

    driver = relationship("Driver", back_populates="race_results")
    constructor = relationship("Constructor", back_populates="race_results")

    # circuit_id = Column(String, ForeignKey("circuits.circuit_id"))
    # circuit = relationship("Circuit", back_populates="races")
    # results = relationship("Result", back_populates="race")


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(String)
    driver_ref = Column(String)
    number = Column(Integer)
    code = Column(String)
    forename = Column(String)
    surname = Column(String)
    nationality = Column(String)
    dob = Column(DateTime)

    race_results = relationship("RaceResult", back_populates="driver")

    def __repr__(self):
        return (
            f"<Driver(driver_id={self.driver_id}, name={self.forename} {self.surname})>"
        )


class Constructor(Base):
    __tablename__ = "constructors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    constructor_id = Column(String)
    constructor_ref = Column(String)
    name = Column(String)
    nationality = Column(String)

    race_results = relationship("RaceResult", back_populates="constructor")

    def __repr__(self):
        return f"<Constructor(constructor_id={self.constructor_id}, name={self.name})>"


logging.basicConfig(filename="etl_ingestion.log", level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql+psycopg2://posgres:password@localhost:5432/f1db"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a metadata instance
metadata = MetaData()

# Bind the engine to the metadata
metadata.bind = engine

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create the database if it doesn't exist
Base.metadata.create_all(engine)


directory_of_this_file = Path(__file__).parent


def get_data_from_excel(filepath="drivers.xlsx"):
    logger.info("Fetching data from %s", filepath)
    df = pd.read_excel(directory_of_this_file / "etl_races" / filepath)
    logger.info("Data fetched from %s", filepath)
    return df


def main():
    logger.info("Starting the script")

    for year in range(2021, 2024):
        for round in [
            f
            for f in os.listdir(f"retrieved_data/{year}")
            if os.path.isdir(os.path.join(f"retrieved_data/{year}", f))
        ]:
            if not os.path.exists(f"retrieved_data/{year}/{round}/race_results.csv"):
                logger.warning(
                    f"Skipping year {year} and round {round}; file not found: `race_results.csv`"
                )
                continue
            drivers = []
            constructors = []
            results = []
            logger.info(f"Processing year {year} and round {round}")

            race_df = pd.read_csv(
                os.path.join(f"retrieved_data/{year}/{round}", "race_results.csv")
            )
            race_df.dropna(subset=["Position"], inplace=True)

            for _, row in race_df.iterrows():
                if (
                    result := session.query(RaceResult)
                    .filter_by(year=year, round=round, position=row["Position"])
                    .first()
                    is not None
                ):
                    continue
                # Check if the driver already exists in the database
                driver = (
                    session.query(Driver)
                    .filter_by(
                        driver_id=row["DriverId"],
                        forename=row["FirstName"],
                        surname=row["LastName"],
                    )
                    .first()
                )

                constructor = (
                    session.query(Constructor)
                    .filter_by(constructor_id=row["TeamId"])
                    .first()
                )

                if not constructor:
                    # If the constructor doesn't exist, create a new one
                    constructor = Constructor(
                        constructor_id=row["TeamId"],
                        name=row["TeamName"],
                    )
                    constructors.append(constructor)
                else:
                    logging.info(
                        f"Constructor {row['TeamName']} already exists in the database"
                    )

                if not driver:
                    # If the driver doesn't exist, create a new one
                    driver = Driver(
                        code=row["Abbreviation"],
                        driver_id=row["DriverId"],
                        number=row["DriverNumber"],
                        forename=row["FirstName"],
                        surname=row["LastName"],
                        nationality=row["CountryCode"],
                    )
                    drivers.append(driver)
                else:
                    logging.info(
                        f"Driver {row['LastName']} already exists in the database"
                    )

                result = RaceResult(
                    year=year,
                    round=round,
                    position=row["Position"],
                    points=row["Points"],
                    driver=driver,
                    constructor=constructor,
                )
                results.append(result)

            # Bulk save drivers and laps
            logger.info("Saving data to the database")
            session.bulk_save_objects(drivers)
            logger.info(f"{len(drivers)} drivers saved")
            session.bulk_save_objects(constructors)
            logger.info(f"{len(constructors)} constructors saved")
            session.bulk_save_objects(results)
            logger.info(f"{len(results)} results saved")

        # Commit changes to the database
        logger.info(f"Committing changes to the database for year {year}")
        session.commit()
        logger.info(f"Changes committed for year {year}")

    logger.info("Script ended successfully")


if __name__ == "__main__":
    main()
