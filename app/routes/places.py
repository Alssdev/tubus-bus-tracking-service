from flask import Blueprint, request, jsonify
import polyline
from shapely import LineString

from app.services import google_maps, stop_services, route_services

bp = Blueprint('places', __name__)

@bp.route('/search', methods=['POST'])
def search_place ():
  data = request.get_json()

  parts = []
  travelTime = 0

  # get lat,lng of the place (Use Google Maps API)
  lng, lat = google_maps.place_get_position(data['placeId'])

  # find the closest bus stop to user
  user_bus_stop, path2 = stop_services.find_nearby_user_to_stop(data['lng'], data['lat'])
  if user_bus_stop:
    print(path2)
    travelTime += LineString(path2).length * 111 / 5
    parts.append({
      'type': 'WALK_STOP',
      'start': { 'lat': data['lat'], 'lng': data['lng'] },
      'path': polyline.encode(path2),
      'stop': {
        'id': user_bus_stop.id,
        'lat': user_bus_stop.position.y,
        'lng': user_bus_stop.position.x
      }
    })
  else:
    return jsonify({
      'error': 'USER_TOO_FAR',
      'data': None
    }), 400

  # find the closest bus stop to place
  place_bus_stop, path1 = stop_services.find_nearby_stop_to_place(lng, lat, data['placeId'])
  if not place_bus_stop:
    return jsonify({
      'error': 'PLACE_TOO_FAR',
      'data': None
    }), 400

  if place_bus_stop.route == user_bus_stop.route:
    # find path between bus stops of the same route
    start = (user_bus_stop.position.x, user_bus_stop.position.y)
    end = (place_bus_stop.position.x, place_bus_stop.position.y)
    path3 = route_services.get_segment_of_route(place_bus_stop.route.route, start, end)

    travelTime += LineString(path3).length * 111 / 45
    parts.append({
      'type': 'BUS',
      'path': polyline.encode(path3),
      'stop1': {
        'id': user_bus_stop.id,
        'lat': user_bus_stop.position.y,
        'lng': user_bus_stop.position.x
      },
      'stop2': {
        'id': place_bus_stop.id,
        'lat': place_bus_stop.position.y,
        'lng': place_bus_stop.position.x
      }
    })

    travelTime += LineString(path1).length * 111 / 5
    parts.append({
      'type': 'WALK_PLACE',
      'path': polyline.encode(path1),
      'start': {
        'lat': place_bus_stop.position.y,
        'lng': place_bus_stop.position.x
      },
      'place': {
        'placeId': data['placeId'],
        'lat': lat,
        'lng': lng
      }
    })
  else:
    return jsonify({
      'error': 'ROUTE_NOT_SUPPORTED',
      'data': None
    }), 400
  
  return jsonify({
    'error': None,
    'data': {
      'parts': parts,
      'travelTime': travelTime * 60
    }
  })