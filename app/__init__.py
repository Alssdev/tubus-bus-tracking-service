from flask import Flask

from app.services import tracking_services
from .config import Config
from .routes import tracking
from .dao import dao

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    # blueprints
    app.register_blueprint(tracking.bp, url_prefix="/api/tracking")

    # init db
    dao.init()

    # init services
    tracking_services.init()

    return app
