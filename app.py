import streamlit as st
import folium
from streamlit_folium import folium_static
import json

# Set the page title
st.title("Hidden Places of Art and Culture")

# Load existing places from JSON file
existing_places = []
with open("places.json", "r") as file:
    for line in file:
        existing_places.append(json.loads(line))

# Create a Folium map centered on the existing places
m = folium.Map(location=[0, 0], zoom_start=2)

# Mark the existing places on the map
for place in existing_places:
    folium.Marker(location=[place['latitude'], place['longitude']], popup=place['name']).add_to(m)

# Display the map in the main page
st.header("Map")
folium_static(m)

# Sidebar header
st.sidebar.header("Add a Place")

# Sidebar input components
place_name = st.sidebar.text_input("Place Name")
latitude = st.sidebar.number_input("Latitude")
longitude = st.sidebar.number_input("Longitude")

# Submit button
if st.sidebar.button("Submit"):
    # Check if the place already exists
    existing_place_names = [place['name'] for place in existing_places]
    if place_name in existing_place_names:
        st.sidebar.error("Place already exists!")
    else:
        # Create a Folium map centered on the provided latitude and longitude
        folium.Marker(location=[latitude, longitude], popup=place_name).add_to(m)

        # Save the place data to the JSON file
        new_place = {
            "name": place_name,
            "latitude": latitude,
            "longitude": longitude
        }
        existing_places.append(new_place)

        with open("places.json", "a") as file:
            file.write(json.dumps(new_place))
            file.write("\n")

# Display a success message if a new place was added
if st.sidebar.button("Submit") and place_name not in existing_place_names:
    st.sidebar.success("Place added successfully!")
