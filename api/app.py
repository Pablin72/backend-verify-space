from app import create_app
from flask_cors import CORS


# Configuración del servidor Flask
app = create_app()
CORS(app)

if __name__ == "__main__":
    # Iniciar el bot de Telegram en un hilo separado


    # Iniciar el servidor Flask
    app.run(host="0.0.0.0", port=5020)
