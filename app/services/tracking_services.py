from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point

from app.models import Bus, BRoute, BStop

from app.dao import bus_dao, tracking_dao
from app.dao import bus_stop_dao

from app.services import buses, bus_routes, bus_stops

import numpy as np

from app.websockets import notify_room

def init():
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
    bus_stops[bus_stop[0]] = BStop(bus_stop[0], bus_stop[1], bus_stop[2], bus_routes[bus_stop[3]], bus_stop[4])
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
    bus_routes[bus[2]].buses.append(buses[bus[0]])

def receive_bus_position (bus_id, lat, lng):
  # find bus
  bus = buses[bus_id]

  if bus:
    # map (lat, lng) to a valid point of the bus route
    mapped_point = _map_point_to_route(lat, lng, bus)

    if mapped_point:
      if bus.set_position(mapped_point):
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

def notify_bus_stops (bus_stop, bus):
  # Determine if the new bus's position affects my ETA.
  # This is determined by finding the bus closest to me.
  # TODO: maybe each bus stop should save who is the closest bus to it
  closest_bus, closest_distance = _closest_bus(bus_stop)

  if bus == closest_bus:
    print(f'🤖 {bus_stop.id} was notified')
    notify_listeners(bus_stop, bus, closest_distance)
  else:
    print('🤖 closest_bus is NONE')


# TODO: very inefficient... estoy cansado gfe
def _closest_bus (bus_stop: BStop) -> tuple[Bus, float]:
  buses = bus_stop.route.buses
  route = bus_stop.route.route

  closest_bus = None
  closest_distance = 1000000 # this will NEVER be a valid distance
  for bus in buses:
    if bus.is_active and bus.distance:

      # bus is behind me
      if bus_stop.distance >= bus.distance:
        if closest_distance > bus_stop.distance - bus.distance:
          closest_bus = bus
          closest_distance = bus_stop.distance - bus.distance

      # bus is not  behind me
      else:
        real_bus_distance = (route.length - bus.distance) + (bus_stop.distance)
        if closest_distance > real_bus_distance:
          closest_bus = bus
          closest_distance = real_bus_distance

  return closest_bus, closest_distance


def notify_listeners(bus_stop: BStop, bus: Bus, distance):
  # at this point bus.distance ALWAYS EXISTS
  assert(type(bus.position) == Point)
  assert(type(bus.distance) == np.float64)

  route = bus_stop.route.route

  # find the segment by accumulating points between start and end points
  route_coords = list(route.coords)
  segment_coords = []  # Begin with the interpolated start point
  segment_aux = [(bus.position.x, bus.position.y)]

  # Add points in between start and end points based on their projected distances
  for coord in route_coords:
      point = Point(coord)
      dist = route.project(point)

      if bus.distance < bus_stop.distance:
        if bus.distance < dist < bus_stop.distance:
            segment_coords.append(coord)
      elif bus.distance < dist < route.length:
          segment_aux.append(coord)
      elif dist < bus_stop.distance:
        segment_coords.append(coord)

  segment_aux.extend(segment_coords)
  segment_coords = segment_aux

  # end with the interpolated end point
  segment_coords.append((bus_stop.position.x, bus_stop.position.y))

  message = {
    'bus': {
      'id': bus.id,
      'lat': bus.position.y,
      'lng': bus.position.x
    },
    'bus_stop_position': {
      'lat': bus_stop.position.y,
      'lng': bus_stop.position.x
    },
    'distance_km': distance * 111, # convert to km
    'eta_min': distance * 222, # simulation of ETA
    'route_points': segment_coords
  }

  notify_room(message, bus_stop.room_name)
