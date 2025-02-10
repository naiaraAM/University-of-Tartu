# pages/views.py
import requests
from django.shortcuts import render
from django.conf import settings
import json
import math
import extract_info_csv


def haversine_distance(lat1, lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points on the earth (specified in decimal degrees)
    """
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers

def mapbox_map(request):
    # Read the data from CSV
    info_stops = extract_info_csv.obtain_tartu_stops()

    stops = [
        {
            'lat': float(info[0]),
            'lng': float(info[1]),
            'id': info[2]
        }
        for info in info_stops
    ]


    # Calculate min and max latitude and longitude values
    latitudes = [stp['lat'] for stp in stops]
    longitudes = [stp['lng'] for stp in stops]
    min_lat, max_lat = min(latitudes), max(latitudes)
    min_lng, max_lng = min(longitudes), max(longitudes)

    stops_id = [stp['id'] for stp in stops]


    # Initialize variables
    input_point = None
    error_message = None

    # Get user input from GET parameters
    input_lat = request.GET.get('latitude')
    input_lng = request.GET.get('longitude')

    if input_lat and input_lng:
        try:
            input_lat = float(input_lat)
            input_lng = float(input_lng)

            # Validate input latitude and longitude
            if not (min_lat <= input_lat <= max_lat) or not (min_lng <= input_lng <= max_lng):
                error_message = (
                    f"Input coordinates are out of bounds. "
                    f"Latitude must be between {min_lat} and {max_lat}, "
                    f"longitude must be between {min_lng} and {max_lng}."
                )
            else:
                input_point = {'lat': input_lat, 'lng': input_lng}

        except ValueError:
            error_message = "Invalid input. Please enter valid numerical values for latitude and longitude."

    response = None
    if input_point:
        response = do_post_point(input_point['lat'], input_point['lng'])

    nearest_stops = []
    if response != None:
        returned_stops = response["results"]
        # print(returned_stops)
        for i in returned_stops:
            coords = i["coords"]
            id = i["id"]
            nearest_stops.append({'lat': coords["lat"], 'lon': coords["lon"], 'id': id})
    # print(nearest_stops)

    #
    # # Recalculate bounds with input point (if valid)
    # bounds = [[min(longitudes), min(latitudes)], [max(longitudes), max(latitudes)]]  # SW and NE corners
    #
    # # Find nearest stops if input point exists and is valid
    # if input_point:
    #     # Calculate distances to all stops
    #     for loc in stops:
    #         loc['distance'] = haversine_distance(
    #             input_point['lat'], input_point['lng'],
    #             loc['lat'], loc['lng']
    #         )
    #     # Sort locations by distance
    #     locations_sorted = sorted(stops, key=lambda x: x['distance'])
    #     N = 5  # Number of nearest stops to find
    #     nearest_stops = locations_sorted[:N]
    #     # Prepare nearest stops data without 'distance' key
    #     nearest_stops = [{'lat': loc['lat'], 'lng': loc['lng']} for loc in nearest_stops]
    # else:
    #     # Remove 'distance' key if present to avoid serialization issues
    #     for loc in stops:
    #         loc.pop('distance', None)

    # Serialize data to JSON strings
    locations_json = json.dumps(stops)
    input_point_json = json.dumps(input_point) if input_point else 'null'
    nearest_stops_json = json.dumps(nearest_stops) if nearest_stops else '[]'
    # print(nearest_stops_json)

    context = {
        'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN,
        'locations': locations_json,
        'input_point': input_point_json,
        'nearest_stops': nearest_stops_json,
        'error_message': error_message,
        'min_lat': min_lat,
        'max_lat': max_lat,
        'min_lng': min_lng,
        'max_lng': max_lng,
    }
    return render(request, 'pages/mapbox_map.html', context)

def do_post_point(latitude, longitude):
    IP_ADDRESS = 'back'
    PORT = '8001'
    URL = f'http://{IP_ADDRESS}:{PORT}/'
    json_data = {'lat': latitude, 'lng': longitude}
    response = None
    print(f"Sending POST request to {URL} with data {json_data}")
    try:
        response = requests.get(f'{URL}?lat={latitude}&lng={longitude}')
        response = response.json()
        # print(f"POST request successful: {response}")
    except requests.RequestException as e:
        print(f"POST request failed: {e}")
    return response