from flask import Flask

from .config import Config
from .routes import tracking
from .routes import buses
from .dao import dao

from app import websockets

app = None

def create_app():
  global app
  global socketio

  app = Flask(__name__)
  socketio = websockets.create_socketio(app)
  app.config.from_object(Config)
  app.app_context().push()

  # blueprints
  app.register_blueprint(tracking.bp, url_prefix="/api/tracking")
  app.register_blueprint(buses.bp, url_prefix="/api/buses")

  # init db
  dao.init()

  # init services
  from app.services import tracking_services
  tracking_services.init()

  return app, socketio
