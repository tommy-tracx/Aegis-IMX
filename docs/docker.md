# Docker Guide

Run Aegis-IMX services in a containerized environment.

## Build the image

```bash
docker build -t aegis-imx .
```

## Run the container

```bash
docker run -p 8000:8000 aegis-imx
```

Visit `http://localhost:8000/docs` to explore the API.

## Docker Compose

Use Docker Compose to build and start the stack:

```bash
docker compose up --build
```

This exposes the API on `http://localhost:8000`.

