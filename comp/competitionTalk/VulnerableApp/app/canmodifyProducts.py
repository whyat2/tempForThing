import os
import mysql.connector
from Config import Config

def manage_products(output_path: str):
    """
    Connect to app2_db, create products table if missing,
    read all products, and write results to output_path.
    Each step logs to the file, even if an error occurs.
    """
    lines = []
    connection = None
    cursor = None

    try:
        # Connect to app2_db
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database="app2_db",
            port=Config.MYSQL_PORT
        )
        cursor = connection.cursor(dictionary=True)
        lines.append("Connected to app2_db")
    except Exception as e:
        lines.append(f"Failed to connect to app2_db: {e}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return

    # Step 1: Create products table if not exists
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS products2 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            price DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        lines.append("Checked/Created table 'products2'")
    except Exception as e:
        lines.append(f"Error creating table: {e}")

    # Step 2: Read all products
    try:
        cursor.execute("SELECT * FROM products;")
        products = cursor.fetchall()
        lines.append(f"Found {len(products)} products:")
        for product in products:
            lines.append(str(product))
    except Exception as e:
        lines.append(f"Error reading products: {e}")

    # Step 3: Write all lines to output file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        # Attempt to secure the file
        try:
            os.chmod(output_path, 0o600)
        except Exception:
            pass
    except Exception as e:
        print(f"Failed to write output file: {e}")

    # Cleanup
    try:
        if cursor:
            cursor.close()
    except:
        pass
    try:
        if connection:
            connection.close()
    except:
        pass
