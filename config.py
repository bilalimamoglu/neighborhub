import streamlit as st
import os


EVENTS_URL = st.secrets["EVENTS_URL"]
CALENDAR_RESOURCES_URL = st.secrets["CALENDAR_RESOURCES_URL"]
CONTROL_VARIABLES_URL = st.secrets["CONTROL_VARIABLES_URL"]
LOGO_PATH = os.path.join('resources', 'asset.png')