import requests
import json
import image
from collections import namedtuple
from recordtype import recordtype
from bs4 import BeautifulSoup
from PIL import Image
import urllib.request
from pprint import pprint


key = 'RGAPI-48c7411d-8cd9-4eec-8411-f9de3d3cd336'
champion = namedtuple("champion", 'name, id')
item = namedtuple("item", 'name, id, cost')
summoner = namedtuple("summoner", 'name, Summonerid, Accountid, puuid')
champions = []  # This holds the champion name and ids
items = []  # This holds the items information
items_id = []
summoners = []  # This holds the summoners that we are looking up currently.
champ_information = []  # This holds the lore, names, and titles of each champions
champ_pic = []  # This will hold champion splash pics

request = requests.get(r'https://developer.riotgames.com/game-constants.html')
soup = BeautifulSoup(request.content, "html.parser")
#c = soup.find_all('tbody')
maps = []
list_of_maps = []

"""
c = c[2].find_all('td')
print(c)
for i in c:
    maps.append(i.text)
"""

for i in range(14):
    f = (maps[:3])
    del maps[:3]
    list_of_maps.append(f)

patch = '9.15.1'
counter = 0

champ_data = json.load(
    open(r'/Users/kennedy/Desktop/Python_Projects/RIOT_API/updatedchampion.json', encoding='utf8'))
item_data = json.load(
    open(r'/Users/kennedy/Desktop/Python_Projects/RIOT_API/League_items.json', encoding='utf8'))

for x in champ_data['data']:
    champions.append(champion(x, champ_data['data'][x]['key']))
champions.append(champion("No ban", -1))
for id in item_data['data']:
    items_id.append(id)

for itemz, id in zip(item_data['data'], items_id):
    items.append(item(item_data['data'][id]['name'], id, item_data['data'][id]['gold']['total']))
    #print(item_data['data'][id]['name'] + ': ' + item_data['data'][id]['description'])
    counter += 1


def get_summoner_name(summoner_name):
    #summoner_name = input("Which summoner do you want to look up?")
    request = requests.get(
        r'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + "?api_key=" + key)
    player = summoner(request.json()["name"], request.json()['id'],
                      request.json()['accountId'], request.json()['puuid'])
    summoners.append(player)
    return request.json()["name"], request.json()['id'], request.json()['accountId'], request.json()['puuid']


def free_rotation():
    freeChamps = []
    request = requests.get(
        r'https://na1.api.riotgames.com/lol/platform/v3/champion-rotations' + "?api_key=" + key)
    for champ in champions:
        if int(champ.id) in request.json()['freeChampionIds']:
            freeChamps.append(champ.name)
    return freeChamps


def get_rank():
    request = requests.get(r'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/' +
                           get_summoner_name()[1] + "?api_key=" + key)
    if len(request.json()) == 0:
        print("No ranked data found.")
    else:
        print(request.json())


def get_status():
    status_list = []
    request = requests.get(
        r'https://na1.api.riotgames.com/lol/status/v3/shard-data' + "?api_key=" + key)
    # print(request.json()['services'])
    for status in request.json()['services']:
        #print(status['name'] + ': ' + status['status'])
        status_list.append(status['name'] + ': ' + status['status'])
    return status_list


def get_champion_abilities():
    for champs in champions:
        request = requests.get('http://ddragon.leagueoflegends.com/cdn/' +
                               patch + '/data/en_US/champion/' + champs.name + '.json')
        for x in request.json()['data'][champs.name]['spells']:
            print(x['id'] + '- ' + x['name'] + ': ' + x['description'] + '\n')


champs_played = {}
requested_matches = []
match_info = []


def get_match_history(look_up, num):
    global champs_played
    global requested_matches, match_history
    global team0, team1
    global match_info
    print(champs_played)
    match_history = []
    request = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' +
                           summoners[0][2] + "?api_key=" + key)

    for match in request.json()['matches']:
        match_history.append(match)

    for champion in match_history:
        for champ_id in champions:
            if champion['champion'] == int(champ_id.id):
                champion['champion'] = champ_id.name

    for x in match_history:
        if x['champion'] not in champs_played:
            champs_played[x['champion']] = 1
        else:
            champs_played[x['champion']] += 1

    # print(champs_played)
    if look_up is None:
        pass
    else:
        while True:
            #look_up = input("Want to look at all the games with a perticular champion?")
            if look_up in champs_played:
                for match in match_history:
                    if look_up == match['champion'] or look_up == match['champion'].lower():
                        requested_matches.append(match)
                        print(match)
                break
            else:
                print("Please enter a valid champion")

    # if num is None:
#        pass
#    else:
#        num = int(input("Which game do you want to look at? 0-" +
#                                str(len(requested_matches) - 1)))
        # else:
    #        return
    if num is None:
        pass
    else:
        request = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/' +
                               str(requested_matches[int(num)]['gameId']) + "?api_key=" + key)
        my_json = request.json()
        # print(request.json()) # Holds the game information
        print(request.json()['gameDuration'])
        print(request.json()['gameVersion'])
        print(request.json()['gameMode'])
        print(request.json()['gameType'])

        print("\nEnemy team:")
        print("Team ID:" + str(request.json()['teams'][0]['teamId']))
        print("Victory: " + str(request.json()['teams'][0]['win']))  # Enemy team
        print("First Blood: " + str(request.json()['teams'][0]['firstBlood']))
        print("First Tower: " + str(request.json()['teams'][0]['firstTower']))
        print("Baron Kills: " + str(request.json()['teams'][0]['baronKills']))
        print("Dragon Kills: " + str(request.json()['teams'][0]['dragonKills']))
        print("Rift Herald Kills: " + str(request.json()['teams'][0]['riftHeraldKills']))
        print("Tower Kills: " + str(request.json()['teams'][0]['towerKills']))
        print("Inhibitor Kills: " + str(request.json()['teams'][0]['inhibitorKills']))

        print("\nRequested Summoner's team:")
        print("Team ID:" + str(request.json()['teams'][1]['teamId']))
        print("Victory: " + str(request.json()['teams'][1]['win']))  # Enemy team
        print("First Blood: " + str(request.json()['teams'][1]['firstBlood']))
        print("First Tower: " + str(request.json()['teams'][1]['firstTower']))
        print("Baron Kills: " + str(request.json()['teams'][1]['baronKills']))
        print("Dragon Kills: " + str(request.json()['teams'][1]['dragonKills']))
        print("Rift Herald Kills: " + str(request.json()['teams'][1]['riftHeraldKills']))
        print("Tower Kills: " + str(request.json()['teams'][1]['towerKills']))
        print("Inhibitor Kills: " + str(request.json()['teams'][1]['inhibitorKills']))
        print("\n")

        banned_champs = []
        for ban in request.json()['teams'][0]['bans']:
            for champs in champions:
                if ban['championId'] == int(champs.id):
                    banned_champs.append(champs.name)
        if banned_champs:
            print(banned_champs)
        if not banned_champs:
            print("No champions banned")
        banned_champs = []
        for ban in request.json()['teams'][1]['bans']:
            for champs in champions:
                if ban['championId'] == int(champs.id):
                    banned_champs.append(champs.name)
        print("Banned champions:")
        if banned_champs:
            print(banned_champs)
        if not banned_champs:
            print("No champions banned")

        team0 = []
        team1 = []
        match_information = recordtype("Match", 'summoner_name, champion, items, highestrank, kills, deaths, assists, '
                                                'phy_dmg_dealt_to_champs, mag_dmg_dealt_to_champs,'
                                                'total_dmg_dealt_to_champs, dmg_dealt_to_turrets, vision_score,'
                                                'total_dmg_taken, gold_earned,'
                                                'gold_spent, wards_bought, wards_placed, wards_killed, cs')

        for i_ in request.json()['participants']:
            if int(i_['teamId']) == 100:
                team0.append((i_['teamId'], i_['participantId']))
            else:
                team1.append((i_['teamId'], i_['participantId']))

        # for i_ in request.json()['participantIdentities']:
        #    print(i_)

        for counter_, a in enumerate(team0):
            for i_ in request.json()['participantIdentities']:
                if int(a[1]) == i_['participantId']:
                    team0[counter_] = i_['player']['summonerName']

        for counter_, a in enumerate(team1):
            for i_ in request.json()['participantIdentities']:
                if int(a[1]) == i_['participantId']:
                    team1[counter_] = i_['player']['summonerName']

        players_ = []  # holds the players that were playing the game
        items_ = []  # Holds the items for each summoner
        champions_ = []  # holds the champions played in the match
        highest_ranks_ = []  # holds the players highest rank.
        kills_ = []  # Kills per player
        deaths_ = []  # Deaths per players
        assist_ = []
        phy_dmg_champ_ = []  # Physical damage dealt to champions
        mag_dmg_champ_ = []  # Magic damage dealt to champions
        total_dmg_champ_ = []  # Total damage dealt to champions
        turret_dmg_ = []  # Damage dealt to turrets
        vision_score_ = []  # Vision score for each player
        total_dmg_taken_ = []  # Total damage the player has taken
        gold_earned_ = []  # Total amount of gold the player has earned
        gold_spent_ = []  # Total amount of gold the player has spent
        wards_bought_ = []  # Amount of control wards the player bought
        wards_placed_ = []  # Amount of wards placed down
        wards_killed_ = []  # Number of wards killed
        cs_ = []  # creep score

        for _ in my_json["participantIdentities"]:
            player = _["player"]["summonerName"]
            players_.append(player)

        for _ in my_json["participants"]:
            item = []
            item.extend([_["stats"]["item0"], _["stats"]["item1"], _["stats"]["item2"], _["stats"]["item3"],
                         _["stats"]["item4"], _["stats"]["item5"]])
            items_.append(item)
            champions_.append(_['championId'])
            kills_.append(_["stats"]["kills"])
            deaths_.append(_["stats"]["deaths"])
            assist_.append(_["stats"]["assists"])
            phy_dmg_champ_.append(_["stats"]["physicalDamageDealtToChampions"])
            mag_dmg_champ_.append(_["stats"]["magicDamageDealtToChampions"])
            total_dmg_champ_.append(_["stats"]["totalDamageDealtToChampions"])
            turret_dmg_.append(_["stats"]["damageDealtToTurrets"])
            vision_score_.append(_["stats"]["visionScore"])
            total_dmg_taken_.append(_["stats"]["totalDamageTaken"])
            gold_earned_.append(_["stats"]["goldEarned"])
            gold_spent_.append(_["stats"]["goldSpent"])
            wards_bought_.append(_["stats"]["visionWardsBoughtInGame"])
            try:
                wards_placed_.append(_["stats"]["wardsPlaced"])
                wards_killed_.append(_["stats"]["wardsKilled"])
            except:
                wards_placed_.append(0)
                wards_killed_.append(0)
            cs_.append(_["stats"]["totalMinionsKilled"])
            try:
                highest_ranks_.append(_["highestAchievedSeasonTier"])
            except:
                highest_ranks_.append("NaN")

        for item in items_:  # mapping item id to its name
            for j, subitem in enumerate(item):
                for id in items:
                    if subitem == 0:
                        item[j] = "None"
                    if subitem == int(id.id):
                        item[j] = id.name

        for counter, champion in enumerate(champions_):  # mapping champion id to its name
            for id in champions:
                if champion == int(id.id):
                    champions_[counter] = id.name
                    # print(champions)

        for i in range(10):
            m = match_information(players_[i], champions_[i], items_[i], highest_ranks_[i],
                                  kills_[i], deaths_[i], assist_[i], phy_dmg_champ_[
                                      i], mag_dmg_champ_[i], total_dmg_champ_[i],
                                  turret_dmg_[i], vision_score_[i], total_dmg_taken_[
                                      i], gold_earned_[i], gold_spent_[i],
                                  wards_bought_[i], wards_placed_[i], wards_killed_[i], cs_[i])  # have to work on this...
            match_info.append(m)

        return match_info


def get_champ_info():  # Will get names, titles, lore, skills and tips for each champion
    global champ_information
    for champ in champions:
        try:
            request = requests.get(r'http://ddragon.leagueoflegends.com/cdn/' + patch +
                                   '/data/en_US/champion/' + champ.name + '.json')
            z = request.json()['data'][champ.name]
            champ_information.append([z['id'], z['title'], z['lore'],
                                      z['allytips'], z['enemytips'], z['spells']])
        except:
            pass
    return champ_information


def get_pic():
    global champ_pic
    for champ in champions:
        try:
            pic = urllib.request.urlopen(
                r'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/' + champ.name + '_0.jpg')
            champ_pic.append(pic)
    #img = Image.open(champ_pic[0])
    # img.show()
        except:
            pass


if __name__ == "__main__":
    #get_summoner_name("booty scavanger")
    #get_match_history("Jax", 0)
    pass
#get_summoner_name("TSM Zven")
#match = get_match_history("Xayah", 0)
