import os
from firebase_admin import initialize_app, credentials, firestore, db
from datetime import datetime, timedelta, date
import random


# Use a service account
cred = credentials.Certificate({
    'type': os.environ.get("TYPE"),
    'project_id': os.environ.get("PROJECT_ID"),
    'private_key_id': os.environ.get("PRIVATE_KEY_ID"),
    'private_key': os.environ.get("PRIVATE_KEY").replace('\\n', '\n'),
    'client_email': os.environ.get("CLIENT_EMAIL"),
    'client_id': os.environ.get("CLIENT_ID"),
    'auth_uri': os.environ.get("AUTH_URI"),
    'token_uri': os.environ.get("TOKEN_URI"),
    'auth_provider_x509_cert_url': os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
    'client_x509_cert_url': os.environ.get("CLIENT_X509_CERT_URL")
})
initialize_app(
    cred, {'databaseURL': 'https://ecohub-707c9-default-rtdb.firebaseio.com'})

####### LIGHTS ######


def setLight(room: str, cmd: str):
    ref = db.reference(room)
    ref.set(cmd)
    return {
        'status': ref.get(),
        'name': room
    }


def getLights(room: str):
    db = firestore.client()
    col_ref = db.collection(u'lights').document(room).collection(u'history')
    docs = col_ref.stream()

    lights = []
    for doc in docs:
        vals = {}
        vals[doc.id] = doc.to_dict()
        lights.append(vals)

    return lights


def getLight(room: str):
    db = firestore.client()
    doc_ref = db.collection(u'lights').document(room)
    doc = doc_ref.get()

    data = doc.to_dict()
    data['room'] = room
    return data


def insertLight(data):
    light_data = {
        'name': data['name'],
        'status': data['status'],
        'time':  datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    db = firestore.client()
    history_ref = db.collection(u'lights').document(
        light_data['name']).collection(u'history').document(light_data['time'])
    doc_ref = db.collection(u'lights').document(light_data['name'])

    doc_ref.set({
        u'status': light_data['status'],
        u'time': datetime.fromisoformat(light_data['time'][:-1])
    })

    history_ref.set({
        u'status': light_data['status'],
        u'time': datetime.fromisoformat(light_data['time'][:-1])
    })

    doc = doc_ref.get()
    history_ref.get()

    return doc.to_dict()


def insertLightDuration(room: str, lastOn):
    on_data = {
        'time': lastOn['time'].strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    off_data = {
        'time': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    # get difference
    difference = datetime.strptime(
        off_data['time'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(on_data['time'], "%Y-%m-%dT%H:%M:%SZ")

    duration_seconds = difference.total_seconds()
    print(datetime.strptime(on_data['time'], "%Y-%m-%dT%H:%M:%SZ"))
    # get time in number of minutes, seconds
    minutes = duration_seconds/60

    # insert info into db
    db = firestore.client()
    duration_ref = db.collection(u'lights').document(
        room).collection(u'duration').document(off_data['time'])

    duration_ref.set({
        u'room': room,
        u'duration': minutes,
        u'timeOn': datetime.fromisoformat(on_data['time'][:-1]),
        u'timeOff': datetime.fromisoformat(off_data['time'][:-1]),
        # 0.3892 is g of CO2 per min for LED light bulb
        u'carbon': 0.3892 * minutes,
        u'id': date.today().strftime("%Y-%m-%d")
    })

    doc = duration_ref.get()

    light = {}
    light[off_data['time']] = doc.to_dict()

    return light

###### THERMOSTAT ######


def getTemps():
    database = firestore.client()
    doc_ref = database.collection(u'thermostat').document(u'history')
    doc = doc_ref.get()

    return doc.to_dict()


def getTemp():
    database = firestore.client()
    doc_ref = database.collection(u'thermostat').document(u'current')
    doc = doc_ref.get()

    return doc.to_dict()


def setTemp(temp: str):
    ref = db.reference('thermostat')
    ref.set(str(temp))
    return {
        'temp': ref.get(),
        'time': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    }


def insertTemp(data):
    database = firestore.client()
    cur_ref = database.collection(u'thermostat').document(u'current')
    history_ref = database.collection(u'thermostat').document(u'history')

    cur_ref.set(data)

    history_doc = history_ref.get()

    if history_doc.to_dict() == {}:
        history_ref.set({
            u'0': data,
            u'counter': 1,
        })
    else:
        d = history_doc.to_dict()
        history_ref.update({
            str(d['counter']): data,
            u'counter': firestore.Increment(1)
        })

    doc = cur_ref.get()

    return doc.to_dict()

###### SCHEDULER ######
# device: room# or thermostat;
# type: weekdayOn weekdayOff weekendOn weekendOff paused
# value: <string: 24h time> or boolean


def insertScheduler(device: str, type: str, value):
    database = firestore.client()
    doc_ref = database.collection(u'scheduler').document(device)

    doc_ref.update({
        type: value,
    })
    doc = doc_ref.get()

    return doc.to_dict()

###### DIET ########


def getDiet(userId: str, datestamp: str):
    db = firestore.client()
    doc_ref = db.collection(u'userInfo').document(
        userId).collection(u'dietTotals').document(datestamp)

    doc = doc_ref.get()

    diet = {}
    if doc.exists:
        diet = doc.to_dict()
        diet['date'] = datestamp

    if 'total' not in diet:
        diet['total'] = 0

    return diet


def getDietPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getDiet(userId, yesterday.strftime("%Y-%m-%d"))


def getDietPrevWeek(userId: str):
    diet = []

    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        diet.append(getDiet(userId, day.strftime("%Y-%m-%d")))

    # get todays date
    diet.append(getDiet(userId, date.today().strftime("%Y-%m-%d")))

    return diet


def getDietPrevMonth(userId: str):
    diet = []

    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        diet.append(getDiet(userId, day.strftime("%Y-%m-%d")))

    # get todays date
    diet.append(getDiet(userId, date.today().strftime("%Y-%m-%d")))
    return diet

###### Transportation #######


def getTransportation(userId: str, datestamp: str):
    db = firestore.client()
    doc_ref = db.collection(u'userInfo').document(
        userId).collection(u'transportTotals').document(datestamp)
    doc = doc_ref.get()

    transportation = {}
    if doc.exists:
        transportation = doc.to_dict()
        transportation['date'] = datestamp

    if 'total' not in transportation:
        transportation['total'] = 0

    return transportation


def getTransportationPrevDay(userId: str):
    yesterday = date.today() - timedelta(days=1)

    return getTransportation(userId, yesterday.strftime("%Y-%m-%d"))


def getTransportationPrevWeek(userId: str):
    transportation = []

    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        transportation.append(getTransportation(
            userId, day.strftime("%Y-%m-%d")))

    # get todays date
    transportation.append(getTransportation(
        userId, date.today().strftime("%Y-%m-%d")))

    return transportation


def getTransportationPrevMonth(userId: str):
    transportation = []

    # get previous 6 days
    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        transportation.append(getTransportation(
            userId, day.strftime("%Y-%m-%d")))

    # get todays date
    transportation.append(getTransportation(
        userId, date.today().strftime("%Y-%m-%d")))

    return transportation

####### HOUSEHOLD #######


def getHousehold():
    day = []
    db = firestore.client()

    # room 1
    room1_ref = db.collection(u'lights').document(
        'room1').collection(u'duration')

    query_room1 = room1_ref.where(
        u'id', u'==', datetime.now().strftime("%Y-%m-%d"))

    docs_room1 = query_room1.stream()
    for doc in docs_room1:
        day.append(doc.to_dict())

    # room 2
    room2_ref = db.collection(u'lights').document(
        'room2').collection(u'duration')
    query_room2 = room2_ref.where(
        u'id', u'==', datetime.now().strftime("%Y-%m-%d"))

    docs_room2 = query_room2.stream()
    for doc in docs_room2:
        day.append(doc.to_dict())

    # room 3
    room3_ref = db.collection(u'lights').document(
        'room3').collection(u'duration')
    query_room3 = room3_ref.where(
        u'id', u'==', datetime.now().strftime("%Y-%m-%d"))

    docs_room3 = query_room3.stream()
    for doc in docs_room3:
        day.append(doc.to_dict())

    # room 4
    room4_ref = db.collection(u'lights').document(
        'room4').collection(u'duration')
    query_room4 = room4_ref.where(
        u'id', u'==', datetime.now().strftime("%Y-%m-%d"))

    docs_room4 = query_room4.stream()
    for doc in docs_room4:
        day.append(doc.to_dict())

    return day

####### RECOMMENDATION #######


def insertRecommendation(userId: str, data):
    db = firestore.client()
    doc_ref = db.collection(u'recommendations').document(
        userId)

    doc = doc_ref.get()

    if doc.to_dict() == {}:
        doc_ref.set({
            u'0': data,
            u'counter': 1,
        })
    else:
        d = doc.to_dict()
        doc_ref.update({
            str(d['counter']): data,
            u'counter': firestore.Increment(1)
        })

    doc = doc_ref.get()

    return doc.to_dict()


def getSuggestion(category: str):  # get suggestion for provided data
    if category == '' or category is None:
        return ''

    db = firestore.client()

    suggestions = {}
    recommendation = ''

    doc_ref = db.collection(u'suggestions').document(
        category)
    doc = doc_ref.get()

    suggestions = doc.to_dict()
    recommendation = random.choice(suggestions['suggestions'])

    return recommendation
