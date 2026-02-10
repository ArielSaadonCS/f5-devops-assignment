# F5 DevOps Intern Home Assignment

## Overview
This project implements a small containerized web stack and automated tests using Docker and Docker Compose.

It includes:
- An **Nginx container** that exposes two endpoints:
  - Port 8080 → returns HTTP 200 with custom HTML
  - Port 8081 → returns HTTP error status (418)
- A **Python test container** that validates both endpoints automatically
- A **Docker Compose** setup to run both services together
- A **GitHub Actions CI pipeline** that runs the tests and uploads a success/fail artifact

---

## Design Decisions

- **Separate containers for app and tests**  
  Tests run in their own container to keep the web server image clean and production-like.

- **Docker Compose for orchestration**  
  Compose provides built-in networking and DNS between services, allowing the test container to reach the nginx container using the service name (`nginx`).

- **Python standard library (urllib)**  
  Used instead of external libraries to avoid extra dependencies and keep the test image small.

- **Explicit exit codes in tests**  
  Tests return exit code 0 on success and non-zero on failure so CI can fail correctly.

---

## Assumptions

- The nginx service becomes reachable within a short time window — handled with retry logic.
- Only two endpoints are required by the assignment.
- No TLS/HTTPS is required for this task.

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
- Used Alpine-based Python image for tests
- Avoided extra Python dependencies

---
## Advanced Configuration (Optional)

### HTTPS Support
The project supports HTTPS on port **8443**. A self-signed certificate is automatically generated during the Docker build process using OpenSSL.

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
