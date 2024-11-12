from shapely.geometry import Polygon, Point
from shapely.affinity import rotate, translate
from math import atan2, degrees

from typing_extensions import List
from shapely.geometry import Point

class WayPoint:
  def __init__(self, lat: int, lng: int, next: 'WayPoint', prev: 'WayPoint'):
    self.lat = lat
    self.lng = lng
    self.next = next
    self.prev = prev
    self.polygon = None

  def calc_polygon(self):
    # calculates polygon to determine if a given point P should be proyected in the
    # segment formed by this and self.next waypoint.

    assert(self.next != None)

    p1 = Point(self.lng, self.lat)            # this waypoint
    p2 = Point(self.next.lng, self.next.lat)  # next waypoint

    # height and angle of the resultant polygon
    distance = p1.distance(p2)
    angle = degrees(atan2(p2.y - p1.y, p2.x - p1.x))

    polygon = Polygon([(0, -0.000179), (distance, -0.000179), (distance, 0.000179), (0, 0.000179)])
    polygon = rotate(polygon, angle, origin=(0,0), use_radians=False)
    polygon = translate(polygon, xoff=p1.x, yoff=p2.y)

    self.polygon = polygon

class BusRoute:
  def __init__(self, id: int, waypoints: List):
    self.id = id
    self.waypoints = waypoints
