from jobscheduler.recommendations import executeRecommendations
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from time import sleep


scheduler = BackgroundScheduler()


def start():
    scheduler.start()
    cronTrigger = CronTrigger(year='*', month='*', day='*',
                              hour='20', minute='0', second='0')  # will run at 8pm each day
    scheduler.add_job(executeRecommendations,
                      cronTrigger, id='recommendations')

    sleep(5)
