from flask import Blueprint, request, jsonify, current_app, make_response
from app.services import buses

from app.services import bus_routes

bp = Blueprint('rutas', __name__)

@bp.route('/<route_id>/id', methods=['POST'])
def update_bus_state(route_id):
    route_id = int(route_id)
    if route_id in bus_routes:
        print('updated')
        # TODO

    return 'ok', 200
