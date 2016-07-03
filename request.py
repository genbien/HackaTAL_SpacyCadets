from recastai import Client
from textblob import TextBlob
import random
import http.client
import json
import os
from country_table import countryTable

RECAST_API_TOKEN = os.environ['RECAST_API_TOKEN']
FBDATA_API_TOKEN = os.environ['FBDATA_API_TOKEN']

client = Client(RECAST_API_TOKEN, 'en')

connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': FBDATA_API_TOKEN, 'X-Response-Control': 'minified' }
connection.request('GET', '/v1/competitions/424/leagueTable', None, headers )
response = json.loads(connection.getresponse().read().decode())


def get_intent(sent):
    return question.intent()

def good_team(country, competence):
    if competence == 1:
        ith = 'st'
    else:
        ith = 'nd'
    resp = []
    resp.append(random.choice(("Yes", "Yeah", "Omg", "No yeah", "Whoa")))
    resp.append("the "+country.value.capitalize()+" team is really good!")
    resp.append("They're ranked "+str(competence)+ith+" in their group!")
    return " ".join(resp)

def bad_team(country, competence):
    if competence == 3:
        ith = 'rd'
    else:
        ith = 'th'
    resp = []
    resp.append(random.choice(("Well...", "Um,", "I guess", "Yeah, no", "Meh,")))
    resp.append("the "+country.value.capitalize()+" team is okay.")
    resp.append("They're ranked "+str(competence)+ith+" in their group.")
    return " ".join(resp)


def check_competence(country):
    questionCountry = country.value.lower()

    for listCountry in countryTable:
        if (questionCountry in listCountry):
            index = countryTable.index(listCountry)
            nameCountry = countryTable[index][-1]
            groupDic = response['standings']
            for keyGroup in groupDic.keys() :
                for infoCountry in groupDic[keyGroup]:
                    if (infoCountry['team'].lower()==nameCountry):
                        rank = infoCountry['rank']

    return rank

def response_team_info(country):
    questionCountry = country.value.lower()
    for listCountry in countryTable:
        if (questionCountry in listCountry):
            index = countryTable.index(listCountry)
            nameCountry = countryTable[index][-1]
            groupDic = response['standings']
            for keyGroup in groupDic.keys() :
                for infoCountry in groupDic[keyGroup]:
                    if infoCountry['team'].lower() == nameCountry:
                        print("- The " + questionCountry + " team has played " + (str)(infoCountry['playedGames']) + " games.")


def response_match_result(country):
    questionCountry = country.value.lower()
    for listCountry in countryTable:
        if (questionCountry in listCountry):
            index = countryTable.index(listCountry)
            nameCountry = countryTable[index][-1]
            groupDic = response['standings']
            for keyGroup in groupDic.keys() :
                for infoCountry in groupDic[keyGroup]:
                    if infoCountry['team'].lower() == nameCountry:
                        print("- The " + questionCountry + " team has made " + (str)(infoCountry['goals']) + " goals, scored " +
                        (str)(infoCountry['points']) + " points, and its rank is " + (str)(infoCountry['rank']) + "/4 in group phase." )



# question = client.text_request("Is the German team good?")
# question = client.text_request("Is the team from Portugal bad?")
question = client.text_request("How many goals has the French team made?")

print("Input >>", question.source)

country = question.get('COUNTRY')
intent  = get_intent(question.source)

if intent == 'team_competence':
    competence = check_competence(country)
    if competence < 3:
        print(good_team(country, competence))
    else:
        print(bad_team(country, competence))
elif intent == 'match_result':
    response_match_result(country)
elif intent == 'team_info':
    response_team_info(country)

