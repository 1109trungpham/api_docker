import httpx
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from datetime import datetime


class WeatherResponse(BaseModel):
    header: List[str]
    value: List[List[float]]

### Tạo API FastAPI
app = FastAPI()

@app.get("/weather", response_model=WeatherResponse)
async def get_weather(
    lon: float = Query(..., description="Longitude"),
    lat: float = Query(..., description="Latitude"),
    start_year: int = Query(..., description="Start year"),
    end_year: int = Query(..., description="End year")
):
    
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "longitude": lon,
        "latitude": lat,
        "start_date": f"{start_year}-01-01",
        "end_date":   f"{end_year}-12-31",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "UTC"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url=BASE_URL, params=params)


    if response.status_code != 200:
        return {"error": "Failed to fetch weather data"}


    raw_data = response.json().get("daily", {})
    if not raw_data:
        return WeatherResponse(header=[], value=[])


    header = ["day", "month", "year", "doy", "max_temp", "min_temp", "precip"]
    value = []
    for i, date_str in enumerate(raw_data["time"]):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        value.append([
            date_obj.day,                       # "day"
            date_obj.month,                     # "month"
            date_obj.year,                      # "year"
            date_obj.timetuple().tm_yday,       # "doy"
            raw_data["temperature_2m_max"][i],  # "max_temp"
            raw_data["temperature_2m_min"][i],  # "min_temp"
            raw_data["precipitation_sum"][i]    # "precip"
        ])

    return WeatherResponse(header=header, value=value)
