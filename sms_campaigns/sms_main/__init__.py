from apscheduler.scheduler import Scheduler
from sms_main.views import checkToSendMessages

# Start the scheduler
sched = Scheduler()
sched.start()

# Schedules checkToSendMessages to be run every 5 seconds
sched.add_cron_job(checkToSendMessages, second='*/5')