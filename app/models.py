from shapely.geometry import LineString
from typing_extensions import List
from shapely import Point

import uuid

class Bus:
  def __init__(self, id, lat, lng, is_active, route):
    self.id = id
    self.position: Point | None =  Point(lng, lat) if lat and lng else None
    self.is_active: bool = is_active
    self.route: BRoute = route
    self.distance: float | None = None

  def set_position (self, position: Point):
    new_distance = self.route.route.project(position)

    # if new_distance is behind current_distance, discard it
    if self.distance:
      if new_distance < self.distance:
        if self.route.route.length - self.distance > 0.00022:
          return False

    self.position = position
    self.distance = new_distance
    return True


class BStop:
  def __init__(self, id, lat, lng, route, state):
    self.id = id
    self.position = Point(lng, lat)
    self.route: BRoute = route
    self.room_name: str = str(uuid.uuid4())
    self.distance = route.route.project(self.position)
    self.is_active = state == 1


class BRoute:
  def __init__(self, id, buses: List[Bus], bus_stops: List[BStop], route: LineString):
    self.id: int = id
    self.buses: List[Bus] = buses
    self.bus_stops: List[BStop] = bus_stops
    self.route: LineString = route
