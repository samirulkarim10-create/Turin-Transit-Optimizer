import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# 1. Page Configuration
st.set_page_config(page_title="PoliTo Transit Optimizer", layout="wide")
st.title("🎓 PoliTo Commute Optimizer")
st.write("Visualizing the GTT public transit routes serving Politecnico di Torino.")

# 2. Data Loading with Caching
@st.cache_data
def load_data():
    return pd.read_csv("data/network_geometry.csv")

@st.cache_data
def load_headways():
    return pd.read_csv("data/route_headways.csv")

df = load_data()
headway_df = load_headways()

polito_routes = ["10", "15", "16 CS", "16 CD", "33", "42", "58", "58/"]

# 3. Sidebar for interactivity
st.sidebar.header("Filter Your Commute")
selected_routes = st.sidebar.multiselect(
    "Select lines to visualize:",
    options=sorted(df['route_short_name'].astype(str).unique()),
    default=polito_routes
)
# --> This is the new checkbox for the Isochrone <--
show_isochrone = st.sidebar.checkbox("Show 30-Min Walkable Radius", value=False)

filtered_df = df[df['route_short_name'].astype(str).isin(selected_routes)]

# 4. Render the Map
if not filtered_df.empty:
    fig = px.line_mapbox(
        filtered_df, 
        lat="shape_pt_lat", 
        lon="shape_pt_lon", 
        color="route_short_name",  
        line_group="shape_id",     
        zoom=13.5, 
        center={"lat": 45.0628, "lon": 7.6622}, 
        mapbox_style="open-street-map", 
        title="Routes to Politecnico di Torino",
        height=700
    )
    
    fig.update_traces(line=dict(width=4.5))
    
    fig.add_trace(go.Scattermapbox(
        lat=[45.0628],
        lon=[7.6622],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=22,             
            color='crimson',     
            opacity=1.0
        ),
        text=["🎓 PoliTo Main Campus"],
        textfont=dict(size=16, color='black'), 
        textposition="bottom right",
        name="Campus"
    ))

    # --- NEW ISOCHRONE LOGIC ---
    if show_isochrone:
        with open('data/polito_isochrone.json') as f:
            isochrone_data = json.load(f)
        
        fig.update_layout(
            mapbox_layers=[
                {
                    "sourcetype": "geojson",
                    "source": isochrone_data,
                    "type": "fill",
                    "color": "rgba(220, 20, 60, 0.15)",
                }
            ]
        )
    # ---------------------------

    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select at least one route from the sidebar.")

# 5. Render the Headway Bar Chart
st.markdown("---")
st.subheader("⏱️ Average Wait Time (Headway)")

filtered_headway = headway_df[headway_df['route_short_name'].astype(str).isin(selected_routes)].copy()
filtered_headway['route_short_name'] = filtered_headway['route_short_name'].astype(str)

fig_bar = px.bar(
    filtered_headway, 
    x="route_short_name", 
    y="avg_wait_minutes", 
    title="Average Wait Time per Route (Minutes)",
    labels={"route_short_name": "Line", "avg_wait_minutes": "Wait Time (Min)"},
    text="avg_wait_minutes"
)

fig_bar.update_xaxes(type='category', categoryorder='category ascending')

fig_bar.update_traces(
    textposition='outside',
    marker_color='crimson' 
)

st.plotly_chart(fig_bar, use_container_width=True)