from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from jobscheduler.lights import pauseLight, resumeLight, setWeekdayLightOn, setWeekdayLightOff, setWeekendLightOn, setWeekendLightOff
from firebase.firebase import getLights, getLight, insertLight, getTemps, insertTemp, insertLightDuration
from capstoneApi.external import thermostat, lights


@api_view(['GET'])
def api_overview(request):
    data = {
        "all_entries": "getLights/",
        "single_entry": "getLight/<str:pk>/",
        "create_entry": "insertLight/",
        # "update_entry": "updateLight/<str:pk>/",
        # "delete_entry": "deleteLight/<str:pk>/",
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

        res = requests.get(lights[room]+lights['setLight']+cmd).json()
        entry = insertLight(res)
        # light = {
        #     'name': res['name'],
        #     'status': res['status'],
        #     'time': time.strftime("%Y-%m-%dT%H:%M:%SZ")
        # }

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
        setWeekdayLightOn(room, time)
        return Response(data="successfully updated", status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekend_schedule_light_on(request, room, time):
    try:
        print(room, time)
        setWeekendLightOn(room, time)
        return Response(data="successfully updated", status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekday_schedule_light_off(request, room, time):
    try:
        print(room, time)
        setWeekdayLightOff(room, time)
        return Response(data="successfully updated", status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def set_weekend_schedule_light_off(request, room, time):
    try:
        print(room, time)
        setWeekendLightOff(room, time)
        return Response(data="successfully updated", status=status.HTTP_201_CREATED)
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
        print(request.data)
        entry = insertLight(request.data)
        return Response(data=entry, status=status.HTTP_201_CREATED)
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
def set_temp(request, temp):
    try:
        res = requests.get(thermostat['base']+thermostat['setTemp']+temp)
        return Response(data=res, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def insert_temp(request):
    time = datetime.now()
    try:
        temp = {
            u'temp': request.data['temp'],
            u'time': time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        # entry = insertTemp(temp)

        return Response(data=temp, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['PUT'])
# def update_light(request, pk):
#     try:
#         entry = Moisture.objects.get(id=pk)
#         serializer = MoistureSerializer(instance=entry, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view(['DELETE'])
# def delete_light(request, pk):
#     try:
#         entry = Moisture.objects.get(id=pk)
#         entry.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)
