import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pd.set_option('display.max_columns', None)
url = 'https://www.nba.com/stats/leaders?Season=2012-13&PerMode=Totals'

driver = webdriver.Chrome()
chrome_options = driver.ChromeOptions()
chrome_options.binary_location = "/Applications/Sidekick.app/Contents/MacOS/Sidekick"
driver = driver.Chrome(options=chrome_options)
# Set up Selenium webdriver

driver.get(url)

try:
    # Wait for the table to load
    table_xpath = "//table[@class='table']/tbody"
    table = driver(driver, 10).until(EC.presence_of_element_located((By.XPATH, table_xpath)))
    
    # Extract the table data using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.select('table.table tbody tr')
    
    # Print the data
    for row in rows:
        cells = row.find_all('td')
        for cell in cells:
            print(cell.text.strip())

finally:
    # Quit the driver
    driver.quit()
