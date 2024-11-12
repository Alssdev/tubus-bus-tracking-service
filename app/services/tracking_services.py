from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point
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

  # create a LineString. This represent a bus route and is easly to use.
  for route_id in raw_bus_routes:
    _bus_routes[route_id] = LineString(raw_bus_routes[route_id])

  end = time.time()

  print('⚡ bus routes retrived in {:4f}s'.format(end - start))
