import cv2
from ultralytics import YOLO
import os
import time
from logging import getLogger
import random

logger = getLogger(__name__)

# Cargar el modelo YOLOv8 pre-entrenado
model = YOLO('yolov8s.pt')  # Cambiar por el modelo necesario

cap_source = 0

colors = {}

def get_color(class_id):
    if class_id not in colors:
        colors[class_id] = tuple(random.randint(0, 255) for _ in range(3))
    return colors[class_id]

# Variables globales para indicar si se completó la verificación y para debug
VERIFICATION_COMPLETE = False
LAST_COUNTS = {}

def generate_frames(required_counts):
    global VERIFICATION_COMPLETE, LAST_COUNTS
    VERIFICATION_COMPLETE = False
    LAST_COUNTS = {}
    
    logger.info("Intentando conectar a la cámara de la computadora")
    cap = cv2.VideoCapture(cap_source)
    if not cap.isOpened():
        logger.error("Error: No se puede abrir la cámara")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            logger.error("Error: No se pudo leer el frame")
            break

        logger.debug("Procesando frame con YOLO")
        results = model(source=frame, conf=0.5)
        detections = results[0].boxes if results and results[0].boxes is not None else []
        current_counts = {}

        for det in detections:
            x1, y1, x2, y2 = map(int, det.xyxy[0])
            confidence = det.conf.item()
            class_id = int(det.cls)
            object_name = model.names[class_id] if hasattr(model, "names") and class_id in model.names else str(class_id)
            label = f"{object_name}: {confidence:.2f}"
            color = get_color(class_id)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            current_counts[object_name] = current_counts.get(object_name, 0) + 1

        # Actualizar variable global para debug
        LAST_COUNTS = current_counts.copy()

        # Mostrar conteos actuales en el frame
        y0 = 20
        for i, (obj_name, count) in enumerate(current_counts.items()):
            text = f"{obj_name}: {count}"
            cv2.putText(frame, text, (10, y0 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        logger.info(f"Requerido: {required_counts}, Actual: {current_counts}")
        
        # Si se definieron requerimientos, comprobar si se cumple la verificación
        if required_counts:
            match_count = 0
            total_items = len(required_counts)
            y_start = 20 + len(current_counts) * 20 + 20
            for j, (req_obj, req_count) in enumerate(required_counts.items()):
                current = current_counts.get(req_obj, 0)
                text = f"Requerido - {req_obj}: {req_count} | Actual: {current}"
                print(text)
                cv2.putText(frame, text, (10, y_start + j * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                if current >= req_count:
                    match_count += 1
            if total_items > 0 and match_count == total_items:
                VERIFICATION_COMPLETE = True
                cv2.putText(frame, "Verificación Completa", (10, y_start + (j + 1) * 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
                break

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()
    logger.info("Cámara liberada.")