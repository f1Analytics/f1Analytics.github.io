from .fetcher import Fetcher
import matplotlib.pyplot as plt

import fastf1 as ff1
import fastf1.plotting
fastf1.plotting.setup_mpl(misc_mpl_mods=False)
  
class EngineBucket:
    _COMPOUND_COLORS = {
        'SOFT': '#FF3333',
        'MEDIUM': '#FFF200',
        'HARD': '#EBEBEB',
        'INTERMEDIATE': '#39B54A',
        'WET': '#00AEEF',
        'UNKNOWN': '#000000'}
    
    def __init__(self, gp_id, year):
        self.gp_id = gp_id
        self.year = year
        self.fetcher = Fetcher()
        
class GPBucket(EngineBucket):
    def __init__(self, gp_id, year):
        super().__init__(gp_id, year)
        self._processor = None
        self._set_static_data()
        
        # processing data
        self.race_laps = None   
    
    @property
    def processor(self):
        if self._processor is None:
            from .processor import Processor
            self._processor = Processor(bucket=self)
        return self._processor
    
    def _set_static_data(self):
        self.data = self.fetcher.fetch_static_data()
        self.gp_name = ""
         
    def get_tyre_strategy_summary(self):
        fig = self.processor.create_tyre_strategy_summary()
        return fig
    
    def get_race_data(self, year:int=None, gp_id:int=None):
        if year is None:
            year = self.year
        if gp_id is None:
            gp_id = self.gp_id
        session = ff1.get_session(year=year, gp=gp_id, identifier='R')
        session.load()
        return session
        
    def get_race_laps_data(self, race=None):
        if self.race_laps is None:
            if race is None:
                race = self.get_race_data()
            self.race_laps = race.laps
        return self.race_laps
    
if __name__ == "__main__":
    bucket = GPBucket(year=2024, gp_id=2)
    fig = bucket.get_tyre_strategy_summary()
    fig.savefig("tyre_summary.png")