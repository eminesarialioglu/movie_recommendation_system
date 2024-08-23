from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import re
import json

print("Loaded")
# Çevresel değişkenleri yükleme
load_dotenv()

# OpenAI API anahtarını yükleme
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("API anahtarı bulunamadı. Lütfen .env dosyanızı kontrol edin.")
    st.stop()


# Streamlit Başlık
st.title('Movie Recommendation System')
st.subheader("How It Works?")
st.markdown("""
- **Select the movie genres you like**
- **Enter your 3 favorite movies**
- **Submit the information**
- **Get personalized movie recommendations!**
""")

# Movie genre selection options
movie_types = st.multiselect(
    "Movie Genres",
    [
        "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary",
        "Drama", "Family", "Fantasy", "History", "Horror", "Musical", "Mystery", "Romance",
        "Science Fiction", "Sport", "Thriller", "War", "Western"
    ]
)


# Text input fields for user's favorite movies
favorite_movies = [st.text_input(f"{i}. Movie") for i in range(1, 4)]

if st.button('Get Recommendations'):
    if not movie_types or not any(favorite_movies):
        st.error("Please enter both the movie genres and your favorite movies.")

    else:
        # Prompt oluşturma
        prompt = (
            f"The user enjoys movies in the following genres: {', '.join(movie_types)}. "
            f"Their favorite movies are: {', '.join(favorite_movies)}. "
            "Based on these preferences, recommend some movies with the following details: "
            "Name, Genre, Summary, Release Year, Duration, Director, Actors, IMDb Rating, Rotten Tomatoes Rating, Cover Image URL, and a link to the trailer."
        )

        client = OpenAI()
        # OpenAI ChatCompletion API'ye istek gönderme
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are a film recommendation system."
                 },
                {"role": "user",
                 "content": prompt
                 }
            ]
        )
        response_text = response.choices[0].message.content
        st.write("API Yanıtı:", response_text)


        # Metinden liste oluşturma
        def parse_movie_recommendations(text):
            movies = []
            entries = re.split(r'\n(?=\d+\.)', text.strip())
            for entry in entries:
                movie = {}
                lines = entry.split('\n')
                for line in lines:
                    if line:
                        parts = line.split(': ', 1)
                        if len(parts) == 2:
                            key, value = parts
                            key = key.strip()
                            value = value.strip()
                            if key in ["Name", "Genre", "Summary", "Release Year", "Duration", "Director", "Actors", "IMDb Rating", "Rotten Tomatoes Rating", "Cover Image URL", "Trailer Link"]:
                                movie[key] = value
                if movie:
                    movies.append(movie)
            return movies

        movie_list = parse_movie_recommendations(response_text)
        st.write("Parsed Recommendations:")
        if movie_list:
            st.table(movie_list)
        else:
            st.write("No recommendations found. Please check the API response format.")
