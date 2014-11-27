import JobRun
import Util
import psycopg2
import time

JOB_RUN_ID_INDEX = 0
TASK_ID_INDEX = 1
START_TIME_INDEX = 2
END_TIME_INDEX = 3
STATUS_INDEX = 4

class JobRunDao:
	def __init__(self, connection):
		self.connection = connection

	def __get_last_inserted_id(self, cur):
		select_query = "SELECT MAX(JOB_RUN_ID) FROM JOB_RUN"

		cur.execute(select_query)
		return int(cur.fetchone()[0])	

	def insert(self, job_run):
		insert_query = ""
		insert_query += "INSERT INTO JOB_RUN (TASK_ID, START_TIME, END_TIME, STATUS) VALUES(%s, %s, %s, %s)"

		cur = self.connection.cursor()
		result = cur.execute(insert_query, (job_run.task_id, psycopg2.TimestampFromTicks(time.time()), None, JobRun.STATUS_RUNNING))

		last_inserted_id = self.__get_last_inserted_id(cur)
		self.connection.commit()

		return last_inserted_id
	

	def truncate(self):
		truncate_query= "TRUNCATE TABLE JOB_RUN"
		
		cur = self.connection.cursor()
		cur = cur.execute(truncate_query)
		self.connection.commit()

	def select_all(self):
		select_query = "SELECT * FROM JOB_RUN"
		
		cur = self.connection.cursor()
		
		cur.execute(select_query)
		
		rows = cur.fetchall()
		
		result_job_runs = []

		Util.debug("Rows fetched: " + str(len(rows)))
		
		for row in rows:
			result_job_runs.append(JobRun.JobRun(row[JOB_RUN_ID_INDEX], row[TASK_ID_INDEX], row[START_TIME_INDEX], row[END_TIME_INDEX], row[STATUS_INDEX]))

		return result_job_runs

	def end_job(self, job_run_id, job_status):
		Util.debug("ending job: " + str(job_run_id) + " status: " + job_status)
		update_query = "UPDATE JOB_RUN SET END_TIME = %s, STATUS = %s WHERE JOB_RUN_ID = %s"

		cur = self.connection.cursor()
		result = cur.execute(update_query, (psycopg2.TimestampFromTicks(time.time()), job_status, job_run_id))
		self.connection.commit()

		




