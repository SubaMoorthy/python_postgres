import sched, time

s = sched.scheduler(time.time, time.sleep)
def print_time(msg): print "From print_time", msg, time.time()

def periodic(scheduler, interval, action, actionargs=()):
	scheduler.enter(interval, 1, periodic, (scheduler, interval, action, actionargs))
	action(actionargs)

def print_some_times():
	print time.time()
	periodic(s, 10, print_time, "main")
	periodic(s, 5, print_time, "second")
	s.run()
	print time.time()

def main():
	print_some_times()

if __name__ == "__main__":
	main()
