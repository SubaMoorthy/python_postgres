import Task
import ConnectionUtil
import TaskDao
import JobRunDao

TASK_DAO = TaskDao.TaskDao(ConnectionUtil.get_connection("config.cfg"))
JOB_RUN_DAO = JobRunDao.JobRunDao(ConnectionUtil.get_connection("config.cfg"))

def test_insert():
	t1 = Task.Task(0, "task name", "monthly", 1, 3, 6, 3, "eicho hello", "my_folder2")
	TASK_DAO.insert(t1)
	t2 = Task.Task(0, "task name", "monthly", 1, 3, 6, 3, "echo bye", "my_folder1")
	TASK_DAO.insert(t2)

def test_select_all():
	res = TASK_DAO.select_all()
	for task in res:
		print task.to_string()

def test_load_by_id():
	t1 = Task.Task(0, "task name", "monthly", 1, 3, 6, 3, "echo hello", "my_folder1")
	inserted_task_id = TASK_DAO.insert(t1)
	res  = TASK_DAO.load_by_id(inserted_task_id)
	for task in res:
		print task.to_string()


def main():
	JOB_RUN_DAO.truncate()
	TASK_DAO.truncate()
	test_insert()
	test_select_all()
	#test_load_by_id()

if __name__ == '__main__':
	main()
