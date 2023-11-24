import requests

def get_weather_data(location):
    # Logic to fetch weather data from an external API
    response = requests.get('API_URL', params={'location': location})
    return response.json()

def get_weather_forecast(location):
    # Logic to fetch weather forecast from an external API
    response = requests.get('API_URL', params={'location': location})
    return response.json()

def get_weather_alerts(location):
    # Logic to fetch weather alerts from an external API
    
    response = requests.get('API_URL', params={'location': location})
    return response.json()

