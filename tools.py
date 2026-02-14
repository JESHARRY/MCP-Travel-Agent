import os
import requests
from langchain.tools import tool

@tool
def get_weather(city: str):
    """Fetches real-time weather and forecast for a given city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") != 200:
        return "Weather data not available."
    
    weather_desc = response['weather'][0]['description']
    temp = response['main']['temp']
    return f"Current weather in {city}: {weather_desc}, Temperature: {temp}°C."

@tool
def search_travel_info(query: str):
    """Searches for real-time flights, hotels, and cultural info using Search API."""
    # Note: In a production app, you'd use Skyscanner/Booking APIs here.
    # For this lab, we use a Search Tool to simulate flight/hotel data.
    api_key = os.getenv("SERPER_API_KEY")
    url = "https://google.serper.dev/search"
    payload = {"q": query}
    headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers).json()
    
    results = [item['snippet'] for item in response.get('organic', [])[:3]]
    return "\n".join(results)