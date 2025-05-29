import pandas as pd

# Load the CSV file
links_df = pd.read_csv("links.csv")
print(links_df.info())

# Convert IMDb ID to the format tt0000000
links_df["imdb_id"] = links_df["imdbId"].apply(lambda x: f"tt{x:07d}")
print(links_df.head())

# IMDb URL (movie page)
links_df["imdb_url"] = links_df["imdb_id"].apply(lambda x: f"https://www.imdb.com/title/{x}")
print(links_df.head())

# Poster URL (via OMDb)
OMDB_API_KEY = "877a312e"
links_df["poster_url"] = links_df["imdb_id"].apply(
    lambda x: f"https://img.omdbapi.com/?i={x}&apikey={OMDB_API_KEY}"
)
print(links_df.head())

print(links_df['imdb_url'][0])
print(links_df['poster_url'][0])

# Save to Parquet format
links_df.to_parquet("links_enriched.parquet", index=False)

print("Enriched file saved as output/links_enriched.parquet")
