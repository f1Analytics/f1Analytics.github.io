import os
import logging
import matplotlib.pyplot as plt

def get_fig_path(year: int, gp_id: int) -> str:
    return f"figures/{year}/{gp_id}/"

def save_plot(fig, year: int, gp_id: int, summary_filename: str) -> None:
    filepath = get_fig_path(year, gp_id)
    os.makedirs(filepath, exist_ok=True)
    fig.savefig(get_fig_path(year, gp_id) + summary_filename + ".png")
    logging.info(f"Figure saved at {filepath}tyre_summary.png")