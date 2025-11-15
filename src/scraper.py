import time
import requests
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class EstateWebScraper():
    def __init__(self, params):
        # Initialize the web driver and set the necessary locators and parameters
        self.driver = webdriver.Chrome(service=params.get('service'), options=params.get('options'))
        self.pagination_locator = params.get('pagination_locator')
        self.pages_locator = params.get('pages_locator')
        self.container_locator = params.get('container_locator')
        self.estate_locator = params.get('estate_locator')
        self.title_locator = params.get('title_locator')
        self.address_locator = params.get('address_locator')
        self.price_locator = params.get('price_locator')
        self.next_button_locator = params.get('next_button_locator')
        self.exchange_rate_url = params.get('exchange_rate_url')
        self.exchange_rate_locator = params.get('exchange_rate_locator')
        self.price_per_sqm_locator = params.get('price_per_sqm_locator')
        self.rooms_locator = params.get('rooms_locator')
        self.sqm_locator = params.get('sqm_locator')
        self.url = params.get('url')
        self.exchange_rate = None
        self.wait = WebDriverWait(self.driver, 10)
    
    def get_exchange_rate(self):
        # Retrieve the exchange rate from provided URL
        try:
            with requests.get(self.exchange_rate_url) as response:
                soup = BeautifulSoup(response.content, 'html.parser')
            rate = soup.select_one(self.exchange_rate_locator).text
            self.exchange_rate = round(float(re.sub(r'1 EURO = (\d+\.\d+) Lei', r'\1', rate)), 2)
            return self.exchange_rate
        except requests.RequestException as e:
            raise ValueError(f"Error retrieving exchange rate: {str(e)}")
    
    def _click_accept_button(self):
        # Find and click the Accept button to accept the cookies
        try:
            accept_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_button.click()
        except Exception as e:
            raise ValueError(f"Error: Could not find or click Accept button. {str(e)}")
    
    def _get_pagination(self):
        # Get the total number of pages in the pagination
        try:
            pagination = self.wait.until(
                EC.presence_of_element_located((By.XPATH, self.pagination_locator)))
            pages = pagination.find_elements(By.XPATH, self.pages_locator)
            last_page = 1 if len(pages) == 0 else int(pages[-1].text)
            return last_page
        except Exception as e:
            raise ValueError(f"Error: Failed to get pagination. {str(e)}")
    
    def _get_estates(self):
        # Get the list of estates from the current page
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            estates_container = self.wait.until(
                EC.presence_of_element_located((By.XPATH, self.container_locator)))
            estates_from_page = estates_container.find_elements(By.XPATH, self.estate_locator)
            return estates_from_page
        except Exception as e:
            raise ValueError(f"Error: Failed to get estates. {str(e)}")
        
    def _get_text(self, estate, locator):
        # Retrieve the text from a specific element
        try:
            return estate.find_element(By.XPATH, locator).text
        except Exception as e:
            raise ValueError(f"Error retrieving text from element: {str(e)}")

    def _extract_estate_data(self, estate):
        # Extract the relevant data from an estate
        title = self._get_text(estate, self.title_locator)
        address = self._get_text(estate, self.address_locator)
        price = self._get_text(estate, self.price_locator)
        if "RON" in price:
            price = round((int(re.sub(r"\D", "", price))/self.exchange_rate),2)
        else:
            price = float(re.sub(r"\D", "", price))
        rooms = int(re.sub(r"\D", "", self._get_text(estate, self.rooms_locator)))
        sqm = float(re.sub(r"[^\d\.]", "", self._get_text(estate, self.sqm_locator)))
        if self.price_per_sqm_locator:
            price_per_sqm = self._get_text(estate, self.price_per_sqm_locator)
            if "RON/m²" in price_per_sqm:
                price_per_sqm = round((float(re.sub(r'[^\d,]', '', price_per_sqm).replace(',', '.'))/self.exchange_rate),2)
            else:
                price_per_sqm = float(re.sub(r"\D", "", price_per_sqm))
        else:
            price_per_sqm = round(price / sqm, 2)
        return [title, address, price, price_per_sqm, rooms, sqm]
  
    def _click_next_page(self):
        # Click the Next button to navigate to the next page
        try:
            next_page = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, self.next_button_locator)))
            self.driver.execute_script("arguments[0].click();", next_page)
        except Exception as e:
            raise ValueError(f"Could not find or click Next button. {str(e)}")

    def scrape_url(self):
        # Scrape the data from the provided URL
        self.get_exchange_rate()
        self.driver.get(self.url)
        self._click_accept_button()
        last_page = self._get_pagination()
        data = []
        if last_page == 1:
            estates_from_page = self._get_estates()
            for estate in estates_from_page:
                row = self._extract_estate_data(estate)
                data.append(row)
        else:
            for page in range(1, last_page + 1):
                try:
                    estates_from_page = self._get_estates()
                    for estate in estates_from_page:
                        row = self._extract_estate_data(estate)
                        data.append(row)
                    if page < last_page:
                        self._click_next_page()
                except Exception as e:
                    print(f'Error on page {page}. Refreshing: {e}')
                    self.driver.refresh()
        self.driver.quit()
        df = pd.DataFrame(data, columns=['title', 'address', 'price', 'price_per_sqm', 'rooms', 'sqm']).drop_duplicates()
        df.index = range(1, len(df) + 1)
        return df