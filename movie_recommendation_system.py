from openai import OpenAI
import os
from dotenv import load_dotenv
from prettytable import PrettyTable
# Çevresel değişkenleri yükleme
load_dotenv()

# OpenAI API anahtarını yükleme
api_key = os.getenv("OPENAI_API_KEY")

# Kullanıcıdan film türleri ve favori filmlerini alma
movie_types = input("What types of movies do you like? (separated by commas): ")
favourite_movies = input("Enter your 3 favourite movies (separated by commas): ")

# Prompt oluşturma
prompt = (
    f"The user enjoys movies in the following genres: {movie_types}. "
    f"Their favorite movies are: {favourite_movies}. "
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
print("Recommended Movies:")
movie_recommendations: list[str] = response.choices[0].message. content. split("\n")[1:]
print(movie_recommendations)  # Yanıtı ekrana yazdırıyoruz


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

print("Recommended Movies:")
print(table)