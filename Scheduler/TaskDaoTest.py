import Task
import ConnectionUtil
import TaskDao
import JobRunDao

TASK_DAO = TaskDao.TaskDao(ConnectionUtil.get_connection())
JOB_RUN_DAO = JobRunDao.JobRunDao(ConnectionUtil.get_connection())

def test_insert():
	t1 = Task.Task(0, "task name", "monthly", 1, 3, 6, 3, "eicho hello")
	TASK_DAO.insert(t1)
	t2 = Task.Task(0, "task name", "monthly", 1, 3, 6, 3, "echo bye")
	TASK_DAO.insert(t2)

def test_select_all():
	res = TASK_DAO.select_all()
	for task in res:
		print task.to_string()

def main():
	JOB_RUN_DAO.truncate()
	TASK_DAO.truncate()
	test_insert()
	test_select_all()

if __name__ == '__main__':
	main()
