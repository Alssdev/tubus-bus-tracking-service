import app.dao.dao as dao

def read_bus_routes ():
  # retrive bus routes
  cur = dao.get_cursor()
  cur.execute('SELECT id,numero FROM rutas')
  routes = cur.fetchall()
  cur.close()

  # store routes and waypoints in a dict.
  # [route_id] -> [w0, w1, w2, w3]
  bus_routes = {}

  # retrive waypoints
  for route in routes:
    # retrive waypoints
    cur = dao.get_cursor()
    cur.execute('SELECT longitud, latitud FROM ruta_puntos WHERE id_ruta=%s', (route[0],))
    waypoints = cur.fetchall()
    cur.close()

    bus_routes[route[0]] = waypoints

  return bus_routes
