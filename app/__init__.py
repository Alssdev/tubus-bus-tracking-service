from flask import Flask
from .config import Config
from .routes import tracking
from .dao.tracking_dao import TrackingDAO

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    # blueprints
    app.register_blueprint(tracking.bp, url_prefix="/api")

    # init db
    TrackingDAO.init()

    return app
