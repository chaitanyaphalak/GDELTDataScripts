import jsonpickle
import csv
import json
import datetime
import glob

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

class Subpart(object):
    lat = 0
    long = 0
    organization = ""
    def __init__(self, lat, long, organization):
        self.lat = lat
        self.long = long
        self.organization = organization

class MainJson(object):
    id = ""
    score = 0
    date = None
    subpart_list = []

    def update_date(self,date):
            date2 = datetime.datetime.strptime(date, '%Y%m%d%H%M%S').date()
            self.date = date2

    def update_score(self):
        self.score = self.score + 1

    def update_subpart_list(self, item):
        self.subpart_list.append(item)

    def __init__(self, id, score, subpart_list):
        self.id = id
        self.score = score
        self.subpart_list = subpart_list

def word_freq():
    map = {}

    for gkg_csv_file in glob.glob('*.csv'):
        print(gkg_csv_file)
        with open(gkg_csv_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                s = row['Name']
                t = row['Description']
                obj = MainJson(t, 0, [])
                map[s] = obj

        with open('FinalData.csv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter = '\t')
            for row in reader:
                s = row['EventCounts']
                t = row['Organizations']
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

                sub_part = Subpart(lat, long, t)

                if(len(s) != 0):
                    word = s[0:s.index('#')]
                    if(word in map.keys()):
                        map[word].update_score()
                        map[word].update_subpart_list(sub_part)
                elif(len(theme) != 0):
                    word = theme[0:theme.index(';')]
                    if(word in map.keys()):
                        map[word].update_score()
                        map[word].update_subpart_list(sub_part)

    with open('jsonlist.json', 'w') as outfile:
        for key, value in map.items():
            frozen = jsonpickle.encode(value)
            print(frozen)
            print(',')
            outfile.write(frozen)

word_freq()


