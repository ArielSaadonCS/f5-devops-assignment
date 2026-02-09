# F5 DevOps Intern Home Assignment

## Overview
This repository contains:
- **Nginx container (Ubuntu-based)** with two server blocks:
  - `8080` returns a custom HTML response
  - `8081` returns an HTTP error status
- **Test container (Python)** that validates:
  - `8080` returns `200` and contains expected HTML text
  - `8081` returns the expected error status
- **docker-compose** setup to run both containers together
- **GitHub Actions CI** that runs the compose tests and uploads an artifact:
  - `succeeded` on success
  - `fail` on failure

## Local run
```bash
docker compose up --build --abort-on-container-exit --exit-code-from test
