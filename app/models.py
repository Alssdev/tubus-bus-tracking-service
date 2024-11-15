from shapely.geometry import LineString
from typing_extensions import List
from shapely import Point

import uuid

class Bus:
  def __init__(self, id, lat, lng, is_active, route):
    self.id = id
    self.position: Point | None =  Point(lat, lng) if lat and lng else None
    self.is_active: bool = is_active
    self.route: BRoute = route


class BStop:
  def __init__(self, id, lat, lng, route):
    self.id = id
    self.position = Point(lng, lat)
    self.route: BRoute = route
    self.room_name: str = str(uuid.uuid4())


class BRoute:
  def __init__(self, id, buses: List[Bus], bus_stops: List[BStop], route: LineString):
    self.id: int = id
    self.buses: List[Bus] = buses
    self.bus_stops: List[BStop] = bus_stops
    self.route: LineString = route
