import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from openai import OpenAI

# Çevresel değişkenleri yükleme
load_dotenv()

# OpenAI API anahtarını yükleme
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

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
favourite_movies = [st.text_input(f"{i}. Movie") for i in range(1, 4)]

if st.button('Get Recommendations'):
    if not movie_types or not any(favourite_movies):
        st.error("Please enter both the movie genres and your favorite movies.")
    else:
        # Prompt oluşturma
        prompt = (
            f"The user enjoys movies in the following genres: {movie_types}. "
            f"Their favorite movies are: {favourite_movies}. "
            "Based on these preferences, recommend some movies in a table format. "
            "Include Name, Genre, Summary, Release Year, Duration, Director, Actors, IMDb Rating, Rotten Tomatoes Rating, and a link to the trailer."
        )

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
        # Dönen cevabı işleme

        movie_recommendations: list[str] = response.choices[0].message.content.split("\n")[1:]

        # Tablodaki satırları toplamak için bir liste
        rows = []

        for index, line in enumerate(movie_recommendations):
            columns = line.split('|')
            cleaned_columns = [col.strip() for col in columns if col.strip()]

            # İlk satır başlık olarak algılanıyorsa atla
            if index == 0 and len(cleaned_columns) == len(columns):
                continue

            # Beklenen sütun sayısının altında ise, bu satırı atla
            if len(cleaned_columns) < 10:
                continue

            rows.append(cleaned_columns)

        # Tablonun sütun isimleri
        columns = [
            "Name", "Genre", "Summary", "Release Year", "Duration", "Director",
            "Actors", "IMDb Rating", "Rotten Tomatoes Rating", "Trailer Link"
        ]

        # Pandas DataFrame oluşturma
        df = pd.DataFrame(rows, columns=columns)

        # Streamlit üzerinde tabloyu göster
        st.table(df)
