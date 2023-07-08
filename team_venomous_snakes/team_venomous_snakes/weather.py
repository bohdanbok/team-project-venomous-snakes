import requests

BASE_URL = "api.openweathermap.org/data/2.5/weather?"
API_KEY = '54bd96a092227d0950a024fdc4e6171e'


def what_weather():

    city = input("Please enter city: ")
    url = BASE_URL + "q=" + city + "uk&appid=" + API_KEY
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = main['temp']
        temp_feel_like = main['feels_like']
        humidity = main['humidity']
        pressure = main['pressure']
        weather_report = data['weather']
        wind_report = data['wind']

        print(f"{city:-^35}")
        print(f"City ID: {data['id']}")
        print(f"Temperature: {temperature}")
        print(f"Feel Like: {temp_feel_like}")
        print(f"Humidity: {humidity}")
        print(f"Pressure: {pressure}")
        print(f"Weather Report: {weather_report[0]['description']}")
        print(f"Wind Speed: {wind_report['speed']}")
        print(f"Time Zone: {data['timezone']}")
    else:
        # showing the error message
        print("Error in the HTTP request")


if __name__ == "__main__":
    what_weather()
