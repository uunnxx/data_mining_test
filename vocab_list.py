import re
import sqlite3 as sql


DB = "./static/dict.db"

sql_connection = sql.connect(DB)
cursor = sql_connection.cursor()

# k1, reading, tr


cursor.execute("SELECT tr FROM dict LIMIT 10")
print(f"{cursor.fetchall()}")


sql_connection.close()
