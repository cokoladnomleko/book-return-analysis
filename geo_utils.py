import requests
from geopy.distance import geodesic

# Overpass API URL
OVERPASS_URL = "http://overpass-api.de/api/interpreter"


def get_public_transport(coords: tuple=(45.4,-123.1,45.7,-122.4)):
    """Returns a list of all public transport in the bounding box provided by coordinates
    :param coords: coordinates of the bbox
    :type coords: tuple
    :rtype: list of dicts
    """

    # Define the Overpass query for public transport (bus stops, train stations, bus stations)
    query = f"""
    [out:json];
    (
    node["highway"="bus_stop"]{coords};  // bus stops
    node["railway"="station"]{coords};  // train stations
    node["amenity"="bus_station"]{coords};  // bus stations
    node["public_transport"="platform"]{coords};  // metro/train platforms
    );
    out body;
    """

    # Send the request
    response = requests.get(OVERPASS_URL, params={'data': query})

    # Check for successful request
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        data = None

    # Example: Parse the response to get the coordinates of each transport station
    if data:
        stations = []
        for element in data['elements']:
            if 'lat' in element and 'lon' in element:
                stations.append({
                    "type": element.get('tags', {}).get('highway', element.get('tags', {}).get('railway', 'Unknown')),
                    "lat": element['lat'],
                    "lon": element['lon'],
                    "name": element.get('tags', {}).get('name', 'Unknown')
                })

    return stations


def get_coords_from_address(address: str):
    """Finds latitude and longitude from an address
    :param address: address
    :type address: str
    :returns: latitude and longitude
    :rtype: tuple
    """
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"

    response = requests.get(url, headers = {'User-Agent': 'Chrome/102.0.0.0'})
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        data = None

    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return (lat, lon)
    else:
        return None
    
    
def find_nearest_stations(address, stations):
    """Finds distance to the nearest station & number of stations closer than 0.5 km
    :param address: street address
    :type address: str
    :param station: list of stations in the city
    :type station: list[dict]
    :rtype: dict
    """
    address_coords = get_coords_from_address(address)
    if not address_coords:
        return None

    min_distance = float('inf')
    num_near = 0

    for station in stations:
        station_coords = (station['lat'], station['lon'])
        distance = geodesic(address_coords, station_coords).km
        if distance < min_distance:
            min_distance = distance
        if distance < 0.5:
            num_near += 1

    return {'min_distance': round(min_distance, 3), 'num_near': num_near}
