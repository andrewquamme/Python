import mysql.connector
import config
# import configparser

# config = configparser.ConfigParser()
# config.read('config.ini')
# host = config['mysql']['host']
# user = config['mysql']['user']
# pwd = config['mysql']['password']

# mydb = mysql.connector.connect(
#     host=host,
#     user=user,
#     password=pwd
# )

conn = mysql.connector.connect(**config.mysql)
cursor = conn.cursor()
cursor.execute("SELECT * from authors")
rows = cursor.fetchall()

print('Total Row(s):', cursor.rowcount)
for row in rows:
    print(row)

cursor.close()
conn.close()
