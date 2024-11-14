from flask_socketio import SocketIO, join_room

socketio = None | SocketIO
group_listeners = []

def _handle_connect(data):
  print('New user connected')

def _handle_join(data):
  bus_stop_id = data['bus_stop_id']

  if bus_stop_id not in group_listeners:
    group_listeners.append(bus_stop_id)

  join_room(bus_stop_id)

def _handle_error(error):
  print(error)

def create_socketio(app):
  global socketio

  socketio = SocketIO(app)
  socketio.on_event('connect', _handle_connect)
  socketio.on_event('join', _handle_join)

  return socketio

def notify_group(data, group):
  print(f'> listeners notified')
  socketio.send(data, to=group)
