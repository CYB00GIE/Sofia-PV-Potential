import requests

def get_solar_data(lat, lon):
    url = "https://re.jrc.ec.europa.eu/api/v1/PVcalc"
    params = {
        'lat': lat,
        'lon': lon,
        'outputformat': 'json',
        'pvtechchoice': 'crystsilicon', 
        'losses': 14,  
        'tilt': 30,  
        'azimuth': 180,
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return None

solar_data = get_solar_data(42.6977, 23.3219)

if solar_data:
    print(solar_data)
