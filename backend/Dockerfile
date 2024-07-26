# Utiliza la imagen base de Python 3.8
FROM python:3.8

# Establece el directorio de trabajo
WORKDIR /app

# Copia los requerimientos y los instala
COPY ./backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del backend
COPY backend /app

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar el servidor de FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]