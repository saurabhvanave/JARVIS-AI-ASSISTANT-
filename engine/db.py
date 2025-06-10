import sqlite3
import csv

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# APP

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null,'onedrive', 'C:\\Program Files\\Microsoft OneDrive')"
# cursor.execute(query)
# conn.commit()

# query = "UPDATE sys_command SET path = 'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE' WHERE name = 'power point'"
# cursor.execute(query)
# conn.commit()

# query = "DELETE FROM sys_command WHERE name = 'excel'"
# cursor.execute(query)
# conn.commit()




# WEBSITE
# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'encyclopedia', 'https://www.encyclopedia.com/')"
# cursor.execute(query)
# conn.commit()


# query = "DELETE FROM web_command WHERE id = '13'"
# cursor.execute(query)
# conn.commit()



# CONTACT
# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# importing contacts from google contacts 

# desired_columns_indices = [0, 18]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# conn.commit()
# conn.close()

# for inserting contacts without google contacts 

# query = "INSERT INTO contacts VALUES (null,'abc', '1234567890','null')"
# cursor.execute(query)
# conn.commit()


# query = "DELETE FROM contacts WHERE name = 'Saurabh Vanave'"
# cursor.execute(query)
# conn.commit()

#contact search from db 

# query = 'Saurabh'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])


# CUSTMIZED ANS 

# Create a new table for general responses
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS general_responses (
#     id INTEGER PRIMARY KEY,
#     question TEXT,
#     answer TEXT
# )
# ''')
# conn.commit()

# # Insert "tell me about yourself"
# cursor.execute('''
# INSERT INTO general_responses (question, answer) VALUES (?, ?)
# ''', ("who created you", "I am J.A.R.V.I.S, I was created by SIGCE students."))
# conn.commit()



