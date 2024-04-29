FROM python:3.10.14

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt y luego instalar las dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar archivos y directorios específicos al directorio de trabajo (/app)
COPY . .

# Ejecutar la aplicación cuando el contenedor se inicie
CMD ["python", "app.py"]
