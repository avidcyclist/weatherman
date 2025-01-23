import requests

# Replace with your API key
api_key = '850ab9bf60af46e77034a8f578e1c8eb'
lat = 40.4842  # Latitude for Bloomington
lon = -88.9937  # Longitude for Bloomington
url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely&units=metric&appid={api_key}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("API key is working correctly.")
    print(data)
else:
    print(f"Failed to fetch data: {response.status_code}")
    print(response.text)