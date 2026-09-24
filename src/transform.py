import pandas as pd

print("Loading GTFS files...")
# 1. Load the text files into Pandas DataFrames
routes = pd.read_csv("data/routes.txt")
trips = pd.read_csv("data/trips.txt")
shapes = pd.read_csv("data/shapes.txt")

print("Transforming and joining data...")

# A single bus route runs thousands of trips a day over the exact same path.
# We only need ONE trip per route to get its physical shape on the map.
unique_trips = trips.drop_duplicates(subset=['route_id'])

# 2. Join the Route Name to its Unique Shape ID
# We only select the columns we care about to keep memory usage low
route_info = pd.merge(
    routes[['route_id', 'route_short_name']], 
    unique_trips[['route_id', 'shape_id']], 
    on='route_id', 
    how='inner'
)

# 3. Join the resulting table with the actual GPS coordinates
network_geometry = pd.merge(
    route_info, 
    shapes[['shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence']], 
    on='shape_id', 
    how='inner'
)

# Sort by shape and sequence to ensure the lines draw in the correct order later
network_geometry = network_geometry.sort_values(by=['shape_id', 'shape_pt_sequence'])

print("Transformation complete! Here is a preview of the joined data:")
print(network_geometry.head())
print(f"\nTotal GPS points mapped: {len(network_geometry)}")

# Save the cleaned dataset so our app can load it instantly
network_geometry.to_csv("data/network_geometry.csv", index=False)
print("Saved to data/network_geometry.csv")