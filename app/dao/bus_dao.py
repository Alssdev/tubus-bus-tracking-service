import app.dao.dao as dao

# TODO: add documentation
def read_bus_info (bus_id):
  cur = dao.get_cursor()
  cur.execute('''
    SELECT
      id,
      state AS is_active,
      ruta_id AS route_id
    FROM bus
    WHERE id=%s
  ''', (bus_id,))
  bus = cur.fetchone()
  cur.close()

  return bus
