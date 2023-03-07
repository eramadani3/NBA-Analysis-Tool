import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Path to the directory containing the CSV files
dirname = '../NBA Data'

# Read the all_seasons_stats.csv file
filename = 'all_seasons_stats.csv'
filepath = os.path.join(dirname, filename)
player_df = pd.read_csv(filepath)

# Get player input from user
player_name = input("Enter player name: ")

# Filter dataframe to include only the data for the specified player
player_data = player_df.loc[player_df['Player'] == player_name]

# Get the number of games played by the player each season
games_played = player_data.set_index('SEASON')['GP']

# Get the points scored by the player each season
points_scored = player_data.pivot(index='SEASON', columns='TEAM', values='PTS')

# Create the bar chart
ax = points_scored.plot(kind='bar', title=f"{player_name} Scoring by Season")
ax.set_ylabel("Points")
ax.set_xlabel("Season")

# Add the number of games played as a text label above each bar
for i, v in enumerate(games_played):
    ax.text(i, points_scored.iloc[i].max(), f"{int(v)} GP", horizontalalignment='center', fontweight='bold')

plt.show()
