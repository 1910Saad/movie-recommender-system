import streamlit as st
import pickle
import pandas as pd
import requests as rq

def fetch_poster(movie_id):
    res = rq.get('https://api.themoviedb.org/3/movie/{}?api_key=b79d406598f97264c005a515b167d6f5&language=en-US'.format(movie_id))
    data = res.json()
    print(data)
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch movie poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters



movies_dicts = pickle.load(open('movies_dict.pkl ','rb'))
movies = pd.DataFrame(movies_dicts)

similarity = pickle.load(open('similarity.pkl ','rb'))

print(movies)

st.title('Movie Recommender System')
selected_movies_name = st.selectbox('Select your movie', movies['title'].values)

if st.button(label='Recommend'):
    names,posters = recommend(selected_movies_name)
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

