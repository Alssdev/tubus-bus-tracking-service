from flask import Flask

from app.config import Config
from app.routes import places
from app.routes import tracking
from app.routes import buses
from app.routes import stops
from app.routes import routes
from app.dao import dao

from app import websockets

import logging

app = None

def create_app():
  global app
  global socketio

  app = Flask(__name__)
  log = logging.getLogger('werkzeug')
  log.setLevel(logging.ERROR)

  socketio = websockets.create_socketio(app)
  app.config.from_object(Config)
  app.app_context().push()

  # blueprints
  app.register_blueprint(tracking.bp, url_prefix="/api/tracking")
  app.register_blueprint(buses.bp, url_prefix="/api/buses")
  app.register_blueprint(stops.bp, url_prefix="/api/paradas")
  app.register_blueprint(routes.bp, url_prefix="/api/rutas")
  app.register_blueprint(places.bp, url_prefix='/api/places')

  # init db
  dao.init()

  # init services
  from app.services import tracking_services
  tracking_services.init()

  return app, socketio
