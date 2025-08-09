import pandas as pd

netflix = pd.read_csv("data/netflix_titles.csv")
disney = pd.read_csv("data/disney_plus_titles.csv")
amazon = pd.read_csv("data/amazon_prime_titles.csv")

netflix["platform"] = "Netflix"
disney["platform"] = "Disney+"
amazon["platform"] = "Amazon Prime"


common_columns = ["title", "type", "director", "cast", "country", "date_added", "release_year", "rating", "duration", "listed_in", "description", "platform"]

#merge
combined_df = pd.concat([
    netflix[common_columns],
    disney[common_columns],
    amazon[common_columns]
], ignore_index=True)

combined_df["title"] = combined_df["title"].str.strip()
combined_df.drop_duplicates(subset=["title", "platform"], inplace=True)

combined_df.insert(0, 'show_id', ['S' + str(i) for i in range(1, len(combined_df)+1)])

# save
combined_df.to_csv("data/combined_titles.csv", index=False)
