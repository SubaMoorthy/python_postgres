STATUS_FAIL = "FAIL"
STATUS_SUCCESS = "SUCCESSS"
STATUS_RUNNING = "RUNNING"

class JobRun:
	def __init__(self, job_run_id, task_id, start_time, end_time, status):
		self.job_run_id = job_run_id
		self.task_id = task_id
		self.start_time = start_time
		self.end_time = end_time
		self.status = status
	def to_string(self):
		ret_str = ""
		ret_str += "job_run_id: " + str(self.job_run_id) + "\n"
		ret_str += "task_id: " + str(self.task_id) + "\n"
		ret_str += "start_time: " + str(self.start_time) + "\n"
		ret_str += "end_time: " + str(self.end_time) + "\n"
		ret_str += "status: " + self.status + "\n"
		return ret_str
