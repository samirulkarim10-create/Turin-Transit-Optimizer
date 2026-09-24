import openrouteservice
import json

# Your free ORS key
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjA4ZjY0ZDY4Y2FiNzQzYzNhM2M5Yjc0MjVkYzMzN2I2IiwiaCI6Im11cm11cjY0In0="

print("Connecting to OpenRouteService...")
client = openrouteservice.Client(key=API_KEY)

# Coordinates for Politecnico di Torino main campus (Longitude, Latitude for ORS)
polito_coords = [7.6622, 45.0628]

print("Requesting 30-minute transit isochrone...")
try:
    # Request a polygon for areas reachable within 30 minutes (1800 seconds)
    # Note: ORS free tier handles walking/driving isochrones natively. 
    # For this portfolio, we will simulate a "transit/walking" profile using their API.
    iso = client.isochrones(
        locations=[polito_coords],
        profile='foot-walking', # We use walking as a baseline for the API demo
        range=[1800],           # 1800 seconds = 30 minutes
        attributes=['total_pop'] # Cool bonus: estimates how many people live in this radius!
    )
    
    # Save the polygon data locally
    with open('data/polito_isochrone.json', 'w') as f:
        json.dump(iso, f)
        
    print("Success! Isochrone polygon saved to data/polito_isochrone.json")
    
except openrouteservice.exceptions.ApiError as e:
    print(f"API Error: {e}")