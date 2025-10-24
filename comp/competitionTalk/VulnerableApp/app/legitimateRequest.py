import mysql.connector
from Config import Config

def add_product(name: str, price: float):
    """
    Connect to app2_db and insert a new product into the products table.
    """
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
        cursor = connection.cursor()
        
        # Insert the product
        insert_query = "INSERT INTO products (name, price) VALUES (%s, %s);"
        cursor.execute(insert_query, (name, price))
        connection.commit()
        print(f"Product '{name}' added with price {price}")
        
    except Exception as e:
        print(f"Error adding product: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
