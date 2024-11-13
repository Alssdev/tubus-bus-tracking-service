from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point

from app.models import BusStop
from app.websockets import group_listeners, notify_group

from app.dao import tracking_dao
from app.dao import bus_stop_dao

import json

# struct for store all bus routes and its waypoints
_bus_routes: dict[int, LineString] = {}
_bus_stops: dict = {}

def init():
  global _bus_routes
  global _bus_stops

  # read route paths from db
  raw_bus_routes = tracking_dao.read_bus_routes()
  raw_bus_stops = bus_stop_dao.read_bus_stops()

  # create a LineString. This represent a bus route and is easly to use.
  for route_id in raw_bus_routes:
    _bus_routes[route_id] = LineString(raw_bus_routes[route_id])

  for bus_stop in raw_bus_stops:
    _bus_stops[bus_stop[0]] = BusStop(bus_stop[0], bus_stop[1], bus_stop[2],  bus_stop[3])


def map_point_to_route (lat: float, lng: float, route_id: int):
  assert(route_id in _bus_routes)

  point = Point(lng, lat) # x->lng, lat->lat

  if point.distance(_bus_routes[route_id]) <= 0.00045:
    bus_distance = _bus_routes[route_id].project(point)
    bus_point = _bus_routes[route_id].interpolate(bus_distance)

    return bus_point
  else:
    return None

def notify_listeners(bus_point):
  # bsi ~ bus stop id
  for bsi in group_listeners:
    assert(bsi in _bus_stops)

    # bus stop and route data
    stop = _bus_stops[bsi]
    route = _bus_routes[stop.route_id]

    # bus distance
    bus_distance = route.project(bus_point)

    # bus stop position and distance
    point = Point(stop.lng, stop.lat)
    distance = route.project(point)

    forward_distance = 0
    if bus_distance <= distance:
      forward_distance = (distance - bus_distance) * 111
    else:
     forward_distance = ((route.length - bus_distance) + distance) * 111

    message = {
      'bus_position': {
        'lat': bus_point.y,
        'lng': bus_point.x
      },
      'bus_stop_position': {
        'lat': stop.lat,
        'lng': stop.lng
      },
      'distance_km': forward_distance,
      'eta': 0
    }
    notify_group(json.dumps(message), bsi)
