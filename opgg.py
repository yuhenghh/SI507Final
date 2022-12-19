#########################################
##### Name:Yuheng He                         #####
##### Uniqname:yuhenghe                     #####
#########################################
import webbrowser
from urllib.request import urlopen
import json
import sys

import requests
"""
To create a complete Itunes url

@u: target songs and limitation of search
@return: the cascaded string
"""
def create_url_m(u):
    u = u.split(' ')
    url_l = 'https://itunes.apple.com/search?term='
    for i in range(0, len(u)):
        url_l += u[i]
        url_l += '+'
    url_l += '&limit=' + str(lim1)
    print(url_l)
    return url_l

"""
Create a class that called Media

@title
@author
@release_year
@url
@json
@return: the cascaded string
"""
class Media:

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json="None"):
        self.title = title
        self.author = author
        self.release_year = release_year
        self.url = url
        self.json = json
        if self.json != "None":
            self.title = json["trackName"]
            self.author = json["artistName"]
            self.release_year = json["releaseDate"].split("-")[0]
            self.url = json["trackViewUrl"]

    def info(self):
        comb = self.title + " by " + self.author + " (" + str(self.release_year) + ")"
        return comb

    def length(self):
        return 0


# Other classes, functions, etc. should go here
class Song(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL",
                 album="No Album", genre="No Genre", track_length=0, json="None"):
        super().__init__(title, author, release_year, url, json)
        self.album = album
        self.genre = genre
        self.track_length = track_length
        if self.json != "None":
            self.title = json["trackName"]
            self.album = json["collectionName"]
            self.genre = json["primaryGenreName"]
            self.track_length = json["trackTimeMillis"]

    def info(self):
        return super().info() + " [" + self.genre + "]"

    def length(self):
        return int(self.track_length / 1000)


class Movie(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL",
                 rating="No Rating", movie_length=0, json="None"):
        super().__init__(title, author, release_year, url, json)
        self.rating = rating
        self.movie_length = movie_length
        if self.json != "None":
            self.title = json["trackName"]
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = json["trackTimeMillis"]

    def info(self):
        return super().info() + " [" + self.rating + "]"

    def length(self):
        return int(self.movie_length / 1000 / 60)

"""
Use riot API to fetch summoner ranking information

"""
def sum_info(region,sum_name):
    api_key = 'RGAPI-c42a398b-fefe-49da-8862-dbddedf31c70'
    watcher = LolWatcher(api_key)
    my_region = region
    me = watcher.summoner.by_name(my_region, sum_name)
    my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
    print('Here are the 5x5 rank records')
    for items in ((my_ranked_stats[0])):
        print(items,": ",my_ranked_stats[0][items])
    print(' ')
    print('Here are the Solo rank records')
    for items in ((my_ranked_stats[1])):
        print(items,": ",my_ranked_stats[1][items])

"""
Prompt the option menu

"""
def Prompt():
    print('Do you want to \n 1- Search summoner info\n 2- Search Champ info\n 3-Search Music')

"""
funtion that check if the user want to exit the system
"""
def check_exit(inp):
    if inp == 'exit':
        print('Bye!')
        sys.exit()

"""
Create a complete champion search url based on user's input

@u: user input champion name
"""

def create_url(u):
    url_l = 'http://ddragon.leagueoflegends.com/cdn/12.23.1/data/en_US/champion/'
    url_l = url_l + u + ".json"
    return url_l

