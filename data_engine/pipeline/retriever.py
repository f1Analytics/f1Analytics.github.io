import fastf1 as ff1
import os

year, gp_id = 2024, 3


def save_retrieved_data(data, data_type, year, gp_id):
    path = f"retrieved_data/{year}/{gp_id}/"
    os.makedirs(path, exist_ok=True)
    data.to_csv(path + data_type + ".csv", index=False)


quali = ff1.get_session(year=year, gp=gp_id, identifier="Q")
quali.load(telemetry=True, weather=False)

save_retrieved_data(quali.results, "results", year, gp_id)

for driver in quali.drivers:
    abbr = quali.get_driver(driver)["Abbreviation"]
    telemetry = quali.laps.pick_driver("VER").pick_fastest().get_telemetry()
    save_retrieved_data(telemetry, f"telemetry_{abbr}", year, gp_id)

race = ff1.get_session(year=year, gp=gp_id, identifier="R")
race.load(telemetry=False, weather=False)

save_retrieved_data(race.laps, "racelaps", year, gp_id)
