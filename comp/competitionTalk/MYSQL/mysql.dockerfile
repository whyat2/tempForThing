# Use the official MySQL image as base
FROM mysql:8.0.32

# Create directories for persistent logs
RUN mkdir -p /var/log/mysql && chown -R mysql:mysql /var/log/mysql \
    && mkdir -p /var/lib/mysql-files && chown -R mysql:mysql /var/lib/mysql-files

# Copy custom MySQL configuration
COPY my.cnf /etc/mysql/conf.d/audit.cnf

# Copy initialization scripts if needed (optional)
COPY ./init.sql /docker-entrypoint-initdb.d/

# Expose MySQL port
EXPOSE 3306

# Default command (from base image)
CMD ["mysqld"]