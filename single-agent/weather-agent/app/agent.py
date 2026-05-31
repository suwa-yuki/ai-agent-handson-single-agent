# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo
import os
import requests
import google.auth
import google.auth.transport.requests

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


def get_weather(location: str) -> str:
    """Retrieves the real-time and upcoming weather forecast for a specified location.

    This tool first geocodes the location string to latitude/longitude coordinates,
    and then retrieves the forecast details from Google Maps Platform Weather API.

    Args:
        location: The location to get weather information for (e.g., "Seattle, WA", "90210", "Austin, Texas").

    Returns:
        A detailed text summary of the current and upcoming weather forecast, or an error message.
    """
    headers = {"User-Agent": "WeatherAgent/2.0 (contact@weather-agent.local)"}

    # 1. Geocode location using Nominatim (OpenStreetMap)
    geocode_url = "https://nominatim.openstreetmap.org/search"
    geocode_params = {"q": location, "format": "json", "limit": 1}

    try:
        geo_response = requests.get(
            geocode_url, params=geocode_params, headers=headers, timeout=10
        )
        if geo_response.status_code != 200:
            return f"Error: Failed to geocode location '{location}' (HTTP status {geo_response.status_code})."

        geo_data = geo_response.json()
        if not geo_data:
            return (
                f"Error: Could not find the location '{location}'. "
                "Please try specifying a more precise city name, state, or ZIP code (e.g., 'Miami, FL', '90210')."
            )

        display_name = geo_data[0].get("display_name", location)
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

    except Exception as e:
        return f"Error occurred during geocoding: {str(e)}"

    # 2. Authenticate and get Bearer token for Google Maps Weather API
    try:
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        token = credentials.token
    except Exception as e:
        return f"Error authenticating with Google Cloud: {str(e)}"

    # 3. Call Google Maps Platform Weather API
    weather_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": project,
        "User-Agent": "WeatherAgent/2.0",
    }

    # Fetch Current Conditions
    current_url = "https://weather.googleapis.com/v1/currentConditions:lookup"
    current_params = {
        "location.latitude": lat,
        "location.longitude": lon,
        "unitsSystem": "METRIC",
    }

    # Fetch 3-Day Forecast
    forecast_url = "https://weather.googleapis.com/v1/forecast/days:lookup"
    forecast_params = {
        "location.latitude": lat,
        "location.longitude": lon,
        "days": 3,
        "unitsSystem": "METRIC",
    }

    current_data = None
    forecast_data = None

    try:
        # Fetch current conditions
        curr_resp = requests.get(
            current_url, headers=weather_headers, params=current_params, timeout=10
        )
        if curr_resp.status_code == 404:
            return f"Error: The location '{display_name}' is not supported by Google Maps Platform Weather API."
        elif curr_resp.status_code != 200:
            return f"Error: Failed to fetch current weather (HTTP status {curr_resp.status_code}). Detail: {curr_resp.text}"
        current_data = curr_resp.json()

        # Fetch forecast
        fore_resp = requests.get(
            forecast_url, headers=weather_headers, params=forecast_params, timeout=10
        )
        if fore_resp.status_code == 200:
            forecast_data = fore_resp.json()

    except Exception as e:
        return f"Error occurred when retrieving weather data: {str(e)}"

    # 4. Format the output nicely
    result = [f"### Weather Information for: {display_name}\n"]

    # Format Current Conditions
    if current_data:
        cond_text = (
            current_data.get("weatherCondition", {})
            .get("description", {})
            .get("text", "Unknown")
        )
        temp = current_data.get("temperature", {}).get("degrees", "N/A")
        temp_unit = (
            "°C"
            if current_data.get("temperature", {}).get("unit") == "CELSIUS"
            else "°F"
        )
        feels_like = current_data.get("feelsLikeTemperature", {}).get("degrees", "N/A")
        humidity = current_data.get("relativeHumidity", "N/A")
        wind_speed = current_data.get("wind", {}).get("speed", {}).get("value", "N/A")
        wind_unit = (
            "km/h"
            if current_data.get("wind", {}).get("speed", {}).get("unit")
            == "KILOMETERS_PER_HOUR"
            else "mph"
        )
        wind_dir = (
            current_data.get("wind", {}).get("direction", {}).get("cardinal", "N/A")
        )

        result.append("**Current Conditions**:")
        result.append(f"- Weather: {cond_text}")
        result.append(
            f"- Temperature: {temp}{temp_unit} (Feels like {feels_like}{temp_unit})"
        )
        result.append(f"- Relative Humidity: {humidity}%")
        result.append(f"- Wind: {wind_speed} {wind_unit} from {wind_dir}\n")

    # Format Forecast Days
    if forecast_data and "forecastDays" in forecast_data:
        result.append("**Upcoming Forecast**:")
        for day_data in forecast_data["forecastDays"]:
            date_info = day_data.get("displayDate", {})
            date_str = f"{date_info.get('year')}-{date_info.get('month'):02d}-{date_info.get('day'):02d}"
            max_temp = day_data.get("maxTemperature", {}).get("degrees", "N/A")
            min_temp = day_data.get("minTemperature", {}).get("degrees", "N/A")

            day_fc = day_data.get("daytimeForecast", {})
            day_cond = (
                day_fc.get("weatherCondition", {})
                .get("description", {})
                .get("text", "Unknown")
            )

            result.append(f"**{date_str}**:")
            result.append(f"- Temp Range: Min {min_temp}°C / Max {max_temp}°C")
            result.append(f"- Daytime Forecast: {day_cond}")
            result.append("")

    return "\n".join(result)


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are a helpful and knowledgeable weather assistant. "
        "You can check the current and upcoming weather forecast for various locations using your get_weather tool "
        "which is powered by the Google Maps Platform Weather API. "
        "When asked about the weather, use the get_weather tool to look up real-time and forecasted conditions. "
        "Note that some locations may not be supported by the Weather API; if that happens, gracefully explain this limitation "
        "and suggest trying a different location (for example, major US cities)."
    ),
    tools=[get_weather],
)

app = App(
    root_agent=root_agent,
    name="app",
)
