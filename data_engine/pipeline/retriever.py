import fastf1 as ff1
import pandas as pd
from fastf1.events import EventSchedule
import os
import logging

"""
Retrieve all telemetry data for each driver of each gp of each year.

"""


FORMAT = f"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(filename="etl_ingestion.log", level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

# Create a list to store data for each year
all_events = []


def get_rounds_number(schedule: EventSchedule) -> int:
    return schedule["RoundNumber"].max()


def save_retrieved_data(data: pd.DataFrame, data_type: str, year: int, gp_id: int):
    """save the data into a csv file

    Args:
        data (pd.DataFrame): _description_
        data_type (str): _description_
        year (int): the year of the data
        gp_id (int): the gp id of the data
    """
    logger.info(f"Saving {data_type} for year {year} and gp {gp_id}")
    path = f"retrieved_data/{year}/{gp_id}/"
    os.makedirs(path, exist_ok=True)
    data.to_csv(path + data_type + ".csv", index=False)


def fetch_data_for_year(year: int):
    """Load the events for a given year

    Args:
        year (int): year to fetch data for
    """
    schedule = ff1.get_event_schedule(year)
    logging.info(f"Fetched {get_rounds_number(schedule)} rounds for year {year}")
    for gp_id in range(1, get_rounds_number(schedule) + 1):
        quali = ff1.get_session(year=year, gp=gp_id, identifier="Q")
        try:
            quali.load(telemetry=True, weather=False)
            save_retrieved_data(quali.results, "quali_results", year, gp_id)
        except Exception as e:
            logger.exception(
                f"Error loading quali results for year {year} and gp {gp_id}: {e}"
            )

        race = ff1.get_session(year=year, gp=gp_id, identifier="R")
        try:
            race.load(telemetry=False, weather=False, livedata=False)
            save_retrieved_data(race.results, "race_results", year, gp_id)
        except Exception as e:
            logger.exception(
                f"Error loading race results for year {year} and gp {gp_id}: {e}"
            )


def main():
    # Define the range of years to get data
    years = range(2022, 2024)  # Update 2024 to current year as needed

    for year in years:
        # Load the events for a given year
        fetch_data_for_year(year)


if __name__ == "__main__":
    main()
