import fastf1
import pandas as pd
import matplotlib.pyplot as plt
from fastf1 import plotting

# Enable cache
fastf1.Cache.enable_cache('cache')

# Load the race session
print("Loading 2023 Abu Dhabi GP race session...")
session = fastf1.get_session(2023, 22, 'R')
session.load()

# Get the race results
results = session.results
print("\nRace Results:")
print(pd.DataFrame(results)[['DriverNumber', 'BroadcastName', 'Position', 'Points', 'Status']])

# Get all laps
laps = session.laps
print("\nFastest Laps:")
fastest_laps = laps.groupby('Driver')['LapTime'].min().sort_values()
print(fastest_laps)

# Get tire strategies
print("\nTire Strategies:")
tire_strategies = laps.groupby('Driver')['Compound'].value_counts()
print(tire_strategies)

# Plot position changes
print("\nPlotting position changes...")
fig, ax = plt.subplots(figsize=(15, 10))
for driver in session.drivers:
    driver_laps = laps.pick_drivers(driver)
    ax.plot(driver_laps['LapNumber'], driver_laps['Position'], 
            label=driver_laps['Driver'].iloc[0])
ax.set_xlabel('Lap Number')
ax.set_ylabel('Position')
ax.set_title('Position Changes During Race')
ax.invert_yaxis()  # Invert y-axis so P1 is at the top
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('position_changes.png')
print("Position changes plot saved as 'position_changes.png'")

# Plot lap times
print("\nPlotting lap times...")
fig, ax = plt.subplots(figsize=(15, 10))
for driver in session.drivers:
    driver_laps = laps.pick_drivers(driver)
    ax.plot(driver_laps['LapNumber'], driver_laps['LapTime'], 
            label=driver_laps['Driver'].iloc[0])
ax.set_xlabel('Lap Number')
ax.set_ylabel('Lap Time')
ax.set_title('Lap Times During Race')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('lap_times.png')
print("Lap times plot saved as 'lap_times.png'")

# Print some interesting statistics
print("\nRace Statistics:")
print(f"Total Laps: {session.total_laps}")

# Get fastest lap information
fastest_lap = laps.loc[laps['LapTime'].idxmin()]
print(f"Fastest Lap: {fastest_lap['LapTime']} by {fastest_lap['Driver']} on lap {fastest_lap['LapNumber']}")

# Calculate average lap time (excluding in/out laps and slow laps)
quick_laps = laps.pick_quicklaps()
print(f"Average Lap Time (quick laps only): {quick_laps['LapTime'].mean()}")
print(f"Number of DNFs: {len(results[results['Status'] != 'Finished'])}")

# Get pit stop information
print("\nPit Stop Summary:")
pit_stops = laps[laps['PitInTime'].notna()].groupby('Driver').size()
print("Number of pit stops per driver:")
print(pit_stops)

# Get sector times
print("\nSector Times Analysis:")
sector_times = laps.groupby('Driver')[['Sector1Time', 'Sector2Time', 'Sector3Time']].min()
print("Best sector times per driver:")
print(sector_times)

# Get position changes
print("\nPosition Changes:")
start_positions = laps[laps['LapNumber'] == 1].set_index('Driver')['Position']
end_positions = laps[laps['LapNumber'] == session.total_laps].set_index('Driver')['Position']
position_changes = start_positions - end_positions
print("Position changes from start to finish:")
print(position_changes.sort_values(ascending=False)) 