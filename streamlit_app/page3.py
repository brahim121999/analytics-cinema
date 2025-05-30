import streamlit as st
import pandas as pd
from pathlib import Path
import re

# ====== Cache initialization of the MovieClient ======
from filmsdk_ibrahim import MovieClient, MovieConfig

@st.cache_resource
def get_movie_client():
    config = MovieConfig(movie_base_url="https://backend-cinema-96tw.onrender.com")
    client = MovieClient(config=config)
    client.health_check()
    return client

client = get_movie_client()

# === Load data files ===
output_dir = Path(__file__).resolve().parents[1] / "output"

movie_stats = pd.read_parquet(output_dir / "top_movies_by_ratings.parquet")
genre_df = pd.read_parquet(output_dir / "genre_df.parquet")
tags_df = pd.read_parquet(output_dir / "user_tag_stats.parquet")
ratings_df = pd.read_parquet(output_dir / "ratings.parquet")

# === Load enriched metadata ===
meta_links_df = pd.read_parquet(output_dir / "links_enriched.parquet")
meta_links = meta_links_df.set_index("movieId")[["imdb_url", "poster_url"]].to_dict(orient="index")

# === Search Filters ===
st.title("🔎 Movie Explorer")

with st.expander("🎯 Advanced Filters", expanded=True):
    col1, col2, col3 = st.columns([1, 1, 2])

    all_genres = sorted(set(genre_df['genre']))
    selected_genres = col1.multiselect("Genres", all_genres, default=all_genres[:3])

    movie_stats["year"] = movie_stats["title"].apply(
        lambda x: int(re.search(r"\((\d{4})\)", x).group(1)) if re.search(r"\((\d{4})\)", x) else None
    )
    years = movie_stats['year'].dropna().astype(int)
    selected_years = col2.slider("Release Year", min_value=int(years.min()), max_value=int(years.max()), value=(1990, 2018))

    selected_rating = col1.slider("Minimum Average Rating", 0.5, 5.0, 3.5, 0.1)
    selected_votes = col2.slider("Minimum Number of Votes", 0, int(movie_stats['rating_count'].max()), 50, 10)

    tag_options = sorted(tags_df['tag'].unique())
    selected_tags = col3.multiselect("Tags to Include", tag_options)

    keyword = col3.text_input("Keyword in Title")

# Search button
if st.button("🔍 Search"):
    with st.spinner("🔄 Searching movies based on your filters..."):
        # === Filter movies ===
        filtered_movies = movie_stats.copy()

        genre_cache = {}

        def get_genres_with_cache(movie_id: int):
            if movie_id in genre_cache:
                return genre_cache[movie_id]
            try:
                movie = client.get_movie(movie_id)
                genres = movie.genres
                genre_cache[movie_id] = genres
                return genres
            except Exception:
                return None

        filtered_movies['genre'] = filtered_movies['movieId'].apply(get_genres_with_cache)

        if selected_genres:
            filtered_movies = filtered_movies[filtered_movies['genre'].apply(
                lambda g: any(genre in g for genre in selected_genres))]

        filtered_movies = filtered_movies[
            (filtered_movies['avg_rating'] >= selected_rating) &
            (filtered_movies['rating_count'] >= selected_votes) &
            (filtered_movies['year'].between(*selected_years))
        ]

        if keyword:
            filtered_movies = filtered_movies[filtered_movies['title'].str.contains(keyword, case=False)]

        if selected_tags:
            def has_tags(row):
                return all(tag in row.get('tags', '') for tag in selected_tags)
            if 'tags' in filtered_movies.columns:
                filtered_movies = filtered_movies[filtered_movies.apply(has_tags, axis=1)]

        # === Summary metrics ===
        st.markdown("## 🔎 Search Results")
        k1, k2, k3 = st.columns(3)
        k1.metric("🎞️ Number of Movies", len(filtered_movies))
        k2.metric("⭐ Average Rating", f"{filtered_movies['avg_rating'].mean():.2f}" if not filtered_movies.empty else "N/A")
        k3.metric("👥 Average Votes", f"{filtered_movies['rating_count'].mean():.0f}" if not filtered_movies.empty else "N/A")

        # === Display movie cards ===
        def generate_card(movie):
            movie_id = int(movie['movieId'])  # Ensure key is an int
            imdb_url = meta_links.get(movie_id, {}).get('imdb_url', "#")
            poster_url = meta_links.get(movie_id, {}).get('poster_url', "https://via.placeholder.com/120x180?text=No+Image")

            with st.container():
                cols = st.columns([1, 4])
                with cols[0]:
                    st.image(poster_url, width=120)
                with cols[1]:
                    st.markdown(
                        f"""<h4><a href="{imdb_url}" target="_blank" rel="noopener noreferrer">{movie['title']}</a></h4>""",
                        unsafe_allow_html=True
                    )
                    st.markdown(f"**Genres:** {movie['genre']}")
                    st.markdown(f"**Average Rating:** ⭐ {movie['avg_rating']:.2f}")
                    st.markdown(f"**Number of Ratings:** {movie['rating_count']}")
                    if 'tags' in movie:
                        st.markdown(f"**Tags:** *{movie['tags']}*")
                st.divider()

        # Show top movies (up to 30)
        if filtered_movies.empty:
            st.warning("No movies match your filters.")
        else:
            for _, movie in filtered_movies.sort_values("avg_rating", ascending=False).iterrows():
                generate_card(movie)

else:
    st.info("🧭 Set your filters, then click **Search** to explore the movies.")