class Champ:

    def __init__(self, champ_id="No id", champ_title="No title", \
                 skins=[], lore="No lore", allytips="None", \
                 enemytips="None", json="None"):
        self.champ_id = champ_id
        self.champ_title = champ_title
        self.skins = skins
        self.lore = lore
        self.allytips = allytips
        self.enemytips = enemytips
        self.json = json
        if self.json != "None":
            self.champ_id = champ_id
            self.champ_title = json["data"][champ_id]["title"]
            for i in range(len(json["data"][champ_id]["skins"])):
                skins.append(json["data"][champ_id]["skins"][i]["name"])
            self.lore = json["data"][champ_id]["lore"]
            self.allytips = json["data"][champ_id]["allytips"]
            self.enemytips = json["data"][champ_id]["enemytips"]

    def champ_intro(self):
        return "Hi, I am " + self.champ_title + " " + self.champ_id + "!\n"

    def skin_info(self):
        print("This champ has skins as listed \n")
        i = 0
        for item in range(len(self.skins)):
            print(str(i)+"- "+self.skins[item])
            i= i+1

    def lore_info(self):
        print("The background stroy of this champ is "+self.lore)

    def ingame_info(self):
        print("Ally tips\n")
        i= 1
        for items in range(len(self.allytips)):
            print(str(i)+"- "+self.allytips[items])
            i = i+1
        i = 1
        print("enemy tips\n")
        for items in range(len(self.enemytips)):
            print(str(i)+"- "+self.enemytips[items])
            i = i+1
    def champ_info(self):
        self.champ_intro()
        self.lore_info()
        self.ingame_info()
        self.skin_info




from riotwatcher import LolWatcher, ApiError
import pandas as pd

# golbal variables


while 1:
    Prompt()
    x = input()
    if x=='1':
        y= input('Please enter a summonerID')
        check_exit(y)
        sum_info('na1',y)
    elif x=='2':
        y = input('Which champ info you want to know?')
        check_exit(y)
        champinfo_url = create_url(y)
        response = urlopen(champinfo_url)
        data_json = json.loads(response.read())
        champ = Champ(champ_id=y, json=data_json)
        champ.champ_info()
        champ.skin_info()
    elif x=='3':
        songs = []
        movies = []
        medias = []
        # your control code for Part 4 (interactive search) should go here
        x = input('Enter a search term, or "exit" to quit ')
        check_exit(x)
        lim1 = int(input('Please input the maximum number of results you wish to show '))  # limit of results
        index = 1  # index of output
        url = create_url_m(x)
        json_temp = requests.get(url).json()["results"]  # get json file from API
        if len(json_temp) < lim1:  # make sure it will handle when there is not enough result
            lim1 = len(json_temp)
        if len(json_temp) != 0:  # make sure it will handle when there is no result
            for i in range(0, lim1):
                if json_temp[i]['wrapperType'] == 'track':
                    if json_temp[i]['kind'] == 'feature-movie':
                        movies.append(Movie(json=json_temp[i]))
                    if json_temp[i]['kind'] == "song":
                        songs.append(Song(json=json_temp[i]))
                else:
                    medias.append(Media(json=json_temp[i]))

        if len(songs) != 0:
            print('Here are the related songs\n')
        else:
            print('Sorry we cannot find related songs\n')
        for c in songs:
            print('    ' + str(index) + '. ' + c.info())
            print(' ')
            index += 1

        if len(movies) != 0:
            print('Here are the related movies\n')
        else:
            print('Sorry we cannot find related movies\n')
        index = 1
        for m in movies:
            print('    ' + str(index) + '. ' + m.info())
            print(' ')
            index += 1

        if len(medias) != 0:
            print('Here are the related media\n')
        else:
            print('Sorry we cannot find related media\n')
        index = 1
        for mo in medias:
            print('    ' + str(index) + '. ' + mo.info())
            print(' ')
            index += 1

        print('Enter a number for more info, or another search term, or exit')
        print('1 to keep searching')
        print('2 launch url of the first song in web browser')
        print('Enter exit to exit system')
        flag = 1
        while flag == 1:
            y = input()
            check_exit(y)
            if int(y) > 2:
                print('Please input a valid operator, if you wish the exit, input exit')
                print('2')
            else:
                flag = 0

        if y == '2':
            flag = 1
            while flag == 1:
                ind = int(input('Please input the index of song that you wish to open '))
                check_exit(ind)
                if ind <= lim1:
                    webbrowser.open(songs[ind - 1].url)
                    flag = 0
                else:
                    print('Please do not exceed the maximum number of index\n')

    else:
        Prompt()
    check_exit(x)
