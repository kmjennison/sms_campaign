from apscheduler.scheduler import Scheduler
from sms_main.views import *
import logging
logging.basicConfig()

# Start the scheduler
sched = Scheduler()
sched.start()

# Schedules checkToSendMessages to be run every 5 seconds
sched.add_cron_job(checkToSendMessages, second='*/5')