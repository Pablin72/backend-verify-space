# Guía para Ejecutar la Aplicación

## 1. Crear y Activar un Entorno Virtual
Se recomienda usar un entorno virtual para instalar las dependencias de la aplicación de manera aislada.

### En Windows (CMD o PowerShell):
```sh
python -m venv venv
venv\Scripts\activate
```

### En macOS y Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

## 2. Instalar Dependencias
Con el entorno virtual activado, instala las dependencias requeridas:
```sh
pip install -r requirements.txt
```

## 3. Configurar Variables de Entorno (Opcional)
Si la aplicación requiere variables de entorno, configúralas antes de ejecutar el servidor.

## 4. Ejecutar la Aplicación
Ejecuta el siguiente comando para iniciar el servidor Flask:
```sh
python api/app.py
```

## 5. Acceder a la Aplicación
Una vez que el servidor esté corriendo, abre tu navegador y accede a:
```
http://127.0.0.1:5020/objects/
```

## 6. Detener la Aplicación
Para detener la ejecución, presiona `Ctrl + C` en la terminal donde se está ejecutando el servidor.

## 7. Desactivar el Entorno Virtual
Cuando termines de trabajar con la aplicación, puedes desactivar el entorno virtual con:
```sh
deactivate
```
