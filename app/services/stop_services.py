from typing import List
from app.services import bus_stops, BStop
from scipy.spatial import cKDTree
from app.services import google_maps

def find_nearby_stop_to_place(lng, lat, placeId):
  # get all know bus stops
  raw_stop_list: List[BStop] = list(bus_stops.values())

  # filter not active bus stop
  stop_list = [ e for e in raw_stop_list if e.is_active ]

  # generate current bus stop KDTree
  coords = [e.position.coords[0] for e in stop_list]
  stop_tree = cKDTree(coords)

  # find closest bus stop
  stop_indexs = stop_tree.query_ball_point((lng, lat), r= 0.5 / 111) # 500 m

  # use google maps to identiy the closest bust stop by walking
  if len(stop_indexs) > 0:
    bus_stop, path = google_maps.path_stop_place(placeId, [stop_list[i] for i in stop_indexs])
    return bus_stop, path
  else:
    return None, None

def find_nearby_user_to_stop(lng, lat):
  # get all know bus stops
  raw_stop_list: List[BStop] = list(bus_stops.values())

  # filter not active bus stop
  stop_list = [ e for e in raw_stop_list if e.is_active ]

  # generate current bus stop KDTree
  coords = [e.position.coords[0] for e in stop_list]
  stop_tree = cKDTree(coords)

  # find closest bus stops
  stop_indexs = stop_tree.query_ball_point((lng, lat), r= 0.5 / 111) # 500m

  # use google maps to identiy the closest bust stop by walking
  if len(stop_indexs) > 0:
    bus_stop, path = google_maps.path_user_stop(lat, lng, [stop_list[i] for i in stop_indexs])
    return bus_stop, path
  else:
    return None, None
