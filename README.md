# abaeza-basf-python-k8s-llm-api
# Project Structure

The project is organized into two main directories: `backend` and `frontend`.

## Backend

The `backend` directory contains everything related to the FastAPI application. The structure is as follows:

- `app/main.py`: This is the main file for the FastAPI application. This is where the API is defined and the language model is loaded.
- `Dockerfile`: This file defines how the Docker image for the FastAPI application is built.
- `requirements.txt`: This file lists the Python dependencies required for the FastAPI application.
- `backend-deployment.yaml`: This is the Kubernetes configuration file for the backend Deployment.
- `backend-service.yaml`: This is the Kubernetes configuration file for the backend Service.

## Frontend

The `frontend` directory contains everything related to the Streamlit application. The structure is as follows:

- `app/main.py`: This is the main file for the Streamlit application. This is where the user interface is defined and interacts with the backend API.
- `Dockerfile`: This file defines how the Docker image for the Streamlit application is built.
- `requirements.txt`: This file lists the Python dependencies required for the Streamlit application.
- `frontend-deployment.yaml`: This is the Kubernetes configuration file for the frontend Deployment.
- `frontend-service.yaml`: This is the Kubernetes configuration file for the frontend Service.

## Deployment


Para probar tu aplicación FastAPI localmente, sigue estos pasos:

1. **Instala las dependencias**: Ejecuta `pip install -r requirements.txt` en tu terminal para instalar las dependencias necesarias.

2. **Ejecuta la aplicación**: Ejecuta `uvicorn app.main:app --reload` en tu terminal para iniciar la aplicación. El parámetro `--reload` hace que el servidor se reinicie automáticamente cada vez que cambias algún archivo de código.

3. **Abre el navegador**: Ve a `http://localhost:8000` en tu navegador para ver tu aplicación en funcionamiento. También puedes ir a `http://localhost:8000/docs` para ver la documentación interactiva de Swagger UI para tu API.

Recuerda que debes estar en el directorio correcto en tu terminal cuando ejecutes estos comandos (debería ser el directorio que contiene tu archivo `main.py` y `requirements.txt`).




#https://github.com/pablotoledo/StreamMDCollector/tree/main
