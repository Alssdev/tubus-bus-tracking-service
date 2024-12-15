from flask import request
from flask_socketio import SocketIO, disconnect, join_room

from app.models import BStop
from app.services import bus_stops

# handly references
socketio: SocketIO = None
sid_rooms: dict[int, BStop] = {}

def create_socketio(app):
  global socketio

  socketio = SocketIO(app, cors_allowed_origins="*")

  @socketio.on('connect')
  def connect_handler(data):
    print(f'🤖 user with sid={request.sid}')

  @socketio.on('disconnect')
  def disconnect_handler():
    print(f'🤖 bye user with sid={request.sid}')

    # maybe the user never suscribes to a room
    if request.sid in sid_rooms:
      sid_rooms.pop(request.sid)

  @socketio.on('join')
  def join_handler(data):
    if data['bus_stop_id'] in bus_stops:
      bus_stop = bus_stops[data['bus_stop_id']]
      print(f'🤖 user with sid={request.sid}, joined to {bus_stop.id} in route {bus_stop.route.id}')

      # join to room
      join_room(bus_stop.room_name)
      sid_rooms[request.sid] = bus_stop

    else:
      # user is doing wierd stuffs
      disconnect()

  @socketio.on('buses_join')
  def buses_join_handler ():
    print(f'🤖 dashboard connected with sid={request.sid}')
    join_room('dashboard')

  return socketio

def notify_room (data, room):
  print(f'> {data}')
  socketio.send(data, to=room)
