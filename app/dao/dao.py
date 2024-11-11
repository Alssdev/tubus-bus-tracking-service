from flask import current_app
import psycopg2

# databse connection
_conn = None

def init():
  global _conn

  _conn = psycopg2.connect(
    database=current_app.config['DB_DATABASE'],
    host=current_app.config['DB_HOST'],
    user=current_app.config['DB_USER'],
    password=current_app.config['DB_PASSWORD'],
    port=current_app.config['DB_PORT']
  )
  print('⚡ db connection succeeded')

def get_cursor():
  return _conn.cursor()
