from flask import current_app
import psycopg2

class TrackingDAO:
  _conn = None
  _cursor = None

  @staticmethod
  def init():
    _conn = psycopg2.connect(
      database=current_app.config['DB_DATABASE'],
      host=current_app.config['DB_HOST'],
      user=current_app.config['DB_USER'],
      password=current_app.config['DB_PASSWORD'],
      port=current_app.config['DB_PORT']
    )
    print('⚡ db connection succeeded')

  @staticmethod
  def read_route_paths():
    return {}
