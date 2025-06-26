import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)

CORS(app)

logging.basicConfig(level=logging.DEBUG)

NREL_API_KEY = 'iCNqSptJhc2arfzuIKuvAySXbSBmMr0uM36Ar7Tb'
NREL_BASE_URL = 'https://developer.nrel.gov/api/pvwatts/v6.json'

def get_solar_data_from_nrel(lat, lon):
    params = {
        "api_key": NREL_API_KEY,
        "lat": lat,
        "lon": lon,
        "system_capacity": 5,
        "tilt": 30,
        "azimuth": 180,
        "array_type": 1,  
        "module_type": 1, 
        "losses": 14,     
    }

    logging.debug(f"Sending request to NREL API with params: {params}")
    
    response = requests.get(NREL_BASE_URL, params=params)
    
    if response.status_code == 200:
        logging.debug(f"Received response from NREL API: {response.json()}")
        return response.json()
    else:
        logging.error(f"Error from NREL API: {response.status_code} - {response.text}")
        return None

def adjust_energy_output(solar_data, roof_area, panel_size=1.7):
    energy_output = solar_data['outputs']
    
    num_panels = roof_area // panel_size  # Floor division
    logging.debug(f"Calculated number of panels that fit on the roof: {num_panels}")
    
    adjusted_ac_monthly = [energy * num_panels for energy in energy_output['ac_monthly']]

    energy_output['ac_monthly'] = adjusted_ac_monthly
    return energy_output

@app.route('/calculate_energy', methods=['POST'])
def calculate_energy():
    data = request.get_json()
    lat = data['latitude']
    lon = data['longitude']
    
    logging.debug(f"Received coordinates from frontend: lat={lat}, lon={lon}")
    
    # To be calculated
    roof_area = 100

    solar_data = get_solar_data_from_nrel(lat, lon)
    
    if solar_data:
        adjusted_energy_data = adjust_energy_output(solar_data, roof_area)
        
        logging.debug(f"Sending adjusted energy data to frontend: {adjusted_energy_data}")
        return jsonify({'outputs': adjusted_energy_data})
    else:
        logging.error('Failed to get solar data from NREL API')
        return jsonify({'error': 'Could not retrieve solar data from NREL API.'}), 400
    
@app.route('/test_post', methods=['POST'])
def test_post():
    data = request.get_json()
    return jsonify({"message": "POST request received", "data": data}), 200


if __name__ == '__main__':
    app.run(debug=True)
