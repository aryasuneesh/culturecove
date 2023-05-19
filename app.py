import streamlit as st
import folium
from streamlit_folium import folium_static

# Set the page title
st.title("Hidden Places of Art and Culture")

# Sidebar header
st.sidebar.header("Add a Place")

# Sidebar input components
place_name = st.sidebar.text_input("Place Name")
latitude = st.sidebar.number_input("Latitude")
longitude = st.sidebar.number_input("Longitude")

# Submit button
if st.sidebar.button("Submit"):
    # Create a Folium map centered on the provided latitude and longitude
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # Mark the place on the map
    folium.Marker(location=[latitude, longitude], popup=place_name).add_to(m)

    # Display the map in Streamlit using the folium_static function
    st.sidebar.write(folium_static(m))

# Display the marked places
st.header("Marked Places")
# You can fetch and display the marked places using your preferred data source
