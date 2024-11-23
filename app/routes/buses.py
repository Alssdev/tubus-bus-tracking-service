from flask import Blueprint, request, jsonify
from app.dao import bus_dao
from app.models import Bus
from app.services import buses

from app.services import buses, bus_routes

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
def update_bus_list(body):
  # read updated bus list from db
  raw_buses = bus_dao.read_buses()
  for bus in raw_buses:
    if id not in buses:
      buses[bus[0]] = Bus(
        id=bus[0],
        lat=None,
        lng=None,
        is_active=bus[1],
        route=bus_routes[bus[2]]
      )
  
  return 'ok', 200
