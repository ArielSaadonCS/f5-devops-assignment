# F5 DevOps Intern Home Assignment

## Overview
This project implements a containerized web stack and automated tests using Docker and Docker Compose.

It includes:
- An **Nginx container** that exposes two endpoints:
  - Port 8080 → returns HTTP 200 with custom HTML
  - Port 8081 → returns HTTP error status (418)
- A **Python test container** that validates both endpoints automatically
- A **Docker Compose** setup to run both services together
- A **GitHub Actions CI pipeline** that runs the tests and uploads a success/fail artifact

---

## Design Decisions
  
- **Modular Project Structure**
  Separated configuration and Dockerfiles into dedicated directories (`nginx/`, `tests/`) to maintain a clean root directory and separate concerns effectively.
  
- **Minimal Attack Surface & Optimization**
  Used `--no-install-recommends` and cleaned up apt lists in the Dockerfile. This reduces the image size and minimizes potential security vulnerabilities by excluding unnecessary packages.

- **Python standard library (urllib)**  
  Used instead of external libraries to avoid extra dependencies and keep the test image small.

- **Explicit exit codes in tests**  
  Tests return exit code 0 on success and non-zero on failure so CI can fail correctly.
  
- **"Burst" Strategy for Rate Limiting**
  Strictly enforcing 5 requests/second can harm user experience in real-world scenarios. I configured Nginx with `burst=5 nodelay`, which strictly enforces the average rate but allows for small, traffic spikes without immediate rejection.

- **Minimalist Test Image (Alpine)**
  Chose python:3.12-alpine to keep the test image lightweight and speed up CI pulls/builds.

- **Resiliency / Retry Logic**
  Implemented a custom retry mechanism (`wait_until_up`) within the test script. Since Docker Compose starts containers simultaneously, this logic ensures the tests strictly wait for Nginx to be fully ready before execution, preventing flaky failures due to race conditions.

- **Fail-Fast CI Pipeline**
   configured the CI to use `docker compose up --abort-on-container-exit`. This ensures that as soon as the tests complete, the environment creates a teardown event, saving CI resources and providing quicker feedback loops.
  
- **Self-Contained SSL Generation**
  Generated a self-signed certificate during build for the assignment, to keep the project self contained. In production, certificates would be provided via a proper CA and secret management.

---

## Assumptions

- The nginx service becomes reachable within a short time window — handled with retry logic.
- Only two endpoints are required by the assignment.
- No TLS/HTTPS is required for the first part.

---

## Trade-offs

- **Ubuntu base image for nginx** — larger than the official nginx image, but chosen for clarity and explicit package installation steps.
- **Alpine Python image for tests** — very small, but sometimes less compatible with complex packages (acceptable here since only stdlib is used).
- **No healthcheck in compose** — readiness handled in test script instead (simpler but less declarative).

---

## Image Size Optimization

Steps taken to reduce image size:
- Used `--no-install-recommends` in apt installs
- Removed apt package lists after install
- Used Alpine based python image for tests
- Avoided extra python dependencies

---
## Advanced Configuration

### HTTPS Support
The project supports HTTPS on port **8443**. A self signed certificate is automatically generated during the Docker build process using OpenSSL.

### Rate Limiting Configuration
Rate limiting is enabled to prevent abuse.

* **How it works:**
  Nginx uses the `limit_req_zone` directive to track requests per IP address.
  - **Rate:** 5 requests per second (`5r/s`).
  - **Burst:** A buffer of 5 requests (`burst=5`) allows for small traffic spikes.
  - **Behavior:** Requests exceeding the rate + burst buffer are rejected with HTTP 503.

* **How to change the rate limit threshold:**
  1. Open `nginx/nginx.conf`.
  2. Modify the `rate` value in: `limit_req_zone $binary_remote_addr zone=mylimit:10m rate=5r/s;`.
  3. Modify the `burst` value in the `location /` blocks if needed.
  4. Rebuild the container: `docker compose up --build`.
  
  ---

## How to Build and Run Locally

```bash
docker compose up --build --abort-on-container-exit --exit-code-from test
