from ..dao import tracking_dao
from app.models import BusRoute, WayPoint
import time
import numpy as np

_bus_routes = {}

def init():
  global _bus_routes

  # read route paths from db
  raw_bus_routes = tracking_dao.read_bus_routes()

  start = time.time()

  # create handly objects
  for route_id in raw_bus_routes:
    raw_waypoints = raw_bus_routes[route_id]
    waypoints = []

    # first waypoint of the route
    first = raw_waypoints.pop(0)
    first = WayPoint(first[0], first[1], None, None) # for now
    waypoints.append(first)

    # create a chain of waypoints
    current = first
    while len(raw_waypoints) != 0:
      next = raw_waypoints.pop(0)

      if next[0] != current.lat and next[1] != current.lng:
        next = WayPoint(next[0], next[1], current, None)

        current.next = next
        current = next
        waypoints.append(next)

    first.prev = current
    current.next = first

    _bus_routes[route_id] = BusRoute(route_id, waypoints)

  # calc alpha and beta
  for route_id in _bus_routes:
    for waypoint in _bus_routes[route_id].waypoints:
      waypoint.calc_alpha_beta()

  end = time.time()

  # for test only
  # for waypoint in _bus_routes[1].waypoints:
  #   print(f' ({waypoint.lng:.5f},{waypoint.lat:.5f})')
  #   print(f'({waypoint.alpha[0]:.5f},{waypoint.alpha[1]:.5f})')
  #   print(f'({waypoint.beta[0]:.5f},{waypoint.beta[1]:.5f})')

  print('⚡ bus routes retrived in {:4f}s'.format(end - start))
