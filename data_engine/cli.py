from pathlib import Path
import fire
from main import GPBucket
from utils import *
import matplotlib.pyplot as plt
import os
import logging

logging.basicConfig(filename='cli_run.log', encoding='utf-8', level=logging.INFO)

directory_of_this_file = Path(__file__).parent

def cli():
    return "Data Engine CLI"

def plot_position_changes(year, gp):
    pass

def minisector_comparison(year, gp):
    pass

def quali_comparison(year, gp_id, driver_1: str=None, driver_2: str=None, plot_size=(20, 10)):
    bucket = GPBucket(year=year, gp_id=gp_id)
    if driver_1 is None:
        driver_1 = bucket.get_quali_positions(year, gp_id, pos=1)
    if driver_2 is None:
        driver_2 = bucket.get_quali_positions(year, gp_id, pos=2)
    quali_comparison = bucket.get_quali_comparison(driver_1=driver_1, driver_2=driver_2)
    save_plot(quali_comparison, year, gp_id, f"quali_comparison_{driver_1}_{driver_2}.png")
    pass

def racelap_comparison(year, gp):
    pass

def sprint_race_comparison(year, gp):
    pass

def tyre_strategy(year, gp_id):
    bucket = GPBucket(year=year, gp_id=gp_id)
    tyre_summary = bucket.get_tyre_strategy_summary()
    save_plot(tyre_summary, year, gp_id, "tyre_summary.png")
    pass

if __name__ == "__main__":
    fire.Fire()