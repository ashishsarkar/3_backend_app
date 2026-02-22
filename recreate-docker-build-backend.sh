#!/bin/bash

docker stop booking-backend-dev 2>/dev/null || true
docker rm booking-backend-dev 2>/dev/null || true
docker system prune -af
docker build -t booking-backend:dev .
docker run -d -p 4000:4000 --name booking-backend-dev booking-backend:dev