import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote_plus

def get_movie_url(movie_title):
    movie_title = quote_plus(movie_title)
    search_result_url = "https://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=all".format(movie_title)
    r = requests.get(search_result_url)
    soup = BeautifulSoup(r.text)
    first_result = soup.select(".result_text a")[0]
    movie_url = "https://www.imdb.com" + first_result.get("href")
    return movie_url

def get_movie_data(movie_title):
    movie_url = get_movie_url(movie_title)
    r = requests.get(movie_url)
    soup = BeautifulSoup(r.text)
    movie_title = soup.find("h1").text.strip()
    movie_poster_link = [i.get("src") for i in soup.select(".poster img")][0]
    movie_rating = float(soup.select("strong span")[0].text)
    movie_genre = [i.text for i in soup.select(".subtext a")]
    movie_genre.pop()
    movie_cast = [i.text.strip() for i in soup.select(".primary_photo+ td a")]
    movie_data = {
        "movieTitle": movie_title,
        "moviePosterLink": movie_poster_link,
        "movieRating": movie_rating,
        "movieGenre": movie_genre,
        "movieCast": movie_cast
    }
    return movie_data

movie_ratings = []
movie_titles_with_error = []
for movie_title in ca_movie_titles:
    try:
        movie_data = get_movie_data(movie_title)
        movie_rating = movie_data["movieRating"]
        movie_ratings.append(movie_rating)
    except:
        movie_titles_with_error.append(movie_title)
print(movie_rating)
print(movie_titles_with_error)

for movie_title in movie_titles_with_error:
    ca_movie_titles.remove(movie_title)

movies = pd.DataFrame()
movies["title"] = ca_movie_titles
movies["rating"] = movie_ratings
movies = movies.sort_values("rating", ascending=False)
movies.head()
