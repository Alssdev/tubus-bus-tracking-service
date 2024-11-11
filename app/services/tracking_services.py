from ..dao.tracking_dao import TrackingDAO

class TrackingService:
  _route_paths = {}

  def __init__(self):
    route_paths = TrackingDAO.read_route_paths()
