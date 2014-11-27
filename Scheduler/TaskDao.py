import Task
import Util

TASK_ID_INDEX = 0
NAME_INDEX = 1
FREQUENCY_INDEX = 2
MONTH_INDEX = 3
DAY_OF_WEEK_INDEX = 4
DAY_OF_MONTH_INDEX = 5
HOUR_INDEX = 6
COMMAND_INDEX = 7


class TaskDao:
	def __init__(self, connection):
		self.connection = connection
	
	def __get_last_inserted_id(self):
		select_query = "SELECT MAX(TASK_ID) FROM TASK"

		cur = self.connection.cursor()
		cur.execute(select_query)
		return int(cur.fetchone()[0])	

	def insert(self, task):
		insert_query = "INSERT INTO TASK (NAME, FREQUENCY, MONTH, DAY_OF_WEEK, DAY_OF_MONTH, HOUR, COMMAND) VALUES (%s, %s, %s, %s, %s, %s, %s)"

		cur = self.connection.cursor()
		result = cur.execute(insert_query, (task.name, task.frequency, task.month, task.day_of_week, task.day_of_month, task.hour, task.command));
		self.connection.commit()

		return self.__get_last_inserted_id()

	def truncate(self):
		truncate_query = "TRUNCATE TABLE TASK CASCADE"

		Util.debug(truncate_query)

		cur = self.connection.cursor()

		cur.execute(truncate_query)

	def select_all(self):
		select_query = "SELECT * FROM TASK"
		cur = self.connection.cursor()

		Util.debug(select_query)

		cur.execute(select_query)

		rows = cur.fetchall()

		result_tasks = []
		
		for row in rows:
			result_tasks.append(Task.Task(row[TASK_ID_INDEX], row[NAME_INDEX], row[FREQUENCY_INDEX], int(row[MONTH_INDEX]), int(row[DAY_OF_WEEK_INDEX]), int(row[DAY_OF_MONTH_INDEX]), int(row[HOUR_INDEX]), row[COMMAND_INDEX]))

		return result_tasks;
