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


# Autenticarse en GitHub Container Registry
#if this registry is private , need authenticate with -> docker login ghcr.io -u <tu-usuario-de-github> -p <tu-token-de-github>

# Descargar la imagen desde GitHub Container Registry
docker pull ghcr.io/adribaeza/llm-tinyllama-backend:latest

# Ejecutar el contenedor
docker run -d -p 8000:8000 ghcr.io/adribaeza/llm-tinyllama-backend:latest


# llm-tinyllama-backend Docker Deployment Guide

This guide provides detailed instructions on how to pull, build, run, verify, and check logs for the `llm-tinyllama-backend` Docker image from GitHub Container Registry.

## Prerequisites

- Docker Desktop installed on your machine. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop).

## Steps

### 1. Open Terminal

Open your preferred terminal application (PowerShell, cmd, Terminal on macOS, or a Linux terminal).

### 2. Pull the Docker Image

Run the following command to pull the Docker image from the GitHub Container Registry:

`docker pull ghcr.io/adribaeza/llm-tinyllama-backend:latest`

Verify Image Download
`docker images`

Run the Docker Container
`docker run -d --name llm-tinyllama-backend -p 8000:8000 ghcr.io/adribaeza/llm-tinyllama-backend:latest`
-d: Runs the container in detached mode.
--name llm-tinyllama-backend: Names the container.
-p 8000:8000: Maps port 8000 of the container to port 8000 on your machine. Adjust the ports if necessary.
ghcr.io/adribaeza/llm-tinyllama-backend:latest: Specifies the image to use.

Verify the Container is Running
docker ps

Access the Service
If the application exposes a web interface or API, access it via your web browser or tools like curl using the address http://localhost:8000 (or the port you mapped).

Check Container Logs
docker logs llm-tinyllama-backend

Stop and Remove the Container

docker stop llm-tinyllama-backend
docker rm llm-tinyllama-backend

Remove the Docker Image (if needed)
docker rmi ghcr.io/adribaeza/llm-tinyllama-backend:latest


Razones para enviar el historial completo:
Contexto: El modelo necesita el historial completo para entender el contexto de la conversación y generar respuestas adecuadas.
Coherencia: Mantener el historial ayuda a asegurar que las respuestas sean coherentes con las interacciones anteriores.
Memoria: Los modelos LLM no tienen memoria persistente entre solicitudes, por lo que necesitan el historial en cada solicitud para "recordar" lo que se ha discutido

Cómo usar docker-compose
Construir y ejecutar los servicios:
Detener los servicios:
Este archivo docker-compose.yml te permitirá levantar tanto el backend con FastAPI como el frontend con Streamlit de manera sencilla y reproducible.