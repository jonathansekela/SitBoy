#!/usr/bin/env python
import mysql.connector as conn
from datetime import datetime

class SitBoySqlConn():

#region constructors
	def __init__(self, host, user, password, database, use_sql):
		if use_sql:
			self.db = conn.connect(
				# @todo: get rid of this and pass it in instead
				host="localhost",
				user="root",
				password="Thug4Lyfe",
				database="testdb"
			)
			self.cursor = self.db.cursor()
#endregion

#region public functions
	def new_player_login(self, user_id):
		print("new player detected, inserting into db...")
		qry = "INSERT INTO player_access (user_id, access_time) VALUES (%s, %s)"
		val = [(user_id, datetime.now().strftime('%F %T.%f')[:-3])]
		self.__insert(qry, val)

	def session_end(self, user_id):
		print("session end detected, inserting stop time...")
		qry = "INSERT INTO player_access (user_id, stop_time) VALUES (%s, %s)"
		val = [(user_id, datetime.now().strftime('%F %T.%f')[:-3])]
		self.__insert(qry, val)

	def new_player_demographics(self, user_id, age, eth_id, gender, game_familiarity, dog_familiarity):
		print("new player demographics detected, inserting into db...")
		qry = ""
		val = [()]
		self.__insert(qry, val)

	def animation_change(self, user_id, new_animation):
		print("animation change detected. Inserting into db...")
		qry = "INSERT INTO game_data (user_id, user_input, animation, input_is_correct, event_time) VALUES (%s, NULL, %s, 0, %s)"#@todo: make sure null works
		val = [(user_id, new_animation, datetime.now().strftime('%F %T.%f')[:-3])]
		self.__insert(qry, val)

	def user_input(self, user_id, user_input, current_animation, input_is_correct):
		print("user input detected. Inserting into db..")
		qry = "INSERT INTO game_data (user_id, user_input, animation, input_is_correct, event_time) VALUES (%s, %s, %s, %s, %s)"
		val = [(user_id, user_input, current_animation, input_is_correct, datetime.now().strftime('%F %T.%f')[:-3])]
		self.__insert(qry, val)
#endregion

#region private functions

	# qry: the sql query string
	# val: array of value tuples to insert
	def __insert(self, qry, val):
		self.cursor.executemany(qry, val)
		self.db.commit()
		print(self.cursor.rowcount, "record(s) inserted")

	# qry: the sql query string
	def __select(self, qry):
		self.cursor.execute(qry)
		result = self.cursor.fetchall()

		for x in result:
			print(x)

	# qry: the sql query string
	def __update(self, qry):
		self.cursor.execute(qry)
		self.db.commit()
		print(self.db.rowcount, "record(s) affected")
#endregion