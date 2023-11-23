from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv

def scrape_page(driver, csv_writer):
    # Wait for the table to be present
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="htab"]//table[@class="eqs table-scroll"]'))
    )

    # Find all tr rows
    tr_elements = table.find_elements(By.XPATH, './/tbody/tr')

    # Extract and write each row to the CSV file
    for tr in tr_elements:
        row_data = [td.text for td in tr.find_elements(By.TAG_NAME, 'td')]
        csv_writer.writerow(row_data)

# Set up the WebDriver with headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
website = "https://www.emsc-csem.org/Earthquake_information/"
driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

try:
    # Create a CSV file and write header
    with open('earthquake_data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ["Citizen response", "Citizenresp", "Citizen resp", "Date & Time", "Latitude", "Longitude", "Depth", "empty", "Magnitude", "Region"]
        csv_writer.writerow(header)

        # Iterate through multiple pages
        for page in range(1, 8804):  # Adjust the range based on the total number of pages
            # Perform scraping for the current page
            print(f"Processing page {page}")
            scrape_page(driver, csv_writer)

            # Click on the next page button
            next_button = driver.find_element(By.XPATH, '//div[@class="pag spes spes1"]')
            next_button.click()

            # Use WebDriverWait for the next button to be clickable
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="pag spes spes1"]')))

finally:
    driver.quit()
