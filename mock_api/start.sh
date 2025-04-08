#! /bin/bash
docker build -t mock-api -f api.dockerfile .
docker run -d \
  --name mock-api \
  --network app-network \
  -p 8000:8000 \
  mock-api