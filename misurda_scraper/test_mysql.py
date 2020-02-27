import config
import mysql.connector

conn = mysql.connector.connect(**config.mysql)

cursor = conn.cursor()

sql = "INSERT INTO CSC335 (id, date, text) VALUES (%s, %s, %s)"
val = "1", "2/20", "Test"

for 

try:
    cursor.execute(sql, val)
except:
    pass
else:
    print("Send message: " + val)
    conn.commit()

cursor.close()
conn.close()

# cursor.execute("SHOW DATABASES")

# for x in cursor:
#     print(x)

# cursor.execute("SELECT * from authors")
# rows = cursor.fetchall()

# print('Total Row(s):', cursor.rowcount)
# for row in rows:
#     print(row)

