from app.dao import bus_dao

def fetch_bus_info (bus_id):
  raw_data = bus_dao.read_bus_info(bus_id)

  if raw_data:
    return {
      'bus_id': raw_data[0],
      'route_id': raw_data[2],
      'is_active': raw_data[1] == 1
    }
  else:
    return None
