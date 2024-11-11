from flask import Blueprint, request, jsonify, current_app
from app.services import tracking_services

bp = Blueprint('tracking', __name__)

@bp.route('/')
def test():
  return "hello", 200
