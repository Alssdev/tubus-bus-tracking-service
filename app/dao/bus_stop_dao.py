import app.dao.dao as dao

def read_bus_stops():
  cur = dao.get_cursor()
  cur.execute('''
    SELECT
      id,
      latitud AS lat,
      longitud AS lng,
      id_ruta AS route_id
    FROM paradas
    WHERE id_ruta = 1
  ''')
  bus_stops = cur.fetchall()
  cur.close()

  return bus_stops
