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

  return jsonify({
    'error': 'bus not found',
    'lat': None,
    'lng': None
  })
