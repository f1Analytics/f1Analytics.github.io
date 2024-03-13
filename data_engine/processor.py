import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils

import matplotlib.pyplot as plt
from main import GPBucket
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
    
    def create_best_lap_comparison_summary(self, driver_1: str=None, driver_2: str=None):
        quali = self.bucket.quali
        laps_driver_1 = quali.laps.pick_driver(driver_1)
        laps_driver_2 = quali.laps.pick_driver(driver_2)
        
        # Select the fastest lap
        fastest_driver_1 = laps_driver_1.pick_fastest()
        fastest_driver_2 = laps_driver_2.pick_fastest()
                
        # Retrieve the telemetry and add the distance column
        telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
        telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()

        # Make sure whe know the team name for coloring
        team_driver_1 = fastest_driver_1['Team']
        team_driver_2 = fastest_driver_2['Team']
       
        # Extract the delta time
        delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)

        plot_size = [15, 15]
        plot_title = f"{quali.event.year} {quali.event.EventName} - {quali.name} - {driver_1} vs {driver_2}"
        plot_ratios = [1, 4, 2, 1, 2]
        plot_filename = plot_title.replace(" ", "_") + ".png"

        # Make plot a bit bigger
        plt.rcParams['figure.figsize'] = plot_size

        # Create subplots with different sizes
        fig, ax = plt.subplots(5, gridspec_kw={'height_ratios': plot_ratios})

        # Set the plot title
        ax[0].set_title(plot_title, fontsize=25)


        # Delta line
        ax[0].plot(ref_tel['Distance'], delta_time)
        ax[0].axhline(0)
        ax[0].set(ylabel=f"Gap to {driver_2} (s)")

        # Speed trace
        ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], label=driver_1, color=ff1.plotting.team_color(team_driver_1))
        ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], label=driver_2, color=ff1.plotting.team_color(team_driver_2))
        ax[1].set(ylabel='Speed')
        ax[1].legend(loc="lower right")

        # Throttle trace
        ax[2].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Throttle'], label=driver_1, color=ff1.plotting.team_color(team_driver_1))
        ax[2].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Throttle'], label=driver_2, color=ff1.plotting.team_color(team_driver_2))
        ax[2].set(ylabel='Throttle')

        # # Brake trace
        # ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Brake'], label=driver_1, color=ff1.plotting.team_color(team_driver_1))
        # ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Brake'], label=driver_2, color=ff1.plotting.team_color(team_driver_2))
        # ax[3].set(ylabel='Brake')

        # Gear trace
        ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['nGear'], label=driver_1, color=ff1.plotting.team_color(team_driver_1))
        ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['nGear'], label=driver_2, color=ff1.plotting.team_color(team_driver_2))
        ax[3].set(ylabel='Gear')

        # RPM trace
        ax[4].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], label=driver_1, color=ff1.plotting.team_color(team_driver_1))
        ax[4].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], label=driver_2, color=ff1.plotting.team_color(team_driver_2))
        ax[4].set(ylabel='RPM')


        # # DRS trace
        # ax[6].plot(telemetry_driver_1['Distance'], telemetry_driver_1['DRS'], label=driver_1, color=ff1.plotting.team_color(team_driver_1))
        # ax[6].plot(telemetry_driver_2['Distance'], telemetry_driver_2['DRS'], label=driver_2, color=ff1.plotting.team_color(team_driver_2))
        # ax[6].set(ylabel='DRS')
        # ax[6].set(xlabel='Lap distance (meters)')


        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for a in ax.flat:
            a.label_outer()
    
        return fig