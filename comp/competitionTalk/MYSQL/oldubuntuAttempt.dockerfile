FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# Install MySQL and dependencies
RUN apt-get update && apt-get install -y mysql-server libaio1 && rm -rf /var/lib/apt/lists/*

# Ensure directories exist with proper permissions
RUN mkdir -p /var/lib/mysql /var/run/mysqld /docker-entrypoint-initdb.d && \
    chown -R mysql:mysql /var/lib/mysql /var/run/mysqld && \
    chmod 777 /var/run/mysqld

# Copy your initialization script
COPY init.sql /docker-entrypoint-initdb.d/

# Expose MySQL port
EXPOSE 3306

# Entrypoint script to initialize and start MySQL
CMD bash -c '\
    if [ ! -d /var/lib/mysql/mysql ]; then \
        echo "[MySQL] First run detected — initializing database..."; \
        mysqld --initialize-insecure --user=mysql; \
        mysqld_safe & \
        sleep 8; \
        echo "[MySQL] Setting root password..."; \
        mysql -uroot -e "ALTER USER '\''root'\''@'\''localhost'\'' IDENTIFIED WITH mysql_native_password BY '\''${MYSQL_ROOT_PASSWORD:-rootpass}'\''; FLUSH PRIVILEGES;"; \
        for f in /docker-entrypoint-initdb.d/*.sql; do \
            echo "[MySQL] Running init script: $f"; \
            mysql -uroot -p${MYSQL_ROOT_PASSWORD:-rootpass} < "$f"; \
        done; \
        mysqladmin -uroot -p${MYSQL_ROOT_PASSWORD:-rootpass} shutdown; \
    else \
        echo "[MySQL] Existing database found, skipping init."; \
    fi; \
    exec mysqld_safe'
