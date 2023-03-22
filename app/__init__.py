from flask import Flask
from config import Config
from flask_cors import CORS


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, supports_credentials=True)

    from app.module import bp as module_bp

    app.register_blueprint(module_bp, url_prefix="/module")
    from app.system import bp as system_bp

    app.register_blueprint(system_bp, url_prefix="/system")
    from app.graph import bp as graph_bp

    app.register_blueprint(graph_bp, url_prefix="/graph")
    return app
