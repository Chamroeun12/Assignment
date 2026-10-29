# Small, sensible base image following Docker best practices
FROM nginx:alpine

# Remove default configuration
RUN rm -f /etc/nginx/conf.d/default.conf

# Copy custom Nginx reverse proxy / load balancer configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose HTTP port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://127.0.0.1/nginx-health || exit 1

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
