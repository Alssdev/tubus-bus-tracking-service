from app import create_app
from flask import Flask

app, socketio = create_app()

if __name__ == '__main__':
  socketio.run(app, debug=True)
