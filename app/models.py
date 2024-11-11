from typing_extensions import List
import numpy as np


class WayPoint:
  def __init__(self, lat: int, lng: int, next: 'WayPoint', prev: 'WayPoint'):
    self.lat = lat
    self.lng = lng
    self.next = next
    self.prev = prev
    self.alpha = None
    self.beta = None
    self.m = None

    if next and prev:
      self.calc_alpha_beta()


  def calc_alpha_beta(self):
    if self.next.lng - self.lng != 0:
      m = (self.next.lat - self.lat) / (self.next.lng - self.lng)

      a1 = 0.000179*np.abs(m)*np.sqrt(1/(1 + m**2)) + self.lng
      a2 =  -1/m*(a1 - self.lng) + self.lat if m > 0 else 0.000179 + self.lat

      self.alpha = (a1, a2)

      b1 = -0.000179*np.abs(m)*np.sqrt(1/(1 + m**2)) + self.lng
      b2 =  -1/m*(b1 - self.lng) + self.lat if m > 0 else -0.000179 + self.lat

      self.m = m
      self.beta = (b1, b2)
    else:
      a1 = 0.000179 + self.lng
      a2 =  self.lat

      self.alpha = (a1, a2)

      b1 = -0.000179 + self.lng
      b2 = self.lat

      self.m = 0
      self.beta = (b1, b2)


class BusRoute:
  def __init__(self, id: int, waypoints: List):
    self.id = id
    self.waypoints = waypoints
