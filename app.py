import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_calendar import calendar

from config import LOGO_PATH, EVENTS_URL, CALENDAR_RESOURCES_URL, CONTROL_VARIABLES_URL

st.set_page_config(
    page_title="NEIGHBORhub",
    layout='wide',
    page_icon=LOGO_PATH,
    menu_items={
        'Get help': 'mailto:gizemsanyilmaz97@gmail.com',
        'Report a bug': 'mailto:gizemsanyilmaz97@gmail.com',
        'About': """
                               ### About This App
                               This is NEIGHBORhub, a Calendar app for managing events.
                               """
    }
)
st.image(LOGO_PATH, width=200, output_format='PNG')

st.text("")
st.text("")

events_df = pd.read_csv(EVENTS_URL)
calendar_resources_df = pd.read_csv(CALENDAR_RESOURCES_URL)
control_variables_df = pd.read_csv(CONTROL_VARIABLES_URL)

events_for_calendar = events_df.to_dict(orient='records')
calendar_resources_for_calendar = calendar_resources_df.to_dict(orient='records')
control_variables_df = control_variables_df.to_dict(orient='records')

calendar_options = {
    "editable": "false",
    "resourceEditable": "false",
    "durationEditable": "false",
    "startEditable": "false",
    "navLinks": "true",
    "resources": calendar_resources_for_calendar,
    "selectable": "true",
}

calendar_options = {
    **calendar_options,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
        "backgroundColor": "blue"
    },
    "slotMinTime": "08:00:00",
    "slotMaxTime": "23:00:00",
    "initialDate": "2024-05-01",
    "height": "auto",
    "initialView": "resourceTimelineDay",
    "resourceGroupField": "Straße",
}

col1, col2, col3 = st.columns([1, 13, 1])  # Adjust the middle number to control the width

with col2:  # This is where the calendar will be displayed
    state = calendar(
        events=st.session_state.get("events", events_for_calendar),
        options=calendar_options,
        custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 1.5rem;
        }
        .fc-header-toolbar {
        font-size: 12px; /* Smaller font size */
        height: 30px; /* Smaller height */
}
        """,
        key='resource-timeline',
    )

if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

calendar_resources_df[['lat', 'lon']] = calendar_resources_df[['lat', 'lon']].astype(float)
map_data = calendar_resources_df[['lat', 'lon', 'title', 'address', 'content']]

zoom_level = control_variables_df[0]['zoom']
pitch_level = control_variables_df[0]['pitch']

st.markdown('# Discover Our HUBs!')

layer = pdk.Layer(
    'ScatterplotLayer',
    map_data,
    get_position='[lon, lat]',
    get_color='[0, 0, 128, 200]',
    get_radius=50,
    get_elevation=100,
    elevation_scale=4,
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=map_data['lat'].mean(),
    longitude=map_data['lon'].mean(),
    zoom=zoom_level,
    pitch=pitch_level,
)

tooltip = {
    "html": "<p>Address: {title}<br> "
            "What's inside:</b> {content} </p>",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/streets-v12",
    tooltip=tooltip
))
