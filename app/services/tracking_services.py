from typing_extensions import List
from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point

from app.models import BusStop
from app.websockets import group_listeners, notify_group

from app.dao import tracking_dao
from app.dao import bus_stop_dao

import json
import numpy as np

# struct for store all bus routes and its waypoints
_bus_routes: dict[int, LineString] = {}
_bus_stops: dict = {}

# store distance in the route for each bus.
# bus_id -> distance
_last_know_distance: dict[int, float] = {}

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


def map_point_to_route (lat: float, lng: float, route_id: int, bus_id: int):
  assert(route_id in _bus_routes)

  point = Point(lng, lat) # x->lng, lat->lat
  bus_route = _bus_routes[route_id]

  if point.distance(bus_route) <= 0.00045:
    bus_distance = bus_route.project(point)
    bus_point = bus_route.interpolate(bus_distance)

    # save point
    if bus_id in _last_know_distance:
      if bus_distance <= _last_know_distance[bus_id]:
        if bus_route.length - _last_know_distance[bus_id] > 0.00022:
          return None

    _last_know_distance[bus_id] = bus_distance

    return bus_point
  else:
    return None

def notify_listeners(bus_point, bus_id):
  # bsi ~ bus stop id
  for bsi in group_listeners:
    assert(bsi in _bus_stops)

    # bus stop and route data
    stop = _bus_stops[bsi]
    route = _bus_routes[stop.route_id]

    # bus and bus stop distances (from start point of route)
    bus_distance = route.project(bus_point)
    stop_point = Point(stop.lng, stop.lat)
    stop_distance = route.project(stop_point)

    # clculate the distance from the bus to the bus stop
    distance_between = 0
    if bus_distance <= stop_distance:
      distance_between = (stop_distance - bus_distance)
    else:
     distance_between = ((route.length - bus_distance) + stop_distance)

    route_coords = list(route.coords)

    # find the segment by accumulating points between start and end points
    segment_coords = []  # Begin with the interpolated start point
    segment_aux = [bus_point.coords[0]]

    # Add points in between start and end points based on their projected distances
    for coord in route_coords:
        point = Point(coord)
        dist = route.project(point)

        if bus_distance < stop_distance:
          if bus_distance < dist < stop_distance:
              segment_coords.append(coord)
        elif bus_distance < dist < route.length:
            segment_aux.append(coord)
        elif dist < stop_distance:
          segment_coords.append(coord)

    segment_aux.extend(segment_coords)
    segment_coords = segment_aux

    # end with the interpolated end point
    segment_coords.append(stop_point.coords[0])

    message = {
      'bus': {
        'id': bus_id,
        'lat': bus_point.y,
        'lng': bus_point.x
      },
      'bus_stop_position': {
        'lat': stop.lat,
        'lng': stop.lng
      },
      'distance_km': distance_between * 111, # convert to km
      'eta_min': distance_between * 222, # simulation of ETA
      'route_points': segment_coords
    }
    notify_group(message, bsi)
