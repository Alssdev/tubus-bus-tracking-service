from flask import Blueprint, request, jsonify, current_app, make_response
from app.services import tracking_services
from app.services import bus_services

bp = Blueprint('tracking', __name__)

@bp.route('/', methods=['POST'])
def receive_bus_location():
  # body is received as a json
  data = request.get_json()

  # retrive bus' data
  bus = bus_services.fetch_bus_info(data['bus_id'])
  if bus:
    # bus must be active to accept tracking info
    if bus['is_active']:
      # then save new position
      newPoint = tracking_services.map_point_to_route(data['lat'], data['lng'], bus['route_id'])

      # if error
      if not newPoint:
        return jsonify({ 'new_location': None })

      return jsonify({
        'new_location': {
          'lat': newPoint.y,
          'lng': newPoint.x,
        }
      })

    else:
      return jsonify({ 'error': 'BUS_NOT_ACTIVE' }), 400

  else:
    return jsonify({ 'error': 'BUS_NOT_FOUND' }), 400
