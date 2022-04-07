from firebase_admin import auth
from firebase.firebase import getDietPrevWeek, getTransportationPrevWeek, getHousehold, insertRecommendation
from jobscheduler.constants import diet, badDiet, meat, veggie


def executeRecommendations():
    # executing empty sample job
    for user in auth.list_users().iterate_all():
        print(user.uid)
        thresholdDiet(user.uid)
        thresholdTransport(user.uid)
        thresholdHousehold(user.uid)


def thresholdDiet(userId):
    report = ''
    # get week of data
    data = getDietPrevWeek(userId)

    # get total carbon
    weeklyTotal = sum([d['total'] for d in data])

    if weeklyTotal > 43534:
        report += 'DIET: Your weekly total is ' + str(weeklyTotal/1000) + \
            'kg, which is above what the avg Canadian is supposed to produce. You can refer to our suggestions for further tips!.\n'
    else:
        report = 'DIET: Congrats on producing less CO2 than the avg Canadian! The avg Canadian produces 43.53kg a week and you produced ' + \
            str(weeklyTotal/1000) + 'kg.'
        return insertRecommendation(userId, 'diet', report)

    meat_carbon, veggie_carbon, bad_carbon = 0, 0, 0
    for d in data:
        for m in meat:
            if m in d:
                meat_carbon += d[m] * diet[m]
        for v in veggie:
            if v in d:
                veggie_carbon += d[v] * diet[v]
        for b in badDiet:
            if b in d:
                bad_carbon += d[b] * diet[b]

    if (meat_carbon/weeklyTotal) * 100 > 25:
        report += 'Canada\'s Food Guide recommends that 25\% of your plate consist of meat. \nWe noticed that over 25\% of your diet consist of meat: ' + \
            str(int((meat_carbon/weeklyTotal) * 100)) + \
            '\%. If you care to reduce your carbon emissions, we highly consider reducing how much meat you consume.\n'
    if (veggie_carbon/weeklyTotal) * 100 < 50:
        report += 'Canada\'s Food Guide recommends that 50\% of your plate consist of fruits, veggies, and legumes.\nWe noticed that your veggie intake is les than 50\%: ' + \
            str(int((veggie_carbon/weeklyTotal) * 100)) + \
            '\%. If you care to reduce your carbon emissions, we highly consider increasing how much fruits and veggies you consume. You can also sub out meat protein for plant protein.\n'

    report += 'Finally, ' + str(int((bad_carbon/weeklyTotal) * 100)) + \
        '\% of what you ate this week came from our "top 7 worst foods for the environment" list: Beef, Lamb, Shellfish, Chocolate, Dairy, Fish.\n'

    return insertRecommendation(userId, 'diet', report)


def thresholdHousehold(userId):
    report = ''

    data = getHousehold()

    dailyTotalCarbon = sum([d['carbon'] for d in data])
    dailyDurationRoom1 = sum(
        [d['duration'] if d['room'] == 'room1' else 0 for d in data])
    dailyDurationRoom2 = sum(
        [d['duration'] if d['room'] == 'room2' else 0 for d in data])
    dailyDurationRoom3 = sum(
        [d['duration'] if d['room'] == 'room3' else 0 for d in data])
    dailyDurationRoom4 = sum(
        [d['duration'] if d['room'] == 'room4' else 0 for d in data])
    dailyDuration = sum([d['duration'] for d in data])

    if dailyTotalCarbon > 8493.15:
        report += 'HOUSEHOLD: Your daily total is ' + str(int(dailyTotalCarbon/1000)) + \
            'kg which is above what the avg Canadian is supposed to produce. here are our suggestions for further tips!.\n'
    else:
        report = 'HOUSEHOLD: Congrats on producing less CO2 than the avg Canadian! The avg Canadian produces 8.49kg a week and you produced ' + \
            str(dailyTotalCarbon/1000) + 'kg.'
        return insertRecommendation(userId, 'household', report)

    if dailyDuration/60 > 5:
        report += 'We noticed you have your lights running for ' + \
            str(round(dailyDuration/3600, 1)) + \
            'h today. Let\'s see if there is a light you can turn off!\n'

        lights = [(dailyDurationRoom1/dailyDuration, 'room1'), (dailyDurationRoom2/dailyDuration, 'room2'),
                  (dailyDurationRoom3/dailyDuration, 'room3'), (dailyDurationRoom4/dailyDuration, 'room4')]

        lights.sort(key=lambda x: x[0])
        print(lights)
        report += 'We noticed you use' + lights[0][1] + ' the least, is there anyway to minimize this more? We also noticed you use ' + \
            lights[-1][1] + ' the most. Could this be cut down or put on to our scheduler to ensure it gets used only when needed.\n\n'
        report += 'Other recommendations we have are to switch to LEDs if you already have not.\nUse energy efficient appliances. \nTurn off lights that are not used or automate them.'

    return insertRecommendation(userId, 'household', report)


def thresholdTransport(userId):
    report = ''
    # get week of data
    data = getTransportationPrevWeek(userId)

    # get total carbon
    weeklyTotal = sum([d['total'] for d in data])

    if weeklyTotal > 95890:
        report += 'TRANSPORTATION: Your weekly total is ' + str(int(weeklyTotal/1000)) + \
            'kg which is above what the avg Canadian is supposed to produce. here are our suggestions for further tips!.\n'
    else:
        report = 'TRANSPORTATION: Congrats on producing less CO2 than the avg Canadian! The avg Canadian produces 95.89kg a week and you produced ' + \
            str(round(weeklyTotal/1000, 1)) + 'kg.'
        return insertRecommendation(userId, 'transport', report)

    report += 'We recommend trying to achieve a short commute to work (<55km)! We also recommend reducing the number of leisure trips since this drives up your CO2 emissions significantly.'

    return insertRecommendation(userId, 'transport', report)
