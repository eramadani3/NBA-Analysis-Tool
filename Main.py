import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.safari.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pd.set_option('display.max_columns', None)

# Initialize an empty list to hold data from all seasons
all_season_data = []

# Loop through each season from 2010-11 to 2022-23
for year in range(2010, 2023):
    season = str(year) + '-' + str(year+1)[-2:]
    print(f"Processing data for {season} season...")

    # Construct the URL for the NBA stats page for the current season
    url = f"https://www.nba.com/stats/leaders?Season={season}&PerMode=Totals"

    # Set up Selenium webdriver
    driver = webdriver.Safari()

    try:
        # Load the NBA stats page for the current season
        driver.get(url)

        # Wait for the table to load
        table_xpath = "//table[@class='Crom_table__p1iZz']"
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

        data = []
        # Extract the table data using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', {'class': 'Crom_table__p1iZz'})
        rows = table.find_all('tr')

        # Extract the table headers
        header_row = rows[0]
        headers = [th.text.strip() for th in header_row.find_all('th')]
        headers.insert(0, "SEASON") # Add SEASON column header

        # Extract the table data
        for row in rows[1:]:
            cells = row.find_all('td')
            row_data = [season] # Add SEASON value to row data
            for cell in cells:
                row_data.append(cell.text.strip())
            data.append(row_data)

        season_df = pd.DataFrame(data, columns=headers)
        all_season_data.append(season_df)

    finally:
        # Quit the driver
        driver.quit()

# Concatenate data from all seasons into a single dataframe
full_df = pd.concat(all_season_data, ignore_index=True)

# Output the data to a CSV file for all seasons
full_df.to_csv("all_seasons_stats.csv", index=False)
