import requests
import json
import polyline

def place_get_position (placeId):
  api = f'https://places.googleapis.com/v1/places/{placeId}'
  response = requests.get(api, headers={
    'X-Goog-FieldMask': 'location',
    'X-Goog-Api-Key': 'AIzaSyDu4JTEY8e68B1dBOtSDgKJ6gpec_jiKpE'
  })

  location = json.loads(response.text)['location']

  return location['longitude'], location['latitude']

def path_stop_place (placeId, stop_list):
  api = 'https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix'
  headers = {
    'X-Goog-FieldMask': 'originIndex,distanceMeters,status.code,condition',
    'X-Goog-Api-Key': 'AIzaSyDu4JTEY8e68B1dBOtSDgKJ6gpec_jiKpE'
  }
  data = {
    'travelMode': 'WALK',
    'units': 'METRIC',
    'origins': [
      {
        'waypoint': {
          'location': {
            'latLng': {
              'latitude': stop.position.y,
              'longitude': stop.position.x
            }
          }
        }
      }
      for stop in stop_list
    ],
    'destinations': [
      {
        'waypoint': {
          'placeId': placeId
        }
      }
    ]
  }

  response = requests.post(api, headers=headers, json=data)
  data = json.loads(response.text)

  best_index = -1
  best_distance = -1
  for elem in data:
    if elem['condition'] == 'ROUTE_EXISTS':
      if best_distance > elem['distanceMeters'] or best_index == -1:
        best_index = elem['originIndex']
        best_distance = elem['distanceMeters']
  if best_index != -1:
    best_bus_stop = stop_list[best_index]
    path = find_path({
      'location': {
        'latLng': {
          'latitude': best_bus_stop.position.y,
          'longitude': best_bus_stop.position.x
        }
      }
    }, {
      'placeId': placeId
    })

  return best_bus_stop, path

def path_user_stop (lat, lng, stop_list):
  api = 'https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix'
  headers = {
    'X-Goog-FieldMask': 'destinationIndex,distanceMeters,status.code,condition',
    'X-Goog-Api-Key': 'AIzaSyDu4JTEY8e68B1dBOtSDgKJ6gpec_jiKpE'
  }
  data = {
    'travelMode': 'WALK',
    'units': 'METRIC',
    'destinations': [
      {
        'waypoint': {
          'location': {
            'latLng': {
              'latitude': stop.position.y,
              'longitude': stop.position.x
            }
          }
        }
      }
      for stop in stop_list
    ],
    'origins': [
      {
        'waypoint': {
          'location': {
            'latLng': {
              'latitude': lat,
              'longitude': lng
            }
          }
        }
      }
    ]
  }

  response = requests.post(api, headers=headers, json=data)
  data = json.loads(response.text)

  best_index = -1
  best_distance = -1

  for elem in data:
    if elem['condition'] == 'ROUTE_EXISTS':
      if best_distance > elem['distanceMeters'] or best_index == -1:
        best_index = elem['destinationIndex']
        best_distance = elem['distanceMeters']

  if best_index != -1:
    best_bus_stop = stop_list[best_index]
    path = find_path(
      {
        'location': {
          'latLng': {
            'latitude': lat,
            'longitude': lng
          }
        }
      },
      {
        'location': {
          'latLng': {
            'latitude': best_bus_stop.position.y,
            'longitude': best_bus_stop.position.x
          }
        }
      }
    )

  return best_bus_stop, path


def find_path (origin, destination):
  api = 'https://routes.googleapis.com/directions/v2:computeRoutes'
  headers = {
    'X-Goog-FieldMask': 'routes.polyline.encodedPolyline',
    'X-Goog-Api-Key': 'AIzaSyDu4JTEY8e68B1dBOtSDgKJ6gpec_jiKpE'
  }
  data = {
    'travelMode': 'WALK',
    'units': 'METRIC',
    'origin': origin,
    'destination': destination
  }

  return polyline.decode(
    json.loads(
      requests.post(api, headers=headers, json=data).text
    )['routes'][0]['polyline']['encodedPolyline']
  )