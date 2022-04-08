from apscheduler.triggers.cron import CronTrigger
from firebase.firebase import insertTemp, setTemp, insertScheduler
from jobscheduler.scheduler import scheduler

###### WEEKDAYS ######


def setWeekdayThermostatOn(temp: str, time: str):
    h, m = time.split(':')[0], time.split(':')[1]

    # check if job already exist
    jobId = 'weekday_thermostat_on'
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    thermostatOnTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='0-6', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: thermostatTemp(
        temp), thermostatOnTrigger, id=jobId)

    # update db to reflect the new changes
    insertScheduler('thermostat', 'weekdayOn', {
        u'time': time, u'temp': temp})
    res = insertScheduler('thermostat', 'paused', False)

    return res


def setWeekdayThermostatOff(temp: str, time: str):
    h, m = time.split(':')[0], time.split(':')[1]

    # check if job already exist
    jobId = 'weekday_thermostat_off'
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    thermostatOffTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='0-6', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: thermostatTemp(
        temp), thermostatOffTrigger, id=jobId)

    # update db to reflect the new changes
    insertScheduler('thermostat', 'weekdayOff', {
        u'time': time, u'temp': temp})
    res = insertScheduler('thermostat', 'paused', False)
    return res

###### WEEKENDS ######


def setWeekendThermostatOn(temp: str, time: str):
    h, m = time.split(':')[0], time.split(':')[1]

    # check if job already exist
    jobId = 'weekend_thermostat_on'
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    thermostatOnTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='5-7', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: thermostatTemp(
        temp), thermostatOnTrigger, id=jobId)

    # update db to reflect the new changes
    insertScheduler('thermostat', 'weekendOn', {
        u'time': time, u'temp': temp})
    res = insertScheduler('thermostat', 'paused', False)
    return res


def setWeekendThermostatOff(temp: str, time: str):
    h, m = time.split(':')[0], time.split(':')[1]

    # check if job already exist
    jobId = 'weekend_thermostat_off'
    job = scheduler.get_job(job_id=jobId)

    # delete if job exist
    if job is not None:
        scheduler.remove_job(job_id=jobId)

    # set schedule
    thermostatOffTrigger = CronTrigger(
        year='*', month='*', day='*', day_of_week='5-7', hour=str(h), minute=str(m), second='0')

    # add job
    scheduler.add_job(lambda: thermostatTemp(
        temp), thermostatOffTrigger, id=jobId)

    # update db to reflect the new changes
    insertScheduler('thermostat', 'weekdendOff', {
        u'time': time, u'temp': temp})
    res = insertScheduler('thermostat', 'paused', False)
    return res

###### SCHEDULING ######


def pauseThermostat():
    jobWeekdayOff = 'weekday_thermostat_off'
    jobWeekdayOn = 'weekday_thermostat_on'
    jobWeekendOff = 'weekend_thermostat_off'
    jobWeekendOn = 'weekend_thermostat_on'

    scheduler.pause_job(job_id=jobWeekdayOff)
    scheduler.pause_job(job_id=jobWeekdayOn)
    scheduler.pause_job(job_id=jobWeekendOff)
    scheduler.pause_job(job_id=jobWeekendOn)

    # update db to reflect the new changes
    res = insertScheduler('thermostat', 'paused', True)
    return res


def resumeThermostat():
    jobWeekdayOff = 'weekday_thermostat_off'
    jobWeekdayOn = 'weekday_thermostat_on'
    jobWeekendOff = 'weekend_thermostat_off'
    jobWeekendOn = 'weekend_thermostat_on'

    scheduler.resume_job(job_id=jobWeekdayOff)
    scheduler.resume_job(job_id=jobWeekdayOn)
    scheduler.resume_job(job_id=jobWeekendOff)
    scheduler.resume_job(job_id=jobWeekendOn)

    # update db to reflect the new changes
    res = insertScheduler('thermostat', 'paused', False)
    return res

###### HELPERS ######


def thermostatTemp(temp: str):
    res = setTemp(temp)
    insertTemp(res)
