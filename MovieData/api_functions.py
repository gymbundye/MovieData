import requests

def get_movie_details(title, api_key):
    base_url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': title}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0], None
    return None, f"Movie '{title}' not found in TMDB database."

def get_genre_list(api_key):
    base_url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {'api_key': api_key}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {genre['id']: genre['name'] for genre in data['genres']}
    return None
