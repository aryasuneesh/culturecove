import streamlit as st
import folium
import json

MAP_CENTER = [0, 0]
MARKER_ICON = folium.Icon(icon="info-sign", prefix="fa")
PLACES_FILE = "places.json"

# Helper function to load places from JSON file
def load_places():
    try:
        with open(PLACES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Helper function to save places to JSON file
def save_places(places):
    with open(PLACES_FILE, "w") as f:
        json.dump(places, f)

# Helper function to mark a place on the map
def mark_place_on_map(map_obj, latitude, longitude, place_name, description, reviews):
    # Create marker with place name and description
    popup_content = f"<b>{place_name}</b><br>{description}<br>"

    if reviews:
        reviews_content = "<ul>"
        for review in reviews:
            reviews_content += f"<li>{review}</li>"
        reviews_content += "</ul>"
        popup_content += reviews_content

    # Add marker to map
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(popup_content, max_width=250),
        icon=MARKER_ICON
    ).add_to(map_obj)

# Main function to build the Streamlit app
def main():
    st.title("Hidden Places of Art and Culture")

    # Load existing places from JSON file
    existing_places = load_places()

    # Create a Folium map centered on the existing places
    m = folium.Map(location=MAP_CENTER, zoom_start=2)

    # Mark the existing places on the map
    for place in existing_places:
        mark_place_on_map(
            m,
            place["latitude"],
            place["longitude"],
            place["place_name"],
            place["description"],
            place.get("reviews", [])
        )

    # Display the map in the main page
    st.header("Map")
    folium_map = m._repr_html_()
    st.components.v1.html(folium_map, width=800, height=600, scrolling=True)

    # Create a sidebar for adding a place and writing a review
    st.sidebar.title("Actions")
    action = st.sidebar.radio("Select Action", ["Add Place", "Write Review"])

    # Add Place action
    if action == "Add Place":
        st.sidebar.subheader("Add Place")
        place_name = st.sidebar.text_input("Place Name")
        latitude = st.sidebar.number_input("Latitude")
        longitude = st.sidebar.number_input("Longitude")
        description = st.sidebar.text_area("Description")

        if st.sidebar.button("Mark Place"):
            place_data = {
                "place_name": place_name,
                "latitude": latitude,
                "longitude": longitude,
                "description": description
            }
            existing_places.append(place_data)
            save_places(existing_places)
            mark_place_on_map(m, latitude, longitude, place_name, description, [])
            st.sidebar.success("Place added successfully!")

    # Write Review action
    elif action == "Write Review":
        st.sidebar.subheader("Write Review")
        place_options = [place["place_name"] for place in existing_places]
        selected_place = st.sidebar.selectbox("Select a Place", place_options)
        review_text = st.sidebar.text_area("Review")

        if st.sidebar.button("Submit Review"):
            for place in existing_places:
                if place["place_name"] == selected_place:
                    if "reviews" not in place:
                        place["reviews"] = []
                    place["reviews"].append(review_text)
                    save_places(existing_places)
                    st.sidebar.success("Review added successfully!")
                    break

    # Display reviews below the map
    st.header("Reviews")
    for place in existing_places:
        st.subheader(place["place_name"])
        reviews = place.get("reviews", [])
        if len(reviews) > 0:
            for review in reviews:
                st.write(review)
        else:
            st.write("No reviews yet for this place.")

if __name__ == "__main__":
    main()
