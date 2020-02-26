import sqlite3 #imports SQLite library to allow database saving
from sqlite3 import Error

class Sql:
	def __init__(self):
		self.db_file = "libary_db.db" #library DB file
		self.create_connection() 

	def create_connection(self): #initialises a connection to the database
		#create a database connection to a SQLite database
		try:
			db = sqlite3.connect(self.db_file)
			#print(sqlite3.version)
			self.init_tables(db)
		except Error as e:
			print(e)
		finally:
			db.close() #closes sql connection after query to optimise memory usage

	def init_tables(self, db): #loads the table if they are not present before (for first creation of database)
		cursor = db.cursor()
		cursor.execute("""CREATE TABLE IF NOT EXISTS data (
						 id integer PRIMARY KEY,
						 title text NOT NULL,
						 description text NOT NULL,
						 issuer_name text,
						 issue_status text,
						 date_issued text,
						 date_due text
						);
						 """)

	def insert(self, item): #adds support for other queries to be added to the program easily
		db = sqlite3.connect(self.db_file)
		cursor = db.cursor() 
		try:
			item_data = (item.uid, item.title, item.description, item.issuer_name, item.issued, item.date_issued, item.date_due)
			cursor.execute("""INSERT into data(id, title, description, issuer_name, issue_status, date_issued, date_due)
							VALUES(?,?,?,?,?,?,?)""", item_data)
			db.commit() #saves to the database
		except Error as e:
			print(e) #prints the error if there is an error with the query
		finally:
			db.close() #closes connection to the database so it is no longer in memory

	def delete(self, uid): #adds support for other queries to be added to the program easily
		db = sqlite3.connect(self.db_file)
		cursor = db.cursor()
		try:

			cursor.execute("DELETE FROM data WHERE id={}".format(uid))
			db.commit() #saves change to the database to the file
		except Error as e: 
			print(e)  #prints the error if there is an error with the query
		finally:
			db.close() #closes connection to the database so it is no longer in memory

	def update(self, item): #updates user data to set issued status / details
		db = sqlite3.connect(self.db_file)
		cursor = db.cursor()
		try:
			item_data = (item.issuer_name, item.issued, item.date_issued, item.date_due, item.uid)
			cursor.execute("""UPDATE data SET issuer_name=?, issue_status=?, date_issued=?, date_due=? WHERE id=?
				""", item_data)
			db.commit() #saves the change to the database file
		except Error as e:
			print(e) #prints the error if the query has an error
		finally:
			db.close() #closes the DB so it is no longer loaded to memory

	def fetch(self): #fetches and returns ALL data from the database, so that it can be loaded into the program's memory
		db = sqlite3.connect(self.db_file)
		cursor = db.cursor()
		data = cursor.execute("SELECT * from data").fetchall()
		db.close()
		return data

	def get_uids(self): #gets all unique ID's from the database and returns them to the main program
		db = sqlite3.connect(self.db_file)
		db.row_factory = lambda cursor, row: row[0]
		cursor = db.cursor()
		uids = cursor.execute("SELECT id from data").fetchall()
		db.close()

		return uids

if __name__ == "__main__": #lets the user know this program is meant to be run as a package, not as a standalone program
	print("This program is meant as a package, not to be executed")