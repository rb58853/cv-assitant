#syntax=docker/dockerfile:1.2
FROM python:3.11.2-slim

# Set working directory
WORKDIR /app

# Copy all files and directories
COPY . .

# RUN --mount=type=secret,id=typesense_cloud_api_key \
#     --mount=type=secret,id=openai_api_key \
#     --mount=type=secret,id=openai_org_token \
#     --mount=type=secret,id=openai_proj_token \
#     sed -i "s/TYPESENSE_CLOUD_API_KEY=/TYPESENSE_CLOUD_API_KEY=$(cat /run/secrets/typesense_cloud_api_key)/" .env.example \
#     && sed -i "s/OPENAI_API_KEY=/OPENAI_API_KEY=$(cat /run/secrets/openai_api_key)/" .env.example \
#     && sed -i "s/OPENAI_ORG_TOKEN=/OPENAI_ORG_TOKEN=$(cat /run/secrets/openai_org_token)/" .env.example \
#     && sed -i "s/OPENAI_PROJ_TOKEN=/OPENAI_PROJ_TOKEN=$(cat /run/secrets/openai_proj_token)/" .env.example \
#     && mv .env.example .env

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run the app

CMD ["uvicorn", "src.app.api.api:app", "--host", "0.0.0.0", "--port", "8080", "--ws-ping-interval", "0", "--ws-ping-timeout", "1200", "--workers", "8"]


