from flask import Blueprint, request, jsonify, current_app, make_response
from app.services import tracking_services
from app.services import bus_services

bp = Blueprint('tracking', __name__)

@bp.route('/', methods=['POST'])
def receive_bus_location():
  # { lat, lng, bus_id }
  data = request.get_json()

  try:
    # valid data
    assert(type(data['bus_id']) == int)
    assert(type(data['lat']) == float)
    assert(type(data['lng']) == float)

    # process new bus position
    valid = tracking_services.receive_bus_position(data['bus_id'], data['lat'], data['lng'])

    if valid:
      # notify listeners
      # TODO: ...
      pass

    return 'ok', 200
  except:
    return 'bad', 400
