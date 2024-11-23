from flask import Blueprint, request, jsonify, current_app, make_response
from app.services import buses

from app.services import buses

bp = Blueprint('buses', __name__)

@bp.route('/<bus_id>/id', methods=['GET'])
def bus_location(bus_id):
  bus_id = int(bus_id)

  # buscar bus
  if bus_id in buses:
    bus = buses[bus_id]
    if bus.is_active and bus.position:
      return jsonify({
        'error': None,
        'lat': bus.position.y,
        'lng': bus.position.x
      })

  print('bus not found');
  return jsonify({
    'error': 'bus not found',
    'lat': None,
    'lng': None
  })


@bp.route('/state/<bus_id>/id', methods=['POST'])
def update_bus_state(bus_id):
    data = request.get_json()

    bus_id = int(bus_id)
    if bus_id in buses:
        buses[bus_id].is_active = data['status'] == 1

    return 'ok', 200

@bp.route('/', methods=['POST'])
def update_bus_list(bus_id):
    return 'ok', 200
