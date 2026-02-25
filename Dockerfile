FROM python:3.12-slim

# Evita warnings y hace pip más rápido/limpio
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia requirements primero → cachea la instalación pesada
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el código fuente
COPY . .

# Puerto (ajusta si usas otro)
EXPOSE 8000

# CMD que usa python -m (más robusto, no depende de binarios en PATH)
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]