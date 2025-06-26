import requests

def get_pvwatts_data(lat, lon, system_capacity_kW=1, tilt=30, azimuth=180):
    api_key = "iCNqSptJhc2arfzuIKuvAySXbSBmMr0uM36Ar7Tb"
    url = "https://developer.nrel.gov/api/pvwatts/v6.json"
    
    params = {
        "api_key": api_key,
        "lat": lat,
        "lon": lon,
        "system_capacity": system_capacity_kW,
        "tilt": tilt,
        "azimuth": azimuth,
        "array_type": 1,  
        "module_type": 1, 
        "losses": 14,     
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return None

solar_data = get_pvwatts_data(42.6977, 23.3219)

if solar_data:
    print(solar_data)
