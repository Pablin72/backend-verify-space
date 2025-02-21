from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    # Configurar la clave secreta para la sesión
    app.secret_key = os.urandom(24)

    from app.routes.video_controller import video_bp
    from app.routes.objects_controller import object_bp

    app.register_blueprint(video_bp)
    app.register_blueprint(object_bp)

    
    return app