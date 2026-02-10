FROM ubuntu:20.04

# Disable interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Nginx and OpenSSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx openssl && \
    rm -rf /var/lib/apt/lists/*

# Generate self-signed SSL certificate
RUN mkdir -p /etc/nginx/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/certs/selfsigned.key \
    -out /etc/nginx/certs/selfsigned.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Remove default config
RUN rm -f /etc/nginx/sites-enabled/default

# Copy custom config
COPY nginx.conf /etc/nginx/conf.d/f5assignment.conf

# Expose HTTP and HTTPS ports
EXPOSE 8080 8081 8443

CMD ["nginx", "-g", "daemon off;"]