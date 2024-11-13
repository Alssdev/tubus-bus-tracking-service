from flask_socketio import SocketIO, join_room

socketio = None | SocketIO
group_listeners = []

def _handle_connect(data):
  print('New user connected')

def _handle_disconnect(data):
  pass

def _handle_join(data):
  bus_stop_id = data['bus_stop_id']

  if bus_stop_id not in group_listeners:
    join_room(bus_stop_id)
    group_listeners.append(bus_stop_id)

def create_socketio(app):
  global socketio

  socketio = SocketIO(app)
  socketio.on_event('connect', _handle_connect)
  socketio.on_event('disconnect', _handle_disconnect)
  socketio.on_event('join', _handle_join)

  return socketio

def notify_group(data, group):
  socketio.send(data, to=group)
