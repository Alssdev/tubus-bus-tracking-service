import app.dao.dao as dao

def read_buses ():
  cur = dao.get_cursor()
  cur.execute('''
    SELECT
      id,
      state AS is_active,
      ruta_id AS route_id
    FROM bus
  ''')
  buses = cur.fetchall()
  cur.close()

  return buses
