import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

def load_parquet_data(file_name):
    file_path = Path(__file__).resolve().parent.parent / "output" / file_name
    return pd.read_parquet(file_path)

# Define the output directory
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

st.title("🏷️ Tags Insights")

# Load datasets
tag_df = load_parquet_data("user_tag_stats.parquet")
tags_good_rating_df = load_parquet_data("tags_good_rating.parquet")
tags_compare_df = load_parquet_data("tags_compare.parquet")
tags_by_genre_df = load_parquet_data("tags_by_genre.parquet")

# Chart 1: Top tags used by users
fig_user_tags = px.bar(
    tag_df, x="count", y="tag", orientation="h",
    title="Top Tags Used by Users",
    labels={"count": "Number of Uses", "tag": "Tag"},
    color="count", color_continuous_scale="viridis"
)
fig_user_tags.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)

# Chart 2: Tags in well-rated movies
fig_good_tags = px.bar(
    tags_good_rating_df,
    x="count",
    y="tag",
    orientation="h",
    title="Most Frequent Tags in Well-Rated Movies (Rating ≥ 4)",
    labels={"count": "Number of Occurrences", "tag": "Tag"},
    color="count",
    color_continuous_scale="viridis"
)
fig_good_tags.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)

# Chart 3: Comparison of tags in well-rated vs poorly rated movies
tags_compare_melted = tags_compare_df.melt(
    id_vars="tag",
    value_vars=["count_good", "count_bad"],
    var_name="Type",
    value_name="count"
)
fig_compare_tags = px.bar(
    tags_compare_melted,
    x="count",
    y="tag",
    color="Type",
    barmode="group",
    title="Tag Comparison: Well-Rated vs Poorly Rated Movies",
    labels={"count": "Number of Occurrences", "tag": "Tag"},
    height=500
)
fig_compare_tags.update_layout(yaxis={'categoryorder': 'total ascending'})

# Show the first three charts stacked vertically with spacing
st.plotly_chart(fig_user_tags, use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

st.plotly_chart(fig_good_tags, use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

st.plotly_chart(fig_compare_tags, use_container_width=True)

st.divider()

# Prepare data for final chart
top_tags_by_genre = tags_by_genre_df.groupby("genre").apply(
    lambda g: g.nlargest(3, 'count')
).reset_index(drop=True)
top_tags_by_genre["tag_label"] = top_tags_by_genre["tag"] + " (" + top_tags_by_genre["genre"] + ")"

# Multi-select widget for genres
all_genres = sorted(top_tags_by_genre["genre"].unique())
selected_genres = st.multiselect(
    "🎯 Select genres to display:",
    options=all_genres,
    default=all_genres
)

# Reactive dataframe filtered by selected genres
filtered_tags = top_tags_by_genre[top_tags_by_genre["genre"].isin(selected_genres)]

# Final chart: Top 3 tags by genre
fig_tags_by_genre = px.bar(
    filtered_tags.sort_values("count"),
    x="count",
    y="tag_label",
    color="genre",
    orientation="h",
    title="Top 3 Most Used Tags by Genre",
    labels={"count": "Number of Occurrences", "tag_label": "Tag (Genre)"},
    height=800
)
fig_tags_by_genre.update_layout(yaxis=dict(categoryorder='total ascending'))

# Display final chart full width
st.plotly_chart(fig_tags_by_genre, use_container_width=True)
