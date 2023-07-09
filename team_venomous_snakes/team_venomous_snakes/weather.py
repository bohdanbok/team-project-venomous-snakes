import requests

BASE_URL = "api.openweathermap.org/data/2.5/weather?"
API_KEY = '54bd96a092227d0950a024fdc4e6171e'


def what_weather():

    city = input("Please enter city: ")
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = round(main['temp'] - 273.15)
        temp_feel_like = round(main['feels_like'] - 273.15)
        humidity = main['humidity']
        pressure = main['pressure']
        weather_report = data['weather']
        wind_report = data['wind']

        print(f"{city:-^35}")
        print(f"Temperature: {temperature}")
        print(f"Feel Like: {temp_feel_like}")
        print(f"Humidity: {humidity} %")
        print(f"Weather Report: {weather_report[0]['description']}")
    else:
        # showing the error message
        print("Error in the HTTP request")


if __name__ == "__main__":
    what_weather()
