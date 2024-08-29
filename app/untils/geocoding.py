import requests

def get_lat_long_osm(address):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'addressdetails': 1
    }
    headers = {
        'User-Agent': 'zonaBro/1.0 (argenbroinfo@gmail.com)' 
    }
    try:
        response = requests.get(base_url, params=params, headers=headers)

        response.raise_for_status()

        results = response.json()
        
        if results:
            location = results[0]
            return location['lat'], location['lon']
        else:
            return None, None
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')
    except Exception as ex:
        print(f'An error occurred: {ex}')
    return None, None

