from firebase_admin import initialize_app, credentials, firestore
from datetime import datetime, timedelta, date
import random

# Use a service account
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "ecohub-707c9",
    "private_key_id": "710ec24c6babe84ec9ec1bcc5a6a3f8bbedb1330",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDZAYxtDxo0f+OM\nSDU+7IJK+LBgCxgPeCERjFsVtq0hqNjHc9Gtu/ozgjevq1bCyEPd11Rss4RjVoG8\nduPQ+zCkc/CtEAwGS5fddfeZu0SAsUBPv6f+M0hs6/9M+Z6s3Ex+fcU7YGqUUxxj\nTEmOhHODNXzBGoq8ZtrXMCCCpZVCSdLmOXZfV8XQoGTAbc+egGCje+Vkbo9phra9\nuvYOzXK2hWVni8HNGKZc0AYF+zACFDTUaKFW/C6ffT8ClrHQ2X3m4dW3XWfVedfl\njmXvV/u5p4VTmxuYrA7IBTphU5NdGpF2WdM/8yEbdQGFClCg+j0tCJS0TTF4aGvd\nwrLPXMK7AgMBAAECggEAI9r2JWTr6wXAhsK9jX6Njq6lkdDzckbii+A5go5y789S\nti3kVMTs88rNwahZRwjI8eQszmMg+jrmZ8nrHXILmPiRKT8wBXBDEPP3a7699FeV\nLTgZHU7C5kBeKA1Mkvo5Z2MHjiaBpa1P0PZfZv1qiqDxUoS8rKGAAjMxA/UxAska\nxFGbzXcA0pvEEgEsxJUn9kwQKMFFrZ8UBPr1HWHjAVniAzTQEWC5nI9YJdIvbRfu\n0Xq16IR5PHC9GvR7eMx32g5fFzZAiNyiK4cZPCTE2mNuNpIxliRKPqN+nL8/i/0d\nEXv59BnKZxAnhJoybP2DfkfCnaaoTIvYNjf7th8rvQKBgQD+GaaAai2L392Ikpuy\nlLNqnG7Oi704AzsZDUwrPxC7zo3bPtR/00Rw31GvnWA/ovv5ynqk5BA0cVdUtH9t\nU+7hNkMYdAX5OLKSHHx/d1JbwNFKtsMZAfKPxv4kbOJREqTXCqw9A6D0HfIyvuZt\n6w3AZI7Xbgx8J1wtJ/sGFz9upQKBgQDaoOZRMxkUXy0EZfaM0fYtukN3HkJJs7Pr\nCs1g/ylfZGTTLFNFqNCms6Udv4/bbjRsy0SEGO8UgcSeSytLH+Chwqo5u4ytpjgZ\nm5nwIeWFIqnXCRBqITrsVcCj+W8cykXaarUtXGWAn/kGMep1zW++kefHwu48mWYQ\nZS6fWPkN3wKBgFbIjexH1zxxfej6IYERdmGQAew7H6n0uIdq2jve8ykhd6OMxujN\nUA+4xd5Twp6ZXLPIarDMT5iJqUj9yJOfWfPDI5FDdxLSQXLTldW2/ALoTNLWrrVo\ny949GWl5YqZL1s63D3JbPeqCG8knF+4snGq8LWj4Zf01OC8X+4zt/bUdAoGAM6yI\nA3UyXlBIkZuP9KTDrPczbvol7MmeotVAycZFfxh5hDgbzoEiH+SiCC/4zoJzvasl\nnJtQFua9FDTsHKuCKnmaRl7/1yNMazEN52X7m8YfooWv7YXBKY7zI06XZpSggglq\nnTgTfZ1R/JbbtdBCsyZFRD/ck1Imf4WKyXr8Er0CgYBEGJtWZmNfaS+OlpeNyJ+a\n6Dfi1/5xZuKMu9exRenv9hCY85RzCBfHq9NV3rckV36LTmisr3CHt9hqcOfsVf9e\n4jUb2u6mMaGvl5fwKT07OzNoQtIfJgIFOSPjKu7j1d0oqEEmMh1ALTYbSM/+zz+b\n7pwyT6bwRzDcXFphp6EqlA==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ctcaz@ecohub-707c9.iam.gserviceaccount.com",
    "client_id": "107332052420228923058",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ctcaz%40ecohub-707c9.iam.gserviceaccount.com"

})
initialize_app(cred)

####### LIGHTS ######


def getLights(room):
    db = firestore.client()
    col_ref = db.collection(u'lights').document(room).collection(u'history')
    docs = col_ref.stream()

    lights = []
    for doc in docs:
        vals = {}
        vals[doc.id] = doc.to_dict()
        lights.append(vals)

    return lights


def getLight(room):
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


def insertLightDuration(room, lastOn):
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
    db = firestore.client()
    col_ref = db.collection(u'thermostat')
    docs = col_ref.stream()

    temps = []
    for doc in docs:
        vals = {}
        vals[doc.id] = doc.to_dict()
        temps.append(vals)

    return temps


def getTemp(timestamp):
    db = firestore.client()
    doc_ref = db.collection(u'thermostat').document(timestamp)
    doc = doc_ref.get()

    temp = {}
    temp[timestamp] = doc.to_dict()

    return temp


def insertTemp(data):
    db = firestore.client()
    doc_ref = db.collection(u'thermostat').document(data['time'])
    doc_ref.set({
        u'temp': data['temp'],
        u'time': datetime.fromisoformat(data['time'][:-1])
    })

    doc = doc_ref.get()

    temp = {}
    temp[data['time']] = doc.to_dict()

    return temp

###### DIET ########


def getDiet(userId, datestamp):
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


def getDietPrevDay(userId):
    yesterday = date.today() - timedelta(days=1)

    return getDiet(userId, yesterday.strftime("%Y-%m-%d"))


def getDietPrevWeek(userId):
    diet = []

    # get previous 6 days
    for i in range(6, 0, -1):
        day = date.today() - timedelta(days=i)
        diet.append(getDiet(userId, day.strftime("%Y-%m-%d")))

    # get todays date
    diet.append(getDiet(userId, date.today().strftime("%Y-%m-%d")))

    return diet


def getDietPrevMonth(userId):
    diet = []

    for i in range(30, 0, -1):
        day = date.today() - timedelta(days=i)
        diet.append(getDiet(userId, day.strftime("%Y-%m-%d")))

    # get todays date
    diet.append(getDiet(userId, date.today().strftime("%Y-%m-%d")))
    return diet

###### Transportation #######


def getTransportation(userId, datestamp):
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


def getTransportationPrevDay(userId):
    yesterday = date.today() - timedelta(days=1)

    return getTransportation(userId, yesterday.strftime("%Y-%m-%d"))


def getTransportationPrevWeek(userId):
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


def getTransportationPrevMonth(userId):
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


def insertRecommendation(userId, category, data):
    # today = date.today().strftime("%d-%m-%Y")

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


# print(insertRecommendation('Test', 'ss', 'hey now youre rockstar'))


def getSuggestion(category):  # get suggestion for provided data
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
