import ConnectionUtil
import TaskDao
import Task
import os
import Util
import threading
import JobRunDao
import JobRun
import datetime

TASK_DAO = TaskDao.TaskDao(ConnectionUtil.get_connection())
JOB_RUN_DAO = JobRunDao.JobRunDao(ConnectionUtil.get_connection())

def start_job_run(task):
	Util.debug("start_job_run" + str(task.task_id))
	j = JobRun.JobRun(1, task.task_id, None, None, None)
	return JOB_RUN_DAO.insert(j)

def end_job_run(job_run_id, status):
	Util.debug("end_job_run" + str(job_run_id))
	JOB_RUN_DAO.end_job(job_run_id, status)

def do_run(task, job_run_id):
	result = os.system(task.command)
	status = JobRun.STATUS_SUCCESS if result == 0 else JobRun.STATUS_FAIL
	end_job_run(job_run_id, status)

def get_hourly_tasks(tasks):
	ret_tasks = []
	for task in tasks:
		if task.frequency == Task.FREQ_HOURLY:
			ret_tasks.append(task)
	return ret_tasks

def get_weekly_tasks(tasks):
	ret_tasks = []
	for task in tasks:
		if task.frequency == Task.FREQ_WEEKLY and task.day_of_week == datetime.datetime.toda().weekday() and task.hour == datetime.datetime.today().hour:
			ret_tasks.append(task)
	return ret_tasks

def get_daily_tasks(tasks):
	ret_tasks = []
	for task in tasks: 
		if task.frequency == Task.FREQ_DAILY and task.hour == datetime.datetime.today().hour:
			ret_tasks.append(task)
	return ret_tasks

def get_montly_tasks(tasks):
	ret_tasks = []
	for task in tasks:
		if task.frequency == Task.FREQ_MONTHLY and task.day_of_month == datetime.datetime.toda().day and task.hour == datetime.datetime.today().hour:
			ret_tasks.append(task)
	return ret_tasks

def run():
	tDao = TaskDao.TaskDao(ConnectionUtil.get_connection())
	tasks = tDao.select_all()
	tasks_to_run = []
	tasks_to_run.extend(get_hourly_tasks(tasks))
	tasks_to_run.extend(get_daily_tasks(tasks))
	tasks_to_run.extend(get_weekly_tasks(tasks))
	tasks_to_run.extend(get_montly_tasks(tasks))
	print (tasks_to_run)
	for task in tasks_to_run:
		job_run_id = start_job_run(task)
		t = threading.Thread(target=do_run, args = (task, job_run_id, ))
		t.daemon = False
		t.start()
		
def main():
	run()

if __name__ == '__main__':
	main()
