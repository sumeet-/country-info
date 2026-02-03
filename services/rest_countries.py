import requests

# Function to fetch country data from REST Countries API
def fetch_country_data(country_name: str) -> dict:
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Error fetching data for country: {country_name}")

    data = response.json()
    if not data:
        raise ValueError(f"No data found for country: {country_name}")

    return data if data else {}  # Return the first matching country data