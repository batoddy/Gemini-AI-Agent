# tools/weather_tool.py

from typing import Any, Dict

import requests

from app.exceptions import ToolValidationError
from tools.base_tool import BaseTool


class WeatherTool(BaseTool):
    def __init__(self) -> None:
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"

    @property
    def name(self) -> str:
        return "weather"

    @property
    def description(self) -> str:
        return "Gets the current weather of a city."

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "city": {
                        "type_": "STRING",
                        "description": "City name. Example: Istanbul",
                    }
                },
                "required": ["city"],
            },
        }

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        city = kwargs.get("city")

        if not city or not isinstance(city, str):
            raise ToolValidationError(
                "The 'city' argument is required and must be a string."
            )

        city = city.strip()
        if not city:
            raise ToolValidationError("The city name cannot be empty.")

        try:
            geo_response = requests.get(
                self.geocoding_url,
                params={"name": city, "count": 1, "language": "en", "format": "json"},
                timeout=10,
            )
            geo_response.raise_for_status()
            geo_data = geo_response.json()
        except requests.RequestException as e:
            return {
                "status": "error",
                "tool": self.name,
                "error": f"Could not get city coordinates: {e}",
            }

        results = geo_data.get("results")
        if not results:
            return {
                "status": "error",
                "tool": self.name,
                "error": f"No city found for '{city}'.",
            }

        place = results[0]
        latitude = place["latitude"]
        longitude = place["longitude"]
        city_name = place["name"]
        country = place.get("country", "Unknown")

        try:
            weather_response = requests.get(
                self.weather_url,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current_weather": "true",
                    "timezone": "auto",
                },
                timeout=10,
            )
            weather_response.raise_for_status()
            weather_data = weather_response.json()
        except requests.RequestException as e:
            return {
                "status": "error",
                "tool": self.name,
                "error": f"Could not get weather data: {e}",
            }

        current_weather = weather_data.get("current_weather")
        if not current_weather:
            return {
                "status": "error",
                "tool": self.name,
                "error": "Weather data is not available.",
            }

        weather_code = current_weather.get("weathercode")
        weather_description = self._get_weather_description(weather_code)

        return {
            "status": "success",
            "tool": self.name,
            "city": city_name,
            "country": country,
            "temperature_c": current_weather.get("temperature"),
            "wind_speed_kmh": current_weather.get("windspeed"),
            "weather_code": weather_code,
            "weather_description": weather_description,
            "observation_time": current_weather.get("time"),
        }

    def _get_weather_description(self, code: Any) -> str:
        try:
            code = int(code)
        except (TypeError, ValueError):
            return "Unknown"

        if code == 0:
            return "Sunny"
        elif code in [1, 2, 3]:
            return "Cloudy"
        elif code in [45, 48]:
            return "Foggy"
        elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
            return "Rainy"
        elif code in [71, 73, 75, 77, 85, 86]:
            return "Snowy"
        elif code in [95, 96, 99]:
            return "Stormy"
        else:
            return "Unknown"
