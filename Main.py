import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.safari.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pd.set_option('display.max_columns', None)
url = 'https://www.nba.com/stats/leaders?Season=2012-13&PerMode=Totals'

driver = webdriver.Safari()
# Set up Selenium webdriver

driver.get(url)

try:
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

    # Extract the table data
    for row in rows[1:]:
        cells = row.find_all('td')
        row_data = []
        for cell in cells:
            row_data.append(cell.text.strip())
        data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    print(df)
finally:
    # Quit the driver
    driver.quit()
