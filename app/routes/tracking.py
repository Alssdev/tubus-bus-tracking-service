from flask import Blueprint, request, jsonify, current_app
from ..services.tracking_services import TrackingService

bp = Blueprint('tracking', __name__)

@bp.route('/')
def test():
  return "hello", 200
