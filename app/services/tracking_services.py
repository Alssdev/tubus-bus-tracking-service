from typing_extensions import List
from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point

from app.models import Bus, BRoute, BStop

from app.dao import bus_dao, tracking_dao
from app.dao import bus_stop_dao

from app.services import buses, bus_routes, bus_stops

import json
import numpy as np

def init():
  global _bus_routes
  global _bus_stops

  # read and process bus routes from db
  raw_bus_routes = tracking_dao.read_bus_routes()
  for route_id in raw_bus_routes:
    bus_routes[route_id] = BRoute(
      id = route_id,
      buses=[],
      bus_stops=[],
      route=LineString(raw_bus_routes[route_id])
  )

  # read and process bus_stops from db
  raw_bus_stops = bus_stop_dao.read_bus_stops()
  for bus_stop in raw_bus_stops:
    bus_stops[bus_stop[0]] = BStop(bus_stop[0], bus_stop[1], bus_stop[2], bus_routes[bus_stop[3]])
    bus_routes[bus_stop[3]].bus_stops.append(bus_stops[bus_stop[0]])

  # read an process buses from db
  raw_buses = bus_dao.read_buses()
  for bus in raw_buses:
    buses[bus[0]] = Bus(
      id=bus[0],
      lat=None,
      lng=None,
      is_active=bus[1],
      route=bus_routes[bus[2]]
    )
    route=bus_routes[bus[2]].buses.append(buses[bus[0]])

def receive_bus_position (bus_id, lat, lng):
  # find bus
  bus = buses[bus_id]

  if bus:
    # map (lat, lng) to a valid point of the bus route
    mapped_point = _map_point_to_route(lat, lng, bus)

    if mapped_point:
      bus.position = mapped_point
      return True

  return False

def _map_point_to_route (lat: float, lng: float, bus: Bus):
  point = Point(lng, lat) # x->lng, lat->lat
  bus_route = bus.route.route

  if point.distance(bus_route) <= 0.00045:
    bus_distance = bus_route.project(point)
    return bus_route.interpolate(bus_distance)
  else:
    return None

# def notify_listeners(bus_point, bus_id):
#   # bsi ~ bus stop id
#   for bsi in group_listeners:
#     assert(bsi in _bus_stops)

#     # bus stop and route data
#     stop = _bus_stops[bsi]
#     route = _bus_routes[stop.route_id]

#     # bus and bus stop distances (from start point of route)
#     bus_distance = route.project(bus_point)
#     stop_point = Point(stop.lng, stop.lat)
#     stop_distance = route.project(stop_point)

#     # clculate the distance from the bus to the bus stop
#     distance_between = 0
#     if bus_distance <= stop_distance:
#       distance_between = (stop_distance - bus_distance)
#     else:
#      distance_between = ((route.length - bus_distance) + stop_distance)

#     route_coords = list(route.coords)

#     # find the segment by accumulating points between start and end points
#     segment_coords = []  # Begin with the interpolated start point
#     segment_aux = [bus_point.coords[0]]

#     # Add points in between start and end points based on their projected distances
#     for coord in route_coords:
#         point = Point(coord)
#         dist = route.project(point)

#         if bus_distance < stop_distance:
#           if bus_distance < dist < stop_distance:
#               segment_coords.append(coord)
#         elif bus_distance < dist < route.length:
#             segment_aux.append(coord)
#         elif dist < stop_distance:
#           segment_coords.append(coord)

#     segment_aux.extend(segment_coords)
#     segment_coords = segment_aux

#     # end with the interpolated end point
#     segment_coords.append(stop_point.coords[0])

#     message = {
#       'bus': {
#         'id': bus_id,
#         'lat': bus_point.y,
#         'lng': bus_point.x
#       },
#       'bus_stop_position': {
#         'lat': stop.lat,
#         'lng': stop.lng
#       },
#       'distance_km': distance_between * 111, # convert to km
#       'eta_min': distance_between * 222, # simulation of ETA
#       'route_points': segment_coords
#     }
#     notify_group(message, bsi)
