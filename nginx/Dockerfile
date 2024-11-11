# Dockerfile for Nginx
FROM nginx:alpine

# Copy the custom Nginx configuration file
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Copy the static files from the Django container
COPY ./staticfiles_build/static /usr/share/nginx/html/static

# Expose port 80 for Nginx
EXPOSE 80
