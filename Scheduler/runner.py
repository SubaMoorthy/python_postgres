import ConnectionUtil
import TaskDao
import Task
import os
import Util
import threading
import JobRunDao
import JobRun
import datetime
from optparse import OptionParser

def start_job_run(job_run_dao,task):
	Util.debug("start_job_run" + str(task.task_id))
	j = JobRun.JobRun(1, task.task_id, None, None, None)
	return job_run_dao.insert(j)

def end_job_run(job_run_dao, job_run_id, status):
	Util.debug("end_job_run" + str(job_run_id))
	job_run_dao.end_job(job_run_id, status)

def do_run(job_run_dao, task, job_run_id):
	command = "cd %s & %s" %(task.folder, task.command)
	Util.debug(command)
	result = os.system(command)
	status = JobRun.STATUS_SUCCESS if result == 0 else JobRun.STATUS_FAIL
	end_job_run(job_run_dao, job_run_id, status)

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

def run(job_run_dao, tasks):
	for task in tasks:
		job_run_id = start_job_run(job_run_dao, task)
		t = threading.Thread(target=do_run, args = (job_run_dao, task, job_run_id, ))
		t.daemon = False
		t.start()

def run_all(job_run_dao, task_dao):
	tasks = task_dao.select_all()
	tasks_to_run = tasks
	tasks_to_run = []
	tasks_to_run.extend(get_hourly_tasks(tasks))
	tasks_to_run.extend(get_daily_tasks(tasks))
	tasks_to_run.extend(get_weekly_tasks(tasks))
	tasks_to_run.extend(get_montly_tasks(tasks))
	print (tasks_to_run)
	run(job_run_dao, tasks_to_run)
	#run(job_run_dao, tasks)

def run_by_task_id(job_run_dao, task_dao, task_id):
	tasks = task_dao.load_by_id(task_id)

	if len(tasks) == 0:
		Util.error("There not tasks with id of : " + task_id)
		return
	
	run(job_run_dao, tasks)
	
		
def main():
	parser = OptionParser()
	parser.add_option("-t", "--task-id", dest="task_id", default=None)
	parser.add_option("-c", "--config-path", dest="config_path", default=None)
	(options, args) = parser.parse_args()
	task_id = options.task_id
	config_path = options.config_path

	task_dao = TaskDao.TaskDao(ConnectionUtil.get_connection(config_path))
	job_run_dao = JobRunDao.JobRunDao(ConnectionUtil.get_connection(config_path))

	if (task_id is not None):
		run_by_task_id(job_run_dao, task_dao, task_id)
	else:
		run_all(job_run_dao, task_dao)

if __name__ == '__main__':
	main()
