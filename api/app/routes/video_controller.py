from flask import Blueprint, jsonify, request, send_file, Response, session

from app.yolo_detector import generate_frames



video_bp = Blueprint('video_bp', __name__)


# Endpoint para servir el video en tiempo real
@video_bp.route('/video_feed')
def video_feed():
    # Extraer los objetos requeridos de la sesión
    required_counts = session.get('required_counts', {})
    return Response(generate_frames(required_counts), mimetype='multipart/x-mixed-replace; boundary=frame')