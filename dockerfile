#syntax=docker/dockerfile:1.2
FROM python:3.11.2-slim

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Configurar las variables de entorno
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Expose port
EXPOSE 8080

# Set working directory
WORKDIR /app

# Copy all files and directories
COPY . .

# Run the app
CMD ["uvicorn", "src.app.api.api:app", "--host", "0.0.0.0", "--port", "8080", "--ws-ping-interval", "0", "--ws-ping-timeout", "180", "--workers", "4"]


