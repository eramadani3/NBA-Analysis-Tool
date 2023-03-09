from tkinter import *
from tkinter import filedialog
from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import customtkinter

class Model:
    def __init__(self):
# Load teams file
        teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
        # Load players file
        players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)

        # Get team ID based on team name
        def get_team_id(team_name):
            for team in teams:
                if team['teamName'] == team_name:
                    return team['teamId']
            return -1

        # Get player ID based on player name
        def get_player_id(first, last):
            for player in players:
                if player['firstName'] == first and player['lastName'] == last:
                    return player['playerId']
            return -1


        

class View(customtkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Create a tkinter window
        root = customtkinter.CTk()
        root.geometry
        root.title("NBA Shot Chart")

        # Create input fields and labels
        self.player_name_label = Label(root, text="Player Name (First, Last): ")
        self.player_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.player_name_entry = Entry(root)
        self.player_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.team_name_label = Label(root, text="(Team Name City): ")
        self.team_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.team_name_entry = Entry(root)
        self.team_name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.year_label = Label(root, text="Year (YYYY-YY): ")
        self.year_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.year_entry = Entry(root)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        # Create a button to trigger data retrieval and visualization
        self.visualize_button = Button(root, text="Generate Shot Chart", command=self.create_plot)
        self.visualize_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Start the tkinter main loop
        root.mainloop()
    def create_court(self,ax, color):
        # Short corner 3PT lines
        ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
        ax.plot([220, 220], [0, 140], linewidth=2, color=color)

        # 3PT Arc
        ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))

        # Lane and Key
        ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
        ax.plot([80, 80], [0, 190], linewidth=2, color=color)
        ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
        ax.plot([60, 60], [0, 190], linewidth=2, color=color)
        ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
        ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))

        # Rim
        ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))

        # Backboard
        ax.plot([-30, 30], [40, 40], linewidth=2, color=color)

        # Remove ticks
        ax.set_xticks([])
        ax.set_yticks([])

        # Set axis limits
        ax.set_xlim(-250, 250)
        ax.set_ylim(0, 470)

        return ax
    def create_plot(self):
        # Get user input from GUI
        player_name = self.player_name_entry.get()
        team_name = self.team_name_entry.get()
        year = self.year_entry.get()

        # Get player ID
        first, last = player_name.split()
        player_id = Model.get_player_id(first, last)

        # Create JSON request
        shot_json = shotchartdetail.ShotChartDetail(
            team_id=Model.get_team_id(team_name),
            player_id=player_id,
            context_measure_simple='PTS',
            season_nullable=year,
            season_type_all_star='Regular Season')

        shot_data = json.loads(shot_json.get_json())

        relevant_data = shot_data['resultSets'][0]
        headers = relevant_data['headers']
        rows = relevant_data['rowSet']

        # Create pandas DataFrame
        player_data = pd.DataFrame(rows)
        player_data.columns = headers

        mpl.rcParams['font.family'] = 'Avenir'
        mpl.rcParams['font.size'] = 18
        mpl.rcParams['axes.linewidth'] = 2
        # Create figure and axes
        fig = plt.figure(figsize=(4, 3.76))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_title(f"{player_name} ({year}) Stats")

        # Draw court
        ax = self.create_court(ax, 'black')

        # Plot hexbin of shots
        ax.hexbin(player_data['LOC_X'], player_data['LOC_Y'] + 60, gridsize=(30, 30), extent=(-300, 300, 0, 940), bins='log', cmap='Reds')

        # Annotate player name and season
        ax.text(0, 1.05, f'{player_name}\n{year} Regular Season', transform=ax.transAxes, ha='left', va='baseline')

        # save the figure with a filename based on the player name and year
        filename = f"{player_name}_{year}_stats.png"
        fig.savefig(filename)
        plt.show()
    
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view