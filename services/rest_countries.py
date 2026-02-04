import logging

import requests


logger = logging.getLogger(__name__)

# Function to fetch country data from REST Countries API
def fetch_country_data(country_name: str) -> dict:
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)

    if response.status_code != 200:
        logger.error(f"Error fetching data for {country_name}: {response.status_code}")
        return {}

    return response.json()