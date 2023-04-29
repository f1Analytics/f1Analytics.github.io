import argparse

from IPython.display import display, HTML
# display(HTML("<style>.container { width:100% !important; }</style>"))

import os
import numpy as np
import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from matplotlib import pyplot as plt
import plt_param

from utils import moving_average

# year = 2023
# gp = 'Bahrein' 


parser = argparse.ArgumentParser(
    prog='main',
    description='Analysis of the desired GP',
    epilog="Figures will be saved in the folder _assets/img/")

parser.add_argument('--year', type=int, nargs=1, default=2023, help='year of the gp')
parser.add_argument('--gp', type=int, nargs=1, default=2, help='name of the gp')
parser.add_argument('--drivers', nargs='*', help='drivers to analyze')

args = parser.parse_args()
print(args)

def export_figure(self, filename):
    date = datetime.date.today().strftime("%d-%m-%Y")
    path = f"../../reports/figures/{date}/"

    if os.path.exists(path):
        plt.savefig(path + filename + ".png", bbox_inches="tight")

    if not os.path.exists(path):
        os.makedirs(path)
        plt.savefig(path + filename + ".png", bbox_inches="tight")

    print(f"Successfully export {filename}")
    pass

def main(year:int = 2023, gp:int = 1, drivers:list = []):
    """main function

    Args:
        year (int): year
        gp (either int or str): gp name or gp number
    """
    
    session = ff1.get_session(year, gp, 'R')
    session.load()
    
    laps_rus = session.laps.pick_driver('RUS')
    laps_ham = session.laps.pick_driver('HAM')
    laps_lec = session.laps.pick_driver('LEC')
    laps_ver = session.laps.pick_driver('VER')
    laps_per = session.laps.pick_driver('PER')
    laps_alo = session.laps.pick_driver('ALO')

    laps = [laps_rus, laps_ham, laps_lec, laps_ver, laps_per, laps_alo]
    
    import datetime
    laps = [laps_rus, laps_ham, laps_lec, laps_ver, laps_per]
    laps = [laps_ham, laps_lec, laps_per, laps_alo]
    fig, ax = plt.subplots()

    plt.plot()
    ax = plt.gca()
    # ax.set_ylim([0,0.01])
    for i in laps:
        driver = i.head(1)['Driver'].values
        n_stints = max(i['Stint'].values)
        color = ff1.plotting.team_color(i['Team'].values[0])
        for s in range(n_stints):
            cond_stint = i['Stint'] == s+1    
            new_laps = i[cond_stint]
            cond_accurate = new_laps['IsAccurate'] == True
            # cond_accurate = i[cond_stint]['IsAccurate'] == True
            # tt_laps = new_laps[cond_accurate]['LapTime']
            tt_laps_values = new_laps[cond_accurate]['LapTime'].values
            tt_laps_interpolated = moving_average(tt_laps_values)
            # tt_laps_interpolated = tt_laps.rolling(7).mean().shift(-3)
            # tt_laps = [j if j<102056000000 else None for j in i['LapTime'].values]
            lap_number = new_laps[cond_accurate]['LapNumber']
            ax.plot(lap_number, tt_laps_values, '*', markersize=2, color=color)
            ax.plot(lap_number, tt_laps_interpolated, color=color)
            

    # ax.set_ylim([0.0010964484953703705, 0.0012])
    # ax.set_xlim([xmin, xmax])

    # Set title
    plt.title(f'Laps Evolution - {gp} {year}')
    plt.legend()

    # Save fig
    plt.savefig(f'laps_time_{gp}_{year}.png', dpi=300)

    # Load the session data
    race = ff1.get_session(year, circuit, 'R')
    laps = race.load_laps(with_telemetry=True)

    driver_stints = laps[['Driver', 'Stint', 'Compound', 'LapNumber']].groupby(
        ['Driver', 'Stint', 'Compound']
    ).count().reset_index()
    
        
    driver_stints = driver_stints.rename(columns={'LapNumber': 'StintLength'})

    driver_stints = driver_stints.sort_values(by=['Stint'])

    compound_colors = {
        'SOFT': '#FF3333',
        'MEDIUM': '#FFF200',
        'HARD': '#EBEBEB',
        'INTERMEDIATE': '#39B54A',
        'WET': '#00AEEF',
    }

    plt.rcParams["figure.figsize"] = [15, 10]
    plt.rcParams["figure.autolayout"] = True

    fig, ax = plt.subplots()

    for driver in race.results['Abbreviation']:
        stints = driver_stints.loc[driver_stints['Driver'] == driver]
        
        previous_stint_end = 0
        for _, stint in stints.iterrows():
            plt.barh(
                [driver], 
                stint['StintLength'], 
                left=previous_stint_end, 
                color=compound_colors[stint['Compound']], 
                edgecolor = "black"
            )
            
            previous_stint_end = previous_stint_end + stint['StintLength']
            
    # Set title
    plt.title(f'Race strategy - {gp} {year}')
            
    # Set x-label
    plt.xlabel('Lap')

    # Invert y-axis 
    plt.gca().invert_yaxis()

    # Remove frame from plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.savefig(f'strategy_{year}_{gp}.png', dpi=300)

    session_2023 = ff1.get_session(2023, gp, 'R')
    session_2023.load()

    lec_2023 = session_2023.laps.pick_driver('LEC')
    sai_2023 = session_2023.laps.pick_driver('SAI')

    session_2022 = ff1.get_session(2022, gp, 'R')
    session_2022.load()

    lec_2022 = session_2022.laps.pick_driver('LEC')
    sai_2022 = session_2022.laps.pick_driver('SAI')
    
    comparison_lec = [lec_2022, lec_2023]
    comparison_sai = [sai_2022, sai_2023]


    plt.plot()
    ax = plt.gca()
    n = 2022
    # ax.set_ylim([0,0.01])
    color = 'blue'
    for i in comparison_lec:
        driver = i.head(1)['Driver'].values
        n_stints = max(i['Stint'].values)
        for s in range(n_stints):
            cond_stint = i['Stint'] == s+1    
            new_laps = i[cond_stint]
            cond_accurate = new_laps['IsAccurate'] == True
            # cond_accurate = i[cond_stint]['IsAccurate'] == True
            # tt_laps = new_laps[cond_accurate]['LapTime']
            tt_laps_values = new_laps[cond_accurate]['LapTime'].values
            tt_laps_interpolated = moving_average(tt_laps_values)
            # tt_laps_interpolated = tt_laps.rolling(7).mean().shift(-3)
            # tt_laps = [j if j<102056000000 else None for j in i['LapTime'].values]
            lap_number = new_laps[cond_accurate]['LapNumber']
            ax.plot(lap_number, tt_laps_values, '*', markersize=2, label=n, color=color)
            ax.plot(lap_number, tt_laps_interpolated, color=color)
        n += 1
        color = ff1.plotting.team_color('Ferrari')
        

    # ax.set_ylim([0.0010964484953703705, 0.0012])
    # ax.set_xlim([xmin, xmax])

    # Set title
    plt.title(f'Laps Evolution - Leclerc')
    plt.legend()

    # Save fig
    plt.savefig(f'laps_time_comparison_leclerc_{gp}.png', dpi=300)

    plt.show()

    ax = plt.gca()
    # ax.set_ylim([0,0.01])
    n = 2022
    color = 'blue'
    for i in comparison_sai:
        driver = i.head(1)['Driver'].values
        n_stints = max(i['Stint'].values)
        for s in range(n_stints):
            cond_stint = i['Stint'] == s+1    
            new_laps = i[cond_stint]
            cond_accurate = new_laps['IsAccurate'] == True
            # cond_accurate = i[cond_stint]['IsAccurate'] == True
            # tt_laps = new_laps[cond_accurate]['LapTime']
            tt_laps_values = new_laps[cond_accurate]['LapTime'].values
            tt_laps_interpolated = moving_average(tt_laps_values)
            # tt_laps_interpolated = tt_laps.rolling(7).mean().shift(-3)
            # tt_laps = [j if j<102056000000 else None for j in i['LapTime'].values]
            lap_number = new_laps[cond_accurate]['LapNumber']
            ax.plot(lap_number, tt_laps_values, '*', markersize=2, label=n, color=color)
            ax.plot(lap_number, tt_laps_interpolated, color=color)
        color = ff1.plotting.team_color('Ferrari')
        n += 1
            

    # ax.set_ylim([0.0010964484953703705, 0.0012])
    # ax.set_xlim([xmin, xmax])

    # Set title
    plt.title(f'Laps Evolution - Sainz')
    plt.legend()

    # Save fig
    plt.savefig(f'laps_time_comparison_sainz_{gp}.png', dpi=300)

    return 

if __name__ == "__main__":
    year_ = args.year
    gp_ = args.gp
    drivers_ = args.driver
    main(year=year_, gp=gp_, drivers=drivers_)
