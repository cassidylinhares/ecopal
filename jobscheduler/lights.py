import requests
from apscheduler.triggers.cron import CronTrigger
from firebase.firebase import insertLight
from capstoneApi.external import lights
from jobscheduler.scheduler import scheduler

'''
room: select [room1, room2, room3, room4]
time: 22:00 (24h format)
'''

###### WEEKDAYS ######


def setWeekdayLightOn(room, time):
    h, m = time.split(':')[0], time.split(':')[1]

    # check if job already exist
    jobId = 'weekday_light_on_' + room
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    lightOnTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='0-5', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: lightOn(room), lightOnTrigger, id=jobId)
    return 0


def setWeekdayLightOff(room, time):
    h, m = time.split(':')[0], time.split(':')[1]

    # check if job already exist
    jobId = 'weekday_light_off_' + room
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    lightOffTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='0-5', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: lightOff(room), lightOffTrigger, id=jobId)

    return 0

###### WEEKENDS ######


def setWeekendLightOn(room, time):
    h, m = time.split(':')[0], time.split(':')[1]

    # check if job already exist
    jobId = 'weekend_light_on_' + room
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    lightOnTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='5-7', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: lightOn(room), lightOnTrigger, id=jobId)

    return lightOnTrigger


def setWeekendLightOff(room, time):
    h, m = time.split(':')[0], time.split(':')[1]

    # check if job already exist
    jobId = 'weekend_light_off_' + room
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    lightOffTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='5-7', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: lightOff(room), lightOffTrigger, id=jobId)

    return lightOffTrigger

###### SCHEDULING ######


def pauseLight(room):
    jobWeekdayOff = 'weekday_light_off_' + room
    jobWeekdayOn = 'weekday_light_on_' + room
    jobWeekendOff = 'weekend_light_off_' + room
    jobWeekendOn = 'weekend_light_on_' + room

    scheduler.pause_job(job_id=jobWeekdayOff)
    scheduler.pause_job(job_id=jobWeekdayOn)
    scheduler.pause_job(job_id=jobWeekendOff)
    scheduler.pause_job(job_id=jobWeekendOn)
    return 'paused ' + room


def resumeLight(room):
    jobWeekdayOff = 'weekday_light_off_' + room
    jobWeekdayOn = 'weekday_light_on_' + room
    jobWeekendOff = 'weekend_light_off_' + room
    jobWeekendOn = 'weekend_light_on_' + room

    scheduler.resume_job(job_id=jobWeekdayOff)
    scheduler.resume_job(job_id=jobWeekdayOn)
    scheduler.resume_job(job_id=jobWeekendOff)
    scheduler.resume_job(job_id=jobWeekendOn)
    return 'resumed ' + room


def lightOn(room):
    res = requests.get(lights[room]+lights['setLight']+'on').json()
    insertLight(res)


def lightOff(room):
    res = requests.get(lights[room]+lights['setLight']+'off').json()
    insertLight(res)
