import os
import mysql.connector
from Config import Config

def check_price_column_encryption(output_path: str):
    """
    Connect to app2_db, check if products table exists,
    and check if the price column is likely encrypted at rest.
    Write the results to a file.
    """
    lines = []
    connection = None
    cursor = None

    try:
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

    # Step 1: Check if products table exists
    try:
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = 'app2_db' AND TABLE_NAME = 'products' AND COLUMN_NAME = 'price';
        """)
        column_info = cursor.fetchone()
        if column_info:
            lines.append(f"Column 'price' exists with data type: {column_info['DATA_TYPE']}")
        else:
            lines.append("Column 'price' does not exist.")
    except Exception as e:
        lines.append(f"Error checking price column: {e}")

    # Step 2: Inspect sample data to infer encryption
    try:
        cursor.execute("SELECT price FROM products LIMIT 5;")
        rows = cursor.fetchall()
        if rows:
            encrypted_hint = False
            for row in rows:
                val = row['price']
                # If numeric column contains non-numeric data, hint at encryption
                if isinstance(val, (bytes, str)):
                    encrypted_hint = True
            if encrypted_hint:
                lines.append("Price column may be encrypted (non-numeric data found).")
            else:
                lines.append("Price column does not appear to be encrypted at rest.")
        else:
            lines.append("No data in products table to check for encryption.")
    except Exception as e:
        lines.append(f"Error reading price column: {e}")

    # Step 3: Write results to file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
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
