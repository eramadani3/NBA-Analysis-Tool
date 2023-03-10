# NBA-Analysis-Tool
This Python project uses the tkinter library to visualize NBA player shot charts. The second section plots different statistics for entered player over
the course of their career (NBA Data collected is from 1970-2023).

Installation
This project utilizes tkinter, json, requests, pandas, matplotlib, customtkinter. Importing the necessary libraries is crucial to the script and GUI working

Usage
In the analysis directory, shotChart.py gathers user input for NBA player, NBA team, and year. Then it utilizes the NBA API to gather shot chart data for
the corresponding year and generates a png with a heatmap for the player.

visual.py creates a bar chart for inputted player and selected basketball statistic. The script utilizes all_seasons_stats.csv in the NBA Data directory.
The data available is from 1970-2023. The script plots a players total for given statistic over the course of their career
