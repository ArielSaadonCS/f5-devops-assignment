# Use an official Nginx image
FROM nginx:alpine

# Install openssl
RUN apk add --no-cache openssl

# Create a self-signed SSL certificate
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/nginx-selfsigned.key \
    -out /etc/ssl/certs/nginx-selfsigned.crt \
    -subj "/C=US/ST=State/L=Location/O=Organization/OU=Unit/CN=yourdomain.com"

# Copy the default Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 443
EXPOSE 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]