from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st
from prettytable import PrettyTable

print("Loaded")
# Çevresel değişkenleri yükleme
load_dotenv()

# OpenAI API anahtarını yükleme
api_key = os.getenv("OPENAI_API_KEY")

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
favorite_movies = []
for i in range(1, 4):
    favorite_movies.append(st.text_input(f"{i}. Movie"))


#Kullanıcıdan film türleri ve favori filmlerini alma
"""movie_types = st.text_input("What types of movies do you like? (separated by commas): ")
favourite_movies = st.text_input("Enter your 3 favourite movies (separated by commas): ")

if st.button('Get Recommendations'):
    if not movie_types or not favourite_movies:
        st.error("Please enter the movie genres and favorite movies.")
"""
if st.button('Get Recommendations'):
    if not movie_types or not all(favorite_movies):
        st.error("Please fill in both the movie genres and your favorite movies.")

    else:
        # Prompt oluşturma
        prompt = (
            f"The user enjoys movies in the following genres: {movie_types}. "
            f"Their favorite movies are: {favorite_movies}. "
            "Based on these preferences, recommend some movies in a table format. "
            "The table should include the movie's name, genre,a short summary,and cover image URL."
        )
        client = OpenAI()
        # OpenAI ChatCompletion API'ye istek gönderme
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # "gpt-4" olarak da değiştirebilirsiniz eğer erişiminiz varsa
            messages=[
                {"role": "system", "content": "You are a film recommendation system."},
                {"role": "user", "content": prompt}
            ]
        )

        # Dönen cevabı işleme ve tablo formatında gösterme
        #print("Recommended Movies:")
        movie_recommendations: list[str] = response.choices[0].message. content. split("\n")[1:]
        #print(movie_recommendations)  # Yanıtı ekrana yazdırıyoruz

        st.subheader("Recommended Movies")
        # Tabloyu oluşturma
        table = PrettyTable()
        table.field_names = ["Movie Name", "Genre", "Summary", "Cover Image"]

        # Metni tabloya dönüştürme
        for line in movie_recommendations:
            columns = line.split('|')
            if len(columns) >= 4:
                movie_name = columns[1].strip()
                genre = columns[2].strip()
                summary = columns[3].strip()
                cover_image_url = columns[4].strip() if len(columns) > 4 else "N/A"
                table.add_row([movie_name, genre, summary, cover_image_url])
        st.write("Recommended Movies:")
        st.text(table)
