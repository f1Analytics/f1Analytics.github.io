from pathlib import Path
from fetcher import Fetcher
import matplotlib.pyplot as plt

import fastf1 as ff1
import fastf1.plotting

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

directory_of_this_file = Path(__file__).parent
ff1.Cache.enable_cache(directory_of_this_file / "cache/")


class EngineBucket:
    _COMPOUND_COLORS = {
        "SOFT": "#FF3333",
        "MEDIUM": "#FFF200",
        "HARD": "#EBEBEB",
        "INTERMEDIATE": "#39B54A",
        "WET": "#00AEEF",
        "UNKNOWN": "#000000",
    }

    def __init__(self, gp_id, year):
        self.gp_id = gp_id
        self.year = year
        self.fetcher = Fetcher()


class GPBucket(EngineBucket):
    def __init__(self, gp_id, year):
        super().__init__(gp_id, year)
        self.quali = None
        self.race = None

        self._processor = None

        self._set_gp_info()
        self._set_static_data()

        # processing data
        self.race_laps = None

    @property
    def processor(self):
        if self._processor is None:
            from processor import Processor

            self._processor = Processor(bucket=self)
        return self._processor

    def _set_static_data(self):
        self.data = self.fetcher.fetch_static_data()
        self.gp_name = ""

    def _set_gp_info(self):
        ff1.get_session()
        self.quali = ff1.get_session(self.year, self.gp_id, "Q")
        self.quali.load()
        self.race = ff1.get_session(self.year, self.gp_id, "R")
        self.race.load()

    def get_tyre_strategy_summary(self):
        fig = self.processor.create_tyre_strategy_summary()
        return fig

    def get_quali_comparison(self, driver_1, driver_2):
        fig = self.processor.create_best_lap_comparison_summary(driver_1, driver_2)
        return fig

    def get_race_data(self, year: int = None, gp_id: int = None):
        return self.race

    def get_race_laps_data(self, race=None):
        if self.race_laps is None:
            if race is None:
                race = self.race
            self.race_laps = race.laps
        return self.race_laps


if __name__ == "__main__":
    bucket = GPBucket(year=2024, gp_id=2)
    fig = bucket.get_quali_comparison("VER", "LEC")
    fig.savefig("quali_comparison.png")
