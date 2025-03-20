import mysql.connector

connection = mysql.connector.connect(
    host="gateway01.eu-central-1.prod.aws.tidbcloud.com",
    port=4000,
    user="3VYhXePBWtRATMR.root",
    password="0OJIXKOUfAXP7Rx9",
    database="IMDB",
    ssl_ca=r"L:\Bot\IMDBSCRAP\ca.pem",
    ssl_disabled=False
)

cursor = connection.cursor()
cursor.execute("SELECT DATABASE();")
print(cursor.fetchone())  # ✅ Check if connection works

cursor.close()
connection.close()
