import streamlit as st
import pickle
import pandas as pd
import requests
import time

def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=e19ebb47a0e4de206c82e84ea1389d0e&language=en-US'.format(movie_id)
    
    retries = 3
    for _ in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Will raise an HTTPError for bad responses
            data = response.json()
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            time.sleep(3)  # Wait for 3 seconds before retrying

    return "Failed to get poster after retries"



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('FLICKFINDER')

selected_movie_name  = st.selectbox(
'SEARCH YOUR FAVORITE MOVIE',
movies['title'].values)

if st.button('recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])