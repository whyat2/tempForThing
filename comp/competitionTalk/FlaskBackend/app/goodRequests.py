import os
import mysql.connector
from Config import Config
import random
import string
import time 

connection = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DB,
    port=Config.MYSQL_PORT
)

cursor = connection.cursor()

def random_string(length=6):
    """Generate a random lowercase string of given length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

try:
    while True:
        # Create random name and email
        name = random_string(8).capitalize()
        email = f"{random_string(6)}@{random_string(5)}.com"

        # Insert data
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (name, email)
        )
        connection.commit()

        print(f"Inserted: {name} - {email}")

        # Query and print all data
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            print(row)

        # Wait 5 second
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    cursor.close()
    connection.close()

