from flask import Blueprint, request, jsonify, current_app, make_response
from app.services import buses

from app.services import bus_stops

bp = Blueprint('paradas', __name__)

@bp.route('/state/<stop_id>/id', methods=['POST'])
def update_bus_state(stop_id):
    data = request.get_json()

    stop_id = int(stop_id)
    if stop_id in bus_stops:
        bus_stops[stop_id].is_active = data['status'] == 1

    return 'ok', 200
