# src/config.py

# --- Scraper Configuration (for code review) ---
SELL_URL = "https://www.storia.ro/ro/rezultate/vanzare/apartament/locatii-multiple?distanceRadius=0&market=ALL&locations=%5Bbucuresti%2Ccluj%2Fcluj--napoca%2Ciasi%2Fiasi%2Ctimis%2Ftimisoara%5D&viewType=listing"
RENT_URL = "https://www.storia.ro/ro/rezultate/inchiriere/apartament/locatii-multiple?market=ALL&distanceRadius=0&locations=%5Bbucuresti%2Ccluj%2Fcluj--napoca%2Ciasi%2Fiasi%2Ctimis%2Ftimisoara%5D&by=DEFAULT&direction=DESC&viewType=listing"
EXCHANGE_RATE_URL = "https://www.cursbnr.ro/"

# Note: The ChromeDriver path is machine-specific and should be managed by the user.
# We keep locators here to show the original scraping logic.

# --- Locators ---
PAGINATION_LOCATOR = "//nav[@data-cy='pagination']"
PAGES_LOCATOR = ".//button[@aria-current='false']"
CONTAINER_LOCATOR = "//div[contains(@data-cy, 'organic')]"
ESTATE_LOCATOR = ".//li[@data-cy='listing-item']"
TITLE_LOCATOR = ".//h3[contains(@data-cy, 'title')]"
ADDRESS_LOCATOR = ".//p[@class='css-14aokuk e1ualqfi4']"
PRICE_LOCATOR = ".//span[@class='css-1on0450 ei6hyam2'][1]"
PRICE_PER_SQM_LOCATOR = ".//span[@class='css-1on0450 ei6hyam2'][2]"
SELLING_ROOMS_LOCATOR = ".//span[@class='css-1on0450 ei6hyam2'][3]"
RENTING_ROOMS_LOCATOR = ".//span[@class='css-1on0450 ei6hyam2'][2]"
SELLING_SQM_LOCATOR = ".//span[@class='css-1on0450 ei6hyam2'][4]"
RENTING_SQM_LOCATOR = ".//span[@class='css-1on0450 ei6hyam2'][3]"
NEXT_BUTTON_LOCATOR = "//button[contains(@data-cy, 'next-page')]"
EXCHANGE_RATE_LOCATOR = "div.value:-soup-contains('EURO'):-soup-contains('Lei')"


# --- Analysis Configuration ---
COUNTY_LIST = ['Cluj', 'Bucuresti', 'Timis', 'Iasi']
CITY_LIST = ['Cluj-Napoca', 'Bucuresti', 'Timisoara', 'Iasi']
SHORT_NAME_LIST = ['cj', 'b', 'tm', 'is']