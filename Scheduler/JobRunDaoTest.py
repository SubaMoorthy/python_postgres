import JobRun
import ConnectionUtil
import JobRunDao

JOB_RUN_DAO = JobRunDao.JobRunDao(ConnectionUtil.get_connection())

def test_insert():
	j1 = JobRun.JobRun(0, 3, "", "", JobRun.STATUS_RUNNING) 
	job_run_id = JOB_RUN_DAO.insert(j1)
	return job_run_id

def test_select():
	job_runs = JOB_RUN_DAO.select_all()
	for job_run in job_runs:
		print(job_run.to_string())

def test_end_job(job_run_id):
	JOB_RUN_DAO.end_job(job_run_id, JobRun.STATUS_SUCCESS)

def main():
	JOB_RUN_DAO.truncate()
	job_run_id = test_insert()
	test_select()
	test_end_job(job_run_id)
	test_select()



if __name__ == "__main__":
	main()
