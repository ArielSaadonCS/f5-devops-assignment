FROM ubuntu:20.04 

# disable interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive

#download/update available packges from Ubuntu for installtion
RUN apt-get update \
#install web server
&& apt-get install -y --no-install-recommends nginx \
#remove lists downloaded by apt-get-update(for faster image)
&& rm -rf /var/lib/apt/lists/*

#remove the default ngninx site config to avoid conflicts
RUN rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default

#copy the custom nginx configuration
COPY nginx.conf etc/nginx/conf.d/f5assignment.conf
# document the ports this container will listen on
EXPOSE 8080 8081
#run nginx in foreground so the container keeps running
CMD ["nginx" , "-g" , "daemon off;"]
