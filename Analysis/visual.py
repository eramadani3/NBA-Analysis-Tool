import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class NBAStatsGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NBA Stats Viewer")
        self.create_widgets()
        
    def create_widgets(self):
        # Create label and entry for player name input
        player_label = ttk.Label(self.root, text="Enter player name:")
        player_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.player_entry = ttk.Entry(self.root)
        self.player_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Create label and combobox for stat selection
        stat_label = ttk.Label(self.root, text="Select a stat to plot:")
        stat_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.stat_combobox = ttk.Combobox(self.root, values=["PTS","FGM","FGA","FG%","3PM","3PA","3P%","FTM","FTA","FT%","OREB","DREB","REB","AST","STL","BLK","TOV","PF","EFF","AST/TOV","STL/TOV"])
        self.stat_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.stat_combobox.current(0)
        
        # Create button to show stats
        show_button = ttk.Button(self.root, text="Show Stats", command=self.show_stats)
        show_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        # Create frame to hold chart
        self.chart_frame = ttk.Frame(self.root)
        self.chart_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(2, weight=1)


    
    def show_stats(self):
        # Path to the directory containing the CSV files
        dirname = '../NBA Data'

        # Read the all_seasons_stats.csv file
        filename = 'all_seasons_stats.csv'
        filepath = os.path.join(dirname, filename)
        player_df = pd.read_csv(filepath)

        # Get player input from user
        player_name = self.player_entry.get()

        # Get the selected stat column from the combobox
        stat_column = self.stat_combobox.get()

        if not stat_column:
            # Show an error message if no stat column is selected
            messagebox.showerror("Error", "Please select a stat column.")
            return

        # Filter dataframe to include only the data for the specified player
        player_data = player_df.loc[player_df['Player'] == player_name]

        # Get the values for the selected stat column
        stat_values = player_data[stat_column]

        # Create the bar chart
        fig, ax = plt.subplots()
        ax = sns.barplot(x=player_data['SEASON'], y=stat_values)
        ax.set_title(f"{player_name} {stat_column} by Season")
        ax.set_xlabel("Season")
        ax.set_ylabel(stat_column)

        # Create FigureCanvasTkAgg widget to embed chart in GUI
        chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    nba_gui = NBAStatsGUI()
    nba_gui.root.mainloop()
