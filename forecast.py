import requests
from datetime import datetime, timedelta
import os

# API endpoint
API_URL = "https://api.open-meteo.com/v1/forecast"

class WeatherForecast:
    def __init__(self, filename="rain.txt"):
        self.filename = filename
        self.forecasts = {}
        self.load_forecasts()

    def load_forecasts(self):
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as file:
                for line in file:
                    date, forecast = line.strip().split(', ', 1)
                    self.forecasts[date] = forecast

    def save_forecast(self, date, forecast):
        self.forecasts[date] = forecast
        with open(self.filename, "a") as file:
            file.write(f"{date}, {forecast}\n")

    def __setitem__(self, date, forecast):
        self.save_forecast(date, forecast)

    def __getitem__(self, date):
        if date in self.forecasts:
            return self.forecasts[date]
        return None

    def __iter__(self):
        return iter(self.forecasts.keys())

    def items(self):
        for date, forecast in self.forecasts.items():
            yield date, forecast

    def get_forecast(self, date):
        if date in self.forecasts:
            print(f"Result from file for {date}: {self.forecasts[date]}")
            return

        params = {
            "latitude": 51.51,
            "longitude": -0.13,
            "daily": "precipitation_sum",
            "start_date": date,
            "end_date": date,
        }
        response = requests.get(API_URL, params=params)
        data = response.json()

        if "daily" in data and "precipitation_sum" in data["daily"]:
            precipitation = data["daily"]["precipitation_sum"][0]
            if precipitation > 0.0:
                result = f"It will rain, precipitation sum: {precipitation} mm"
            elif precipitation == 0.0:
                result = "It will not rain"
            else:
                result = "I don't know"
            self.save_forecast(date, result)
            print(f"Result for {date}: {result}")
        else:
            print(f"No result available for {date}")

# Instantiate the WeatherForecast class
weather_forecast = WeatherForecast()

# Get the date from the user
while True:
    date_input = input("Enter a date in the format YYYY-MM-DD (or press Enter to use tomorrow's date): ")
    if not date_input:
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        break
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
        date = date_input
        break
    except ValueError:
        print("Invalid date format. Please try again.")

# Get the weather forecast
print("\nRESULT BY CALLING FUNCTION:")
weather_forecast.get_forecast(date)

# Access a specific forecast
print("\nRESULT BY SPECIFIC DATE:")
print(f"Forecast for {date}: {weather_forecast[date]}")

# Print all the dates using the __iter__ method
print("\nRESULTS BY ITERATING DATES:")
print("Dates with stored forecasts:")
for date in weather_forecast:
    print(date)

# Example usage of the class
print("\nRESULT BY GENERATING TUBPLES:")
for date, forecast in weather_forecast.items():
    print(f"{date}: {forecast}")