from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point

from ..dao import tracking_dao
import time

# struct for store all bus routes and its waypoints
_bus_routes: dict[int, LineString] = {}

def init():
  global _bus_routes

  # read route paths from db
  raw_bus_routes = tracking_dao.read_bus_routes()

  start = time.time()

  # create a LineString. This represent a bus route and is easly to use.
  for route_id in raw_bus_routes:
    _bus_routes[route_id] = LineString(raw_bus_routes[route_id])

  end = time.time()

  print('⚡ bus routes processed in {:.6f}s'.format(end - start))

def map_point_to_route (lat: float, lng: float, route_id: int):
  assert(route_id in _bus_routes)

  point = Point(lng, lat) # x->lng, lat->lat

  if point.distance(_bus_routes[route_id]) <= 0.00045:
    distance = _bus_routes[route_id].project(point)
    return _bus_routes[route_id].interpolate(distance)
  else:
    return None
