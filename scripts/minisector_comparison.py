import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np
import pandas as pd
import sys
import os

# Enable the cache
ff1.Cache.enable_cache('cache/') 

# Setup plotting
plotting.setup_mpl()

# year, grand_prix, session = int(sys.argv[1]), sys.argv[2], 'Q'
year, grand_prix, session = int(sys.argv[1]), sys.argv[2], 'Q'

driver_1 = sys.argv[3]
driver_2 = sys.argv[4]

circuit = grand_prix.replace(" ", "_")
foldername = f"assets/img/{year}/{circuit}/"

if not os.path.exists(foldername):
    os.makedirs(foldername)
    
# Load the session data
quali = ff1.get_session(year, grand_prix, session)

# Get the laps
laps = quali.load_laps(with_telemetry=True)

# Select the laps from Hamilton and Verstappen
laps_ver = laps.pick_driver(driver_1)
laps_ham = laps.pick_driver(driver_2)

# Get the telemetry data from their fastest lap
fastest_ver = laps_ver.pick_fastest().get_telemetry().add_distance()
fastest_ham = laps_ham.pick_fastest().get_telemetry().add_distance()

# Since the telemetry data does not have a variable that indicates the driver, 
# we need to create that column
fastest_ver['Driver'] = driver_1
fastest_ham['Driver'] = driver_2

# Merge both lap telemetries so we have everything in one DataFrame
telemetry = fastest_ver.append(fastest_ham)

# We want 25 mini-sectors (this can be adjusted up and down)
num_minisectors = 55

# Grab the maximum value of distance that is known in the telemetry
total_distance = total_distance = max(telemetry['Distance'])

# Generate equally sized mini-sectors 
minisector_length = total_distance / num_minisectors

# Initiate minisector variable, with 0 (meters) as a starting point.
minisectors = [0]

# Add multiples of minisector_length to the minisectors
for i in range(0, (num_minisectors - 1)):
    minisectors.append(minisector_length * (i + 1))
    
telemetry['Minisector'] = telemetry['Distance'].apply(
    lambda dist: (
        int((dist // minisector_length) + 1)
    )
)

# Calculate avg. speed per driver per mini sector
average_speed = telemetry.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()

# Select the driver with the highest average speed
fastest_driver = average_speed.loc[average_speed.groupby(['Minisector'])['Speed'].idxmax()]

# Get rid of the speed column and rename the driver column
fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})

# Join the fastest driver per minisector with the full telemetry
telemetry = telemetry.merge(fastest_driver, on=['Minisector'])

# Order the data by distance to make matploblib does not get confused
telemetry = telemetry.sort_values(by=['Distance'])

# Convert driver name to integer
telemetry.loc[telemetry['Fastest_driver'] == driver_1, 'Fastest_driver_int'] = 1
telemetry.loc[telemetry['Fastest_driver'] == driver_2, 'Fastest_driver_int'] = 2

x = np.array(telemetry['X'].values)
y = np.array(telemetry['Y'].values)

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
fastest_driver_array = telemetry['Fastest_driver_int'].to_numpy().astype(float)

#custom cmap
# cmap = cm.get_cmap('winter', 2)

team_ham = laps_ham['Team'].to_list()[0]
team_ver = laps_ver['Team'].to_list()[0]

# team_ver

color_ham = ff1.plotting.team_color(team_ham)
color_ver = ff1.plotting.team_color(team_ver)

from matplotlib import colors

cmap = colors.ListedColormap([color_ham, color_ver])

lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
lc_comp.set_array(fastest_driver_array)
lc_comp.set_linewidth(5)

plt.rcParams['figure.figsize'] = [18, 10]

plt.gca().add_collection(lc_comp)
plt.axis('equal')
plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

# cbar = plt.colorbar(mappable=lc_comp, boundaries=np.arange(1,4))
cbar = plt.colorbar(mappable=lc_comp, boundaries=np.arange(1,4))

# cbar.set_ticks(np.arange(1.5, 9.5))
# np.arange(1.5, 9.5)
# cbar.set_ticks([1.5, 9.5])
cbar.set_ticklabels([driver_1, driver_2])

#cbar.set_ticklabels([driver_1, driver_2])

plt.title(f"{circuit} GP | {driver_1} vs {driver_2} \n Minisector comparison")
plt.savefig(f"{foldername}{circuit}_{driver_1}_{driver_2}_{session}.png", dpi=300)
