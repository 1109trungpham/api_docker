import numpy as np


def create_location(type_location:str, size:int):
    str = ''
    if type_location == 'lat':
        # lat: vĩ độ [-90, 90]
        float_range = np.random.uniform(-90, 90, size)
        for num in float_range:
            num = float("{:.3f}".format(num))
            str = str+f"{num}"+","
        return str[:-2]
    elif type_location == 'lon':
        # lon: kinh độ [-180, 180]
        float_range = np.random.uniform(-180, 180, size)
        for num in float_range:
            num = float("{:.2f}".format(num))
            str = str+f"{num}"+","
        return str[:-2]
    else:
        raise Exception(f'type_location: lat|lon , Not: {type_location}')
         

lon = create_location('lon', 1)
lat = create_location('lat', 1)
my_api_url = f'http://127.0.0.1:8000/weather?lon={lon}&lat={lat}&start_year=2010&end_year=2020'
meteo_url  = f'https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date=2010-01-01&end_date=2020-12-31&hourly=temperature_2m'
print(my_api_url)
# print(meteo_url)

