import fire
from .main import GPBucket
from .utils import get_fig_path
import matplotlib.pyplot as plt
import os
import logging
logging.basicConfig(filename='cli_run.log', encoding='utf-8', level=logging.INFO)

def cli():
    return "Data Engine CLI"

def plot_position_changes(year, gp):
    pass

def minisector_comparison(year, gp):
    pass

def quali_comparison(year, gp):
    pass

def racelap_comparison(year, gp):
    pass

def sprint_race_comparison(year, gp):
    pass

def tyre_strategy(year, gp_id):
    bucket = GPBucket(year=year, gp_id=gp_id)
    tyre_summary = bucket.get_tyre_strategy_summary()
    filepath = get_fig_path(year, gp_id)
    os.makedirs(filepath, exist_ok=True)
    tyre_summary.savefig(filepath+"tyre_summary.png")
    logging.info(f"Figure saved at {filepath}tyre_summary.png")
    pass

if __name__ == "__main__":
    fire.Fire()