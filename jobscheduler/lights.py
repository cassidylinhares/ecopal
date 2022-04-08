from apscheduler.triggers.cron import CronTrigger
from firebase.firebase import insertLight, setLight, insertScheduler
from jobscheduler.scheduler import scheduler

'''
room: select [room1, room2, room3, room4]
time: 22:00 (24h format)
'''

###### WEEKDAYS ######


def setWeekdayLightOn(room: str, time: str):
    h, m = time.split(':')[0], time.split(':')[1]
    h = (h+4) % 24  # convert to UTC
    if h == '0':
        h = '00'

    # check if job already exist
    jobId = 'weekday_light_on_' + room
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    lightOnTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='mon,tue,wed,thu,fri', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: lightOn(room), lightOnTrigger, id=jobId)

    # update db to reflect the new changes
    insertScheduler(room, 'weekdayOn', time)
    res = insertScheduler(room, 'paused', False)
    return res


def setWeekdayLightOff(room: str, time: str):
    h, m = time.split(':')[0], time.split(':')[1]
    h = (h+4) % 24  # convert to UTC
    if h == '0':
        h = '00'

    # check if job already exist
    jobId = 'weekday_light_off_' + room
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    lightOffTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='mon,tue,wed,thu,fri', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: lightOff(room), lightOffTrigger, id=jobId)

    # update db to reflect the new changes
    insertScheduler(room, 'weekdayOff', time)
    res = insertScheduler(room, 'paused', False)
    return res

###### WEEKENDS ######


def setWeekendLightOn(room: str, time: str):
    h, m = time.split(':')[0], time.split(':')[1]
    h = (h+4) % 24  # convert to UTC
    if h == '0':
        h = '00'

    # check if job already exist
    jobId = 'weekend_light_on_' + room
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    lightOnTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='sat,sun', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: lightOn(room), lightOnTrigger, id=jobId)

    # update db to reflect the new changes
    insertScheduler(room, 'weekendOn', time)
    res = insertScheduler(room, 'paused', False)
    return res


def setWeekendLightOff(room: str, time: str):
    h, m = time.split(':')[0], time.split(':')[1]
    h = (h+4) % 24  # convert to UTC
    if h == '0':
        h = '00'

    # check if job already exist
    jobId = 'weekend_light_off_' + room
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    lightOffTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='sat,sun', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: lightOff(room), lightOffTrigger, id=jobId)

    # update db to reflect the new changes
    insertScheduler(room, 'weekendOff', time)
    res = insertScheduler(room, 'paused', False)
    return res

###### SCHEDULING ######


def pauseLight(room: str):
    jobWeekdayOff = 'weekday_light_off_' + room
    jobWeekdayOn = 'weekday_light_on_' + room
    jobWeekendOff = 'weekend_light_off_' + room
    jobWeekendOn = 'weekend_light_on_' + room

    if scheduler.get_job(job_id=jobWeekdayOff) is not None:
        scheduler.pause_job(job_id=jobWeekdayOff)
    if scheduler.get_job(job_id=jobWeekdayOn) is not None:
        scheduler.pause_job(job_id=jobWeekdayOn)
    if scheduler.get_job(job_id=jobWeekendOff) is not None:
        scheduler.pause_job(job_id=jobWeekendOff)
    if scheduler.get_job(job_id=jobWeekendOn) is not None:
        scheduler.pause_job(job_id=jobWeekendOn)

    # update db to reflect the new changes
    res = insertScheduler(room, 'paused', True)
    return res


def resumeLight(room: str):
    jobWeekdayOff = 'weekday_light_off_' + room
    jobWeekdayOn = 'weekday_light_on_' + room
    jobWeekendOff = 'weekend_light_off_' + room
    jobWeekendOn = 'weekend_light_on_' + room

    if scheduler.get_job(job_id=jobWeekdayOff) is not None:
        scheduler.resume_job(job_id=jobWeekdayOff)
    if scheduler.get_job(job_id=jobWeekdayOn) is not None:
        scheduler.resume_job(job_id=jobWeekdayOn)
    if scheduler.get_job(job_id=jobWeekendOff) is not None:
        scheduler.resume_job(job_id=jobWeekendOff)
    if scheduler.get_job(job_id=jobWeekendOn) is not None:
        scheduler.resume_job(job_id=jobWeekendOn)

    # update db to reflect the new changes
    res = insertScheduler(room, 'paused', False)
    return res

###### HELPERS ######


def lightOn(room: str):
    res = setLight(room, 'on')
    insertLight(res)


def lightOff(room: str):
    res = setLight(room, 'off')
    insertLight(res)
