# Turin Transit Optimizer

Your public transit system gives you massive, static text files. This turns them into navigable intelligence.

Navigating a city's transit network is a product of efficiency, and true bottlenecks are rarely visible on a static PDF map. While commuting to the Politecnico di Torino campus, I found that relying on scheduled timetables rather than concrete spatial metrics made it challenging to optimize my route.

I built this project to bridge that gap. By translating raw GTFS (General Transit Feed Specification) data into clear visual trends and spatial maps, this dashboard proves exactly how the network performs. I got tired of staring at endless rows of coordinates and stop times in a spreadsheet, so I built a pipeline that does the work for me. Drop in the GTT open dataset, and the complex web of routes is cleaned, calculated, and instantly visualized in a dynamic web application.

No guesswork. Just Python, geospatial math, and proof of transit efficiency.

### What it does?
The pipeline runs in three fluid stages:

**Extract** — Reads the raw GTFS `.txt` files straight from the Turin open data portal. Massive unjoined tables, `25:30:00` late-night timestamp edge cases, millions of GPS coordinates — it takes it all in.

**Transform** — This is where the core data engineering happens:
*   Relational joins reconstruct the physical paths of specific bus and tram lines using `shapes.txt` and `trips.txt`.
*   Complex timestamp strings are parsed mathematically into seconds-past-midnight to engineer new features on the fly: Average Wait Time (Headway).
*   External API integration via OpenRouteService generates a 30-minute spatial reachability isochrone around the campus.

**Load & Visualize** — The cleaned, grouped data is immediately served into a local Streamlit web application. Instead of querying a database, the user interacts directly with dynamic Plotly Mapbox visuals and category charts.

`GTFS .txt ──▶ Extract ──▶ Transform ──▶ Visualize`

### The stack
*   **Python 3.10+**
*   **pandas** — data wrangling and feature engineering
*   **streamlit** — web framework and UI
*   **plotly** — interactive data visualization and mapping
*   **openrouteservice** — spatial isochrone generation

**Bash:**
```bash
pip install pandas streamlit plotly openrouteservice
```
### Getting started
**Get your raw data**

Download the Turin GTFS data (Google Transit zip) from the Aperto Comune di Torino or Mobility Database. Extract the archive and drop the .txt files (like routes.txt, stop_times.txt, and shapes.txt) into a data/ folder in the project root.

Run the data pipeline
Process the geometry, calculate the headways, and ping the API to generate the local spatial files:

```bash
python src/transform.py
python src/calculate_headways.py
python src/generate_isochrone.py 
```
**Run the application**

Spin up the local server:
```bash
streamlit run src/app.py
```

Interact
Open your browser to http://localhost:8501. The UI instantly populates with the map and metrics:

[MAP] 🗺️ Interactive Route Traces & 30-Min Walkable Isochrone
[CHART] ⏱️ Average Wait Time per Route
========================================
Select any line serving the campus from the dropdown to see exactly how your commute operates.

### Project Structure

```plaintext
Turin-Transit-Optimizer/
├── src/
│   ├── app.py — the complete web UI and frontend
│   ├── transform.py — spatial joins and path reconstruction
│   ├── calculate_headways.py — GTFS time string math and delays
│   └── generate_isochrone.py — OpenRouteService API integration
├── data/ — (Ignored via .gitignore) raw GTFS .txt and processed .csv/.json files
├── .gitignore
└── README.md
```

**License**

Do whatever you want.
