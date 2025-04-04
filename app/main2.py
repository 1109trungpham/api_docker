import httpx
import asyncio
import time
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import logging

logging.basicConfig(filename="requests.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

class WeatherResponse(BaseModel):
    header: List[str]
    value: List[List[float]]
    locations: List[List[float]]

class WeatherResponseList(BaseModel):
    elapsed_time: float
    results: List[WeatherResponse]

app = FastAPI()

@app.get("/weather", response_model=WeatherResponseList)
async def get_weather(
    lon: str = Query(..., description="Comma-separated longitudes"),
    lat: str = Query(..., description="Comma-separated latitudes"),
    start_year: int = Query(..., description="Start year", ge=1940),
    end_year: int = Query(..., description="End year")
):
    lon_list = lon.split(",")
    lat_list = lat.split(",")

    if len(lon_list) != len(lat_list):
        raise HTTPException(status_code=400, detail="Longitude and latitude lists must have the same length")

    locations = list(zip(lon_list, lat_list))
    results = []
    start_time = time.perf_counter()
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    async with httpx.AsyncClient() as client:
        request_nums=0
        for batch in chunk_list(locations, 100):
            batch_lon = ",".join([lon for lon, lat in batch])
            batch_lat = ",".join([lat for lon, lat in batch])
            params = {
                "longitude": batch_lon,
                "latitude": batch_lat,
                "start_date": f"{start_year}-01-01",
                "end_date": f"{end_year}-12-31",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "UTC"
            }

            response = await client.get(BASE_URL, params=params)
            request_nums+=430

            if response.status_code != 200:
                print(f'⚠️ Batch lỗi: {batch}')
                continue
            
            raw_data_list = response.json()  # Danh sách dữ liệu cho từng vị trí
            print(raw_data_list)
            if not isinstance(raw_data_list, list):  # Kiểm tra dữ liệu hợp lệ
                continue

            for i, raw_data in enumerate(raw_data_list):  # Lặp từng vị trí trong batch
                daily_data = raw_data.get("daily", {})
                if not daily_data:
                    print(f"⚠️ No data for location {batch[i]}")
                    continue

                header = ["day", "month", "year", "doy", "max_temp", "min_temp", "precip"]
                value = []

                for j, date_str in enumerate(daily_data["time"]):
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    value.append([
                        int(date_obj.day),                      # "day"
                        int(date_obj.month),                    # "month"
                        int(date_obj.year),                     # "year"
                        int(date_obj.timetuple().tm_yday),      # "doy"
                        float(daily_data["temperature_2m_max"][j]),  # "max_temp"
                        float(daily_data["temperature_2m_min"][j]),  # "min_temp"
                        float(daily_data["precipitation_sum"][j])    # "precip"
                    ])
            
                results.append(WeatherResponse(header=header, value=value, locations=[batch[i]]))
            await asyncio.sleep(15)
        logging.info(f"Số request đã gửi: {request_nums}")
    
    elapsed_time = time.perf_counter() - start_time
    return WeatherResponseList(elapsed_time=elapsed_time, results=results)

# 1 batch (100 location), sleep(15), 2010-2020, 45s