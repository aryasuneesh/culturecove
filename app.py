import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv.main import load_dotenv

load_dotenv()

# Global variables
MAP_CENTER = [0, 0]
MARKER_ICON = folium.Icon(icon="info-sign", prefix="fa")
REVIEWS_FILE = "reviews.csv"
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connect to MongoDB Atlas
uri = f"mongodb+srv://aryasuneesh3:{DB_PASSWORD}@ccluster.a0eszym.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["hidden-places"]
places_collection = db["places"]

# Initialize reviews DataFrame
reviews_df = pd.DataFrame(columns=["Place", "Description", "Review"])

# Helper function to mark a place on the map
def mark_place_on_map(latitude, longitude, place_name, description, review):
    global reviews_df

    # Create marker with place name and description
    popup_content = f"<b>{place_name}</b><br>{description}<br>"

    # Calculate average review rating
    if len(reviews_df) > 0:
        avg_rating = reviews_df[reviews_df["Place"] == place_name]["Review"].mean()
        if pd.notnull(avg_rating):
            avg_rating = round(avg_rating, 2)
            popup_content += f"Avg Rating: {avg_rating} stars out of 5"

    # Add marker to map
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(popup_content, max_width=250),
        icon=MARKER_ICON
    ).add_to(map_obj)

    # Add review to DataFrame
    new_review = {"Place": place_name, "Description": description, "Review": review}
    reviews_df = pd.concat([reviews_df, pd.DataFrame(new_review, index=[0])], ignore_index=True)

    # Save place to MongoDB
    place_data = {
        "place_name": place_name,
        "latitude": latitude,
        "longitude": longitude,
        "description": description,
        "review": review
    }
    places_collection.insert_one(place_data)

# Helper function to add a review to a place
def add_review(place_name, review_text):
    global reviews_df
    new_review = {"Place": place_name, "Description": "", "Review": review_text}
    reviews_df = pd.concat([reviews_df, pd.DataFrame(new_review, index=[0])], ignore_index=True)

    # Update review in MongoDB
    places_collection.update_one({"place_name": place_name}, {"$set": {"review": review_text}})

# Helper function to get the average rating for a place
def get_average_rating(place_name):
    global reviews_df
    avg_rating = reviews_df[reviews_df["Place"] == place_name]["Review"].mean()
    if pd.notnull(avg_rating):
        return round(avg_rating, 2)
    return None

# Helper function to clear input fields
def clear_input_fields():
    st.experimental_set_query_params(place_name="", latitude=0.0, longitude=0.0, description="", review="")

# Main function to build the Streamlit app
def main():
    st.title("Hidden Places of Art and Culture")

    # Create a sidebar for adding a place and writing a review
    st.sidebar.title("Actions")
    action = st.sidebar.radio("Select Action", ["Add Place", "Write Review"])

    # Add Place action
    if action == "Add Place":
        st.sidebar.subheader("Add Place")
        place_name = st.sidebar.text_input("Place Name", key="place_name")
        latitude = st.sidebar.number_input("Latitude", key="latitude")
        longitude = st.sidebar.number_input("Longitude", key="longitude")
        description = st.sidebar.text_area("Description", key="description")
        review = None

        if st.sidebar.button("Mark Place", key="mark_place"):
            mark_place_on_map(latitude, longitude, place_name, description, review)
            clear_input_fields()

    # Write Review action
    elif action == "Write Review":
        st.sidebar.subheader("Write Review")
        place_options = reviews_df["Place"].unique().tolist()
        selected_place = st.sidebar.selectbox("Select a Place", place_options, key="selected_place")
        review = st.sidebar.text_area("Review", key="review")

        if st.sidebar.button("Add Review", key="add_review"):
            add_review(selected_place, review)
            clear_input_fields()

    # Display the map
    folium_static(map_obj)

    # Display the added places and their descriptions
    for idx, place in enumerate(reviews_df["Place"].unique()):
        description = reviews_df.loc[reviews_df["Place"] == place, "Description"].values[0]
        review = get_average_rating(place)
        st.markdown(f"**{idx + 1}. {place}**")
        st.markdown(f"Description: {description}")
        st.markdown(f"Average Rating: {review} stars out of 5" if review is not None else "No reviews yet")

# Load the map with an initial center point
map_obj = folium.Map(location=MAP_CENTER, zoom_start=2)

# Run the Streamlit app
if __name__ == "__main__":
    main()
