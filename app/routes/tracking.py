from flask import Blueprint, request, jsonify, current_app, make_response
from app.services import tracking_services

from app.websockets import sid_rooms
from app.services import buses

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
      bus = buses[data['bus_id']]
      bus_route = bus.route

      active_bus_stops = set(sid_rooms.values())
      for bus_stop in active_bus_stops:
        if bus_stop in bus_route.bus_stops:
          if bus_stop.is_active:
            print(f'[DEBUG]: bus {bus_stop.id} notified')
            tracking_services.notify_bus_stops(bus_stop, bus)

    return 'ok', 200
  except Exception as e:
    print(e)
    return 'bad', 400
