from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from jobscheduler.lights import pauseLight, resumeLight, setWeekdayLightOn, setWeekdayLightOff, setWeekendLightOn, setWeekendLightOff
from jobscheduler.thermostat import pauseThermostat, resumeThermostat, setWeekdayThermostatOn, setWeekdayThermostatOff, setWeekendThermostatOn, setWeekendThermostatOff
from firebase.firebase import getLights, getLight, insertLight, getTemps, insertTemp, insertLightDuration, setLight, setTemp, getTemp


@api_view(['GET'])
def api_overview(request):
    data = {
        "get Lights": "getLights/<str:room>/",
        "get Light": "getLight/<str:room>/",
        "set Light": "setLight/<str:room>/<str:on/off>/",
        "insert Light": "insertLight/",
        "set time of light to turn on on weekdays": "weekdayLightOn/<str:room>/<str:24hTime>/",
        "set time of light to turn off on weekdays": "weekdayLightOff/<str:room>/<str:24hTime>/",
        "set time of light to turn on on weekends": "weekendLightOn/<str:room>/<str:24hTime>/",
        "set time of light to turn off on weekends": "weekendLightOff/<str:room>/<str:24hTime>/",
        "pause automated lights": "pauseLight/<str:room>/",
        "resume automated lights": "resumeLight/<str:room>/",
        "get Temperatures": "getTemps/",
        "get Temperature": "getTemp/",
        "set Temperatures": "setTemp/<str:temp>/",
        "insert Temperatures": "insertTemp/",
        "set time of thermo to go to temp on weekdays": "weekdayThermostatOn/<str:temp>/<str:24hTime>/",
        "set time of thermo to go back to temp on weekdays": "weekdayThermostatOff/<str:temp>/<str:24hTime>/",
        "set time of thermo to go to temp on weekends": "weekendThermostatOn/<str:temp>/<str:24hTime>/",
        "set time of thermo to go back to temp on weekends": "weekendThermostatOff/<str:temp>/<str:24hTime>/",
        "pause automated thermostat": "pauseThermostat/",
        "resume automated thermostat": "resumeThermostat/",

    }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_lights(request, room):
    try:
        entries = getLights(room)
        return Response(data=entries, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_light(request, room):
    try:
        entry = getLight(room)
        return Response(data=entry, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def set_light(request, room, cmd):
    try:
        lastOn = getLight(room)

        res = setLight(room, cmd)
        entry = insertLight(res)

        if cmd == 'off':
            entry = insertLightDuration(room, lastOn)

        return Response(data=entry, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def insert_light(request):
    try:
        print(request.data)
        entry = insertLight(request.data)
        return Response(data=entry, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekday_schedule_light_on(request, room, time):
    try:
        print(room, time)
        res = setWeekdayLightOn(room, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekend_schedule_light_on(request, room, time):
    try:
        print(room, time)
        res = setWeekendLightOn(room, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekday_schedule_light_off(request, room, time):
    try:
        print(room, time)
        res = setWeekdayLightOff(room, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekend_schedule_light_off(request, room, time):
    try:
        print(room, time)
        res = setWeekendLightOff(room, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def pause_schedule_light(request, room):
    try:
        print(room)
        res = pauseLight(room)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def resume_schedule_light(request, room):
    try:
        print(room)
        res = resumeLight(room)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

###### THERMOSTAT ######


@api_view(['GET'])
def get_temps(request):
    try:
        entries = getTemps()
        return Response(data=entries, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_temp(request):
    try:
        lastest_entry = getTemp()
        return Response(data=lastest_entry, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def set_temp(request, temp):
    try:
        res = setTemp(temp)
        print(res)
        entry = insertTemp(res)
        return Response(data=entry, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def insert_temp(request):
    try:
        data = {
            u'temp': request.data['temp'],
            u'time': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        entry = insertTemp(data)

        return Response(data=entry, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekday_schedule_thermostat_on(request, temp, time):
    try:
        print(temp, time)
        res = setWeekdayThermostatOn(temp, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekend_schedule_thermostat_on(request, temp, time):
    try:
        print(temp, time)
        res = setWeekendThermostatOn(temp, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekday_schedule_thermostat_off(request, temp, time):
    try:
        print(temp, time)
        res = setWeekdayThermostatOff(temp, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekend_schedule_thermostat_off(request, temp, time):
    try:
        print(temp, time)
        res = setWeekendThermostatOff(temp, time)
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def pause_schedule_thermostat(request):
    try:
        res = pauseThermostat()
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def resume_schedule_thermostat(request):
    try:
        res = resumeThermostat()
        return Response(data=res, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
