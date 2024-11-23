from flask import Blueprint, request, jsonify, current_app, make_response
from shapely import LineString
from app.dao import tracking_dao
from app.models import BRoute
from app.services import buses

from app.services import bus_routes

bp = Blueprint('rutas', __name__)

@bp.route('/<route_id>/id', methods=['POST'])
def update_bus_state():
    route_id = int(route_id)

    if route_id in bus_routes:
      # get bus route
      bus_route = bus_routes[route_id]

      raw_bus_routes = tracking_dao.read_bus_routes()

      for route_id2 in raw_bus_routes:
        if route_id2 == route_id:
          bus_routes[route_id2] = BRoute(
            id = route_id2,
            buses=bus_route.buses,
            bus_stops=bus_route.bus_stops,
            route=LineString(raw_bus_routes[route_id2])
          )

    return 'ok', 200

@bp.route('/', methods=['POST'])
def update_bus_route_list():
    return 'ok', 200
