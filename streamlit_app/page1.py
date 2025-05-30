import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os

def load_parquet_data(file_name):
    file_path = Path(__file__).resolve().parent.parent / "output" / file_name
    return pd.read_parquet(file_path)

# Define the output directory
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

st.title("🎬 General Analysis of Movies and Ratings")

# Load the data from parquet files
genre_df = load_parquet_data("genre_df.parquet")
movies_by_year = load_parquet_data("movies_by_year.parquet")
top_movies = load_parquet_data("top_movies_by_ratings.parquet")
top_users = load_parquet_data("top_users.parquet")
ratings_df = load_parquet_data("ratings.parquet")

# Chart 1: Number of movies by year (moved up to display first)
fig_by_year = px.bar(
    movies_by_year,
    x="year",
    y="movie_count",
    title="Total Number of Movies per Year (Based on Title)",
    labels={"year": "Year", "movie_count": "Number of Movies"},
)
fig_by_year.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Movies",
    height=500
)

# Chart 2: Top 10 genres by number of movies
fig_genre = px.bar(
    genre_df,
    x="count",
    y="genre",
    title="Top 10 Genres by Number of Movies",
    labels={"genre": "Genre", "count": "Number of Movies"},
    color="count",
    color_continuous_scale="viridis",
    orientation='h'
)
fig_genre.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    height=350
)

# Chart 3: Top 10 users by number of ratings
top_users["userId"] = top_users["userId"].astype(str)
top_users = top_users.sort_values(by="rating_count", ascending=False)
top_users_reversed = top_users[::-1]

fig_users = px.bar(
    top_users_reversed,
    x="rating_count",
    y="userId",
    orientation="h",
    title="Top 10 Users by Number of Ratings",
    labels={"userId": "User", "rating_count": "Number of Ratings"},
    color="rating_count",
    color_continuous_scale="viridis"
)
fig_users.update_layout(
    yaxis=dict(
        categoryorder="array",
        categoryarray=top_users_reversed["userId"].tolist()
    ),
    height=400
)

# Chart 4: Top 20 movies by number of ratings
fig_top_movies = px.bar(
    top_movies.sort_values("rating_count", ascending=True),
    x="rating_count",
    y="title",
    color="avg_rating",
    orientation="h",
    title="Top 20 Movies by Number of Ratings",
    labels={"title": "Movie Title", "rating_count": "Number of Ratings", "avg_rating": "Average Rating"},
    color_continuous_scale="viridis"
)
fig_top_movies.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    height=700
)

# Chart 5: Distribution of ratings given
fig_rating_dist = px.histogram(
    ratings_df,
    x="rating",
    nbins=10,
    title="Distribution of Ratings Given",
    labels={"rating": "Rating"},
)
fig_rating_dist.update_layout(bargap=0.1)

# Chart 6: Distribution of average ratings per user
avg_rating_per_user = ratings_df.groupby("userId")["rating"].mean().reset_index()
fig_avg_rating_dist = px.histogram(
    avg_rating_per_user,
    x="rating",
    nbins=50,
    title="Distribution of Average Ratings per User",
    labels={"rating": "Average Rating"},
)
fig_avg_rating_dist.update_layout(bargap=0.1)

# Streamlit layout
st.subheader("📅 Movie Production Over Time")
st.plotly_chart(fig_by_year, use_container_width=True)

st.markdown("---")

st.markdown("## 📊 Insights Overview")
st.markdown("Use the charts below to explore genre distribution, top movies, user behavior, and film trends over time.")

# Two columns for some charts
col1, col2 = st.columns([1.2, 1.8], gap="medium")

with col1:
    st.subheader("🎭 Genre Insights")
    st.plotly_chart(fig_genre, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.subheader("👤 Top Users by Ratings")
    st.plotly_chart(fig_users, use_container_width=True)

with col2:
    st.subheader("🎞️ Top Rated Movies")
    st.plotly_chart(fig_top_movies, use_container_width=True)

st.markdown("---")

# Show rating distributions
col3, col4 = st.columns(2, gap="large")

with col3:
    st.subheader("📈 Ratings Distribution")
    st.plotly_chart(fig_rating_dist, use_container_width=True)

with col4:
    st.subheader("⭐ Average User Ratings Distribution")
    st.plotly_chart(fig_avg_rating_dist, use_container_width=True)
