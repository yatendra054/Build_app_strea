from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import streamlit as st
geocoders = Nominatim(user_agent="i know distance")
def get_cordinates(location):
    try:
        location_data = geocoders.geocode(location)
        if location_data:
            return location_data.latitude, location_data.longitude
    except AttributeError:
        return None
def get_distance(location1, location2):
    coordinate1 = get_cordinates(location1)
    coordinate2 = get_cordinates(location2)
    if coordinate1 and coordinate2:
        distance = geodesic(coordinate1, coordinate2).kilometers
        return distance
    else:
        return "Your Locations not found"

st.title("Calculate Distance Between Two Locations")
location1 = st.text_input("Enter Your First Location")
location2 = st.text_input("Enter Your Second Location")
if st.button("Distance"):
    if location1 and location2:
        try:
            distance_km = get_distance(location1, location2)
            if distance_km > 1000:
                st.success(f"Diatance from {location1} to {location2} is:{distance_km + 300: .2f} kilometer")
            elif distance_km < 180:
                 st.success(f"Diatance from {location1} to {location2} is:{distance_km + 10: .2f} kilometer")
            elif distance_km > 180 and distance_km < 500:
                 st.success(f"Diatance from {location1} to {location2} is:{distance_km + 50: .2f} kilometer")
            else:
                 st.success(f"Diatance from {location1} to {location2} is:{distance_km + 200: .2f} kilometer")
        except ValueError as e:
            st.error(f"Error:{e}")