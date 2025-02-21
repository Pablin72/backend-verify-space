from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import json
from app.yolo_detector import model

import app.yolo_detector as yolo


object_bp = Blueprint('object_bp', __name__, url_prefix='/objects')

@object_bp.route('/', methods=['GET', 'POST'])
def object_form():
    object_options = model.names if hasattr(model, "names") else {}
    if not isinstance(object_options, dict):
        object_options = {}

    if request.method == 'POST':
        objects_str = request.form.get('objects')
        try:
            required_objects = json.loads(objects_str)
        except Exception as e:
            return render_template('object_form.html', error="Formato JSON inválido.", object_options=object_options)

        session['required_counts'] = required_objects
        return redirect(url_for('object_bp.verify'))

    return render_template('object_form.html', object_options=object_options)

@object_bp.route('/verify')
def verify():
    required_counts = session.get('required_counts', {})
    return render_template('object_verification.html', required_counts=required_counts)

@object_bp.route('/verification_status')
def verification_status():
    required_objects = session.get('required_counts', {})
    return jsonify({
        "verification_complete": yolo.VERIFICATION_COMPLETE,
        "required_counts": required_objects,
        "current_counts": yolo.LAST_COUNTS
    })