import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='98012243a',
    database='second_bot'
 )
cursor = db.cursor()

print(db)
# # create database
# cursor.execute("CREATE DATABASE second_bot")
# # create table data base
# cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY,\
#                first_name VARCHAR(255),\
#                last_name VARCHAR(255),\
#                user_id INT UNIQUE)")

# # create table data base
# cursor.execute("CREATE TABLE catalog (id INT AUTO_INCREMENT PRIMARY KEY,\
#                catalog_name VARCHAR(255),\
#                catalog_id INT UNIQUE)")

# cursor.execute("ALTER TABLE users ADD COLUMN (role VARCHAR(255))")
# db.commit()

# create table products
# cursor.execute("CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY,\
#                product_name VARCHAR(255) ,\
#                product_id VARCHAR(255) UNIQUE,\
#                catalog_id VARCHAR(255))")
# db.commit()

# cursor.execute("ALTER TABLE products ADD COLUMN
# (description VARCHAR (255), product_price INT (20), photo_id VARCHAR (100))")
# db.commit()
