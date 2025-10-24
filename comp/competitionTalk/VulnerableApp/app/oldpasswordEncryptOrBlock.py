
import mysql.connector
from Config import Config


def getUnencryptedPass():
    try:
    # Connect to MySQL (no specific database, or you can keep your Config.MYSQL_DB)
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database="mysql",  # system database
            port=Config.MYSQL_PORT
        )

        if connection.is_connected():
            print("Connected to MySQL system database")

        cursor = connection.cursor(dictionary=True)  # dictionary rows

        # Fetch all users from mysql.user
        cursor.execute("SELECT user, host, authentication_string FROM `user` WHERE user = 'app1_user';")
        user = cursor.fetchone()
        
        if user:
            auth_str = user['authentication_string']
            print(f"User: {user['user']}, Host: {user['host']}")
            
            if auth_str is None or auth_str == '':
                print("  No password set")
            elif auth_str.startswith('*') and len(auth_str) == 41:
                print("  Password is a MySQL SHA1 hash")
            elif auth_str.startswith('$A$') or auth_str.startswith('$2a$') or auth_str.startswith('$2y$'):
                print("  Password is hashed (bcrypt or old MySQL format)")
            else:
                print("  Possibly plain text or unknown format")
        else:
            print("User app1_user not found.")

        # Fetch a single user by username
        username = "root"  # example system user
        cursor.execute("SELECT * FROM `user` WHERE `user` = %s LIMIT 1;", (username,))
        user = cursor.fetchone()
        if user:
            print(f"\nSystem user {username} found:")
            print(user)
        else:
            print(f"\nSystem user {username} not found.")

    except mysql.connector.Error as e:
        print("Error accessing MySQL:", e)

    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("Connection closed")