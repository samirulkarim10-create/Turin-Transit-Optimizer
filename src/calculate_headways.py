import pandas as pd

def time_to_seconds(time_str):
    """Converts a GTFS time string (HH:MM:SS) to total seconds past midnight.
    Crucially handles GTFS times > 24:00:00 for late-night trips."""
    if pd.isna(time_str):
        return pd.NA
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

print("Loading data...")
# We only load the columns we need to save memory
stop_times = pd.read_csv("data/stop_times.txt", usecols=['trip_id', 'stop_id', 'arrival_time'])
trips = pd.read_csv("data/trips.txt", usecols=['route_id', 'trip_id', 'direction_id'])
routes = pd.read_csv("data/routes.txt", usecols=['route_id', 'route_short_name'])

print("Processing times...")
# Convert the HH:MM:SS string to an integer of seconds
stop_times['arrival_sec'] = stop_times['arrival_time'].apply(time_to_seconds)

# Join the tables to link times to specific routes
merged = pd.merge(stop_times, trips, on='trip_id')
merged = pd.merge(merged, routes, on='route_id')

# Filter for the PoliTo routes we care about
polito_routes = ["10", "15", "16 CS", "16 CD", "33", "42", "58", "58/"]
polito_trips = merged[merged['route_short_name'].astype(str).isin(polito_routes)].copy()

# Sort chronologically at every stop for every route direction
polito_trips = polito_trips.sort_values(by=['route_short_name', 'direction_id', 'stop_id', 'arrival_sec'])

print("Calculating wait times (headways)...")
# Calculate the difference in arrival times between consecutive buses
polito_trips['headway_sec'] = polito_trips.groupby(['route_short_name', 'direction_id', 'stop_id'])['arrival_sec'].diff()

# Convert to minutes
polito_trips['headway_min'] = polito_trips['headway_sec'] / 60

# We filter out unreasonable headways (e.g., the gap between the last bus at night and first bus in the morning)
valid_headways = polito_trips[(polito_trips['headway_min'] > 0) & (polito_trips['headway_min'] < 120)].copy()

# Calculate the average wait time for each route
route_avg_headway = valid_headways.groupby('route_short_name')['headway_min'].mean().reset_index()
route_avg_headway = route_avg_headway.round(1)
route_avg_headway.rename(columns={'headway_min': 'avg_wait_minutes'}, inplace=True)

# Save for the Streamlit dashboard
route_avg_headway.to_csv("data/route_headways.csv", index=False)
print("Saved headway calculations to data/route_headways.csv")
print(route_avg_headway)