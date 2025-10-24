import os
import mysql.connector
from Config import Config

def getUnencryptedPass(output_path: str):
    """
    Connect to the MySQL `mysql.user` table and write details for `app1_user`
    (and an example system user 'root') into the file at output_path.
    Writes lines even if parts fail.
    """
    lines = []

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database="mysql",
            port=Config.MYSQL_PORT
        )
        cursor = connection.cursor(dictionary=True)
        lines.append("Connected to MySQL system database")
    except Exception as e:
        lines.append(f"Failed to connect to MySQL: {e}")
        # write what we have so far
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return  # cannot proceed without connection

    # Try to fetch app1_user
    try:
        cursor.execute(
            "SELECT user, host, authentication_string FROM `user` WHERE user = 'app1_user' LIMIT 1;"
        )
        user = cursor.fetchone()
        if user:
            auth_str = user.get('authentication_string')
            lines.append(f"User: {user.get('user')}, Host: {user.get('host')}")
            if auth_str is None or auth_str == '':
                lines.append("  No password set")
            elif auth_str.startswith('*') and len(auth_str) == 41:
                lines.append("  Password is a MySQL SHA1 hash")
            elif auth_str.startswith('$A$') or auth_str.startswith('$2a$') or auth_str.startswith('$2y$'):
                lines.append("  Password is hashed (bcrypt or old MySQL format)")
            else:
                lines.append("  Possibly plain text or unknown format")
        else:
            lines.append("User app1_user not found.")
    except Exception as e:
        lines.append(f"Error fetching app1_user: {e}")

    # Try to fetch example system user 'root'
    try:
        username = "root"
        cursor.execute("SELECT * FROM `user` WHERE `user` = %s LIMIT 1;", (username,))
        sys_user = cursor.fetchone()
        if sys_user:
            lines.append(f"\nSystem user {username} found:")
            for k, v in sys_user.items():
                lines.append(f"  {k}: {v}")
        else:
            lines.append(f"\nSystem user {username} not found.")
    except Exception as e:
        lines.append(f"Error fetching system user {username}: {e}")

    # Write all collected lines
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        # Secure the file (best-effort)
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
