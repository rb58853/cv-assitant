#syntax=docker/dockerfile:1.2
FROM python:3.11.2

# Set working directory
WORKDIR /

# Copy all files and directories
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Configurar las variables de entorno
# ARG OPENAI_API_KEY
# ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--ws-ping-interval", "0", "--ws-ping-timeout", "180", "--workers", "4"]


