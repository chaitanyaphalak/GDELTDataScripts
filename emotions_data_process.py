import jsonpickle
import csv
import json
import datetime

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

class Subpart(object):
    lat = 0
    long = 0
    emotion = {}
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.emotion['Anger'] = 0
        self.emotion['Sad'] = 0
        self.emotion['Hatred'] = 0
        self.emotion['Happy'] = 0
        self.emotion['Fear'] = 0

class MainJson(object):
    id = ""
    subpart_list = []

    def update_subpart_list(self, item):
        self.subpart_list.append(item)

    def __init__(self, id, subpart_list):
        self.id = id
        self.subpart_list = subpart_list

def word_freq():
    map = {}
    c15_reader = []

    with open('whitelist.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            s = row['Emotion']
            t = row['c15']
            if len(t) > 0:
                c15_reader.append(t)
            map[t] = s

    with open('CategoryList.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            s = row['Name']
            t = row['Description']
            obj = MainJson(t, [])
            map[s] = obj

    with open('FinalData.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter = '\t')
        for row in reader:
            s = row['EventCounts']
            u = row['Locations']
            theme = row['Themes']

            fourth_index = find_nth(u, "#", 4) + 1
            fifth_index_1 = find_nth(u, "#", 5)
            fifth_index_2 = fifth_index_1 + 1
            sixth_index = find_nth(u, "#", 6)
            if(len(u[fourth_index:fifth_index_1]) != 0):
                lat = float(u[fourth_index:fifth_index_1])
            if(len(u[fifth_index_2:sixth_index]) != 0):
                long = float(u[fifth_index_2:sixth_index])

            sub_part = Subpart(lat, long)
            gcam = row['GCam']
            y = gcam.strip().split(",")
            for i in y:
                if((i[0] != 'w' and i[0] != 'v' and len(i) != 0)):
                    try:
                        word = i.split(':')[0]
                        val = i.split(':')[1]
                        if (len(word) > 0 and len(val) > 0):
                            if word in c15_reader:
                                sub_part.emotion[map[word]] = sub_part.emotion[map[word]] + float(val)
                                #print(map[word],sub_part.emotion[map[word]])
                    except IndexError:
                        pass

            if(len(s) != 0):
                word = s[0:s.index('#')]
                if(word in map.keys()):
                    map[word].update_subpart_list(sub_part)
            elif(len(theme) != 0):
                word = theme[0:theme.index(';')]
                if(word in map.keys()):
                    map[word].update_subpart_list(sub_part)

    with open('jsonlist_emotions.json', 'w') as outfile:
        for key, value in map.items():
            frozen = jsonpickle.encode(value)
            print(frozen)
            print(',')
            outfile.write(frozen)

word_freq()