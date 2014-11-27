FREQ_DAILY = "DAILY"
FREQ_MONTHLY = "MONTHLY"
FREQ_HOURLY = "HOURLY"
FREQ_WEEKLY = "WEEKLY"

class Task:
	def __init__(self, task_id, name, frequency, month, day_of_week, day_of_month, hour, command):
		self.name = name
		self.frequency = frequency
		self.month = month
		self.day_of_month = day_of_month
		self.day_of_week = day_of_week
		self.hour = hour
		self.command = command
		self.task_id = task_id
	def to_string(self):
		return_string = ""
		return_string += "task_id = " + str(self.task_id)+ "\n"
		return_string += "name = " + self.name + "\n"
		return_string += "frequency = " + self.frequency + "\n"
		return_string += "month = " + str(self.month) + "\n"
		return_string += "day of month = " + str(self.day_of_month) + "\n"
		return_string += "day of week = " + str(self.day_of_week) + "\n"
		return_string += "hour = " + str(self.hour) + "\n"
		return_string += "command = " + self.command + "\n"
		return return_string
