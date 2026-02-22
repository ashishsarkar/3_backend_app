# 3_backend_app — FastAPI backend (dev only)
# Build: docker build -t 3-backend-app .
# Run:   docker run -p 4000:4000 -e DATABASE_URL=... 3-backend-app

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 4000
ENV PORT=4000
# DATABASE_URL must be provided at runtime via docker run -e or docker-compose environment
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000", "--reload"]
