from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def scrape_page(driver, csv_writer):
    # Wait for the table to be present
    table = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="htab"]//table[@class="eqs table-scroll"]'))
    )

    # Find all tr rows
    tr_elements = table.find_elements(By.XPATH, './/tbody/tr')

    # Extract and write each row to the CSV file
    for tr in tr_elements:
        row_data = [td.text for td in tr.find_elements(By.TAG_NAME, 'td')]
        csv_writer.writerow(row_data)

# Set up the WebDriver
website = "https://www.emsc-csem.org/Earthquake_information/"
driver = webdriver.Chrome()
driver.get(website)

try:
    # Create a CSV file and write header
    with open('eq_data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ["Citizen response", "Citizenresp","Citizen resp", "Date & Time", "Latitude", "Longitude", "Depth","empty", "Magnitude", "Region"]
        csv_writer.writerow(header)

        # Iterate through multiple pages
        for page in range(1, 1000):  # Change the range based on the total number of pages
            # Perform scraping for the current page
            print(page)
            scrape_page(driver, csv_writer)

            # Click on the next page button
            next_button = driver.find_element(By.XPATH, '//div[@class="pag spes spes1"]')
            next_button.click()

            # Optional: You may need to add a delay here to allow the page to load
            time.sleep(15)

finally:
    driver.quit()
