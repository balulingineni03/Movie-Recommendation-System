import streamlit as st
import pickle
import pandas as pd

# Load the data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        movie_id = i[0]
        recommended_movies.append(movies.iloc[movie_id])
    return recommended_movies

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie you like, and we will recommend similar ones!',
    movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for movie_details in recommendations:
        st.subheader(movie_details.title)

        # Safely get and display details
        director = movie_details.crew[0] if movie_details.crew else "N/A"
        cast_list = movie_details.cast
        hero = cast_list[0] if len(cast_list) > 0 else "N/A"
        heroine = cast_list[1] if len(cast_list) > 1 else "N/A"
        full_cast = ", ".join(cast_list) if cast_list else "N/A"

        st.text(f"Director: {director}")
        st.text(f"Hero: {hero}")
        st.text(f"Heroine: {heroine}")
        st.text(f"Cast: {full_cast}")