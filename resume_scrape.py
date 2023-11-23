from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv

def navigate_to_page(driver, target_page):
    for page in range(1, target_page + 1):
        # Click on the next page button
        next_button = driver.find_element(By.XPATH, '//div[@class="pag spes spes1"]')
        next_button.click()

        # Use WebDriverWait for the next button to be clickable
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="pag spes spes1"]')))
        print(f"Navigating to page {page}")

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
    with open('earthquake_data.csv', 'a', newline='') as csvfile:  # Use 'a' for append mode
        csv_writer = csv.writer(csvfile)

        # Get the last successfully scraped page number from a file or any other persistence method
        last_scraped_page = 4385  # Replace this with the actual last scraped page number

        # Navigate to the last successfully scraped page
        navigate_to_page(driver, last_scraped_page)

        # Start scraping from the last successfully scraped page
        for page in range(last_scraped_page, 8804):  # Adjust the range based on the total number of pages
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
