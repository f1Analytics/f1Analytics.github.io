import fastf1 as ff1
import matplotlib.pyplot as plt
from .main import GPBucket
class Processor:
    def __init__(self, bucket):
        self.bucket: GPBucket = bucket
    
    def create_tyre_strategy_summary(self):

        race = self.bucket.get_race_data()
        laps_data = race.laps
        drivers = race.drivers
        drivers = [race.get_driver(driver)["Abbreviation"] for driver in drivers]
        
        driver_stints = laps_data[['Driver', 'Stint', 'Compound', 'LapNumber']].groupby(
            ['Driver', 'Stint', 'Compound']
        ).count().reset_index()

        driver_stints = driver_stints.rename(columns={'LapNumber': 'StintLength'})
        driver_stints = driver_stints.sort_values(by=['Stint'])

        plt.rcParams["figure.figsize"] = [15, 10]
        plt.rcParams["figure.autolayout"] = True

        fig, ax = plt.subplots()

        for driver in drivers:
            stints = driver_stints.loc[driver_stints['Driver'] == driver]
            
            previous_stint_end = 0
            for _, stint in stints.iterrows():
                plt.barh(
                    y=driver,
                    width=stint["StintLength"],
                    left=previous_stint_end,
                    color=self.bucket._COMPOUND_COLORS[stint["Compound"]],
                    edgecolor="black",
                    fill=True
                )

                previous_stint_end += stint["StintLength"]              
        
        plt.title(f'Tyre strategy - {self.bucket.year} {self.bucket.gp_id}')
        plt.xlabel("Lap Number")
        plt.grid(False)
        # invert the y-axis so drivers that finish higher are closer to the top
        ax.invert_yaxis()

        # Remove frame from plot
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        return fig