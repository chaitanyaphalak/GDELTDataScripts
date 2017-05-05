import jsonpickle
import csv
import json
import datetime
import glob

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

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
    tone = 0
    def __init__(self, lat, long, organization, tone):
        self.lat = lat
        self.long = long
        self.organization = organization
        self.tone = tone

class MainJson(object):
    id = ""
    score = 0
    date = 0.0
    tone = 0.0
    URL = ""
    subpart_list = []

    def update_date(self, date):
        #print(date)
        date2 = datetime.datetime.strptime(date, "%Y%m%d%H%M%S")
        epoch = datetime.datetime.utcfromtimestamp(0)
        self.date = ((date2 - epoch).total_seconds()*1000.0)

    def update_score(self):
        self.score = self.score + 1

    def update_URL(self, URL):
        self.URL = URL

    def update_subpart_list(self, item):
        self.subpart_list.append(item)

    def __init__(self, id, score, subpart_list):
        self.id = id
        self.score = score
        self.subpart_list = subpart_list

def word_freq():
    map = {}

    with open('CategoryList.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            s = row['Name']
            t = row['Description']
            obj = MainJson(t, 0, [])
            map[s] = obj

    for gkg_csv_file in glob.glob('FinalData_URL.csv'):
        print(gkg_csv_file)
        word = ""
        with open(gkg_csv_file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter = '\t')
            for row in reader:
                date_l = row['Date']
                s = row['EventCounts']
                t = row['Organizations']
                u = row['Locations']
                theme = row['Themes']
                z = row['Tone']
                URL = row['URL']
                print(URL)
                try:
                    tone = z[0:z.index(',')]
                    fourth_index = find_nth(u, "#", 4) + 1
                    fifth_index_1 = find_nth(u, "#", 5)
                    fifth_index_2 = fifth_index_1 + 1
                    sixth_index = find_nth(u, "#", 6)
                    if(len(u[fourth_index:fifth_index_1]) != 0):
                        lat = float(u[fourth_index:fifth_index_1])
                    if(len(u[fifth_index_2:sixth_index]) != 0):
                        long = float(u[fifth_index_2:sixth_index])

                    sub_part = Subpart(lat, long, t, tone)

                    if(len(s) != 0):
                        word = s[0:s.index('#')]
                        if(word in map.keys()):
                            map[word].update_score()
                            map[word].update_URL(URL)
                            map[word].update_subpart_list(sub_part)
                            map[word].update_date(date_l)
                    elif(len(theme) != 0):
                        word = theme[0:theme.index(';')]
                        if(word in map.keys()):
                            map[word].update_score()
                            map[word].update_URL(URL)
                            map[word].update_subpart_list(sub_part)
                            map[word].update_date(date_l)

                except AttributeError:
                    pass
        csvfile.close()

    with open('jsonlist.json', 'w') as outfile:
        final_frozen = "["
        for key, value in map.items():
            frozen = jsonpickle.encode(value)
            final_frozen = final_frozen + frozen + ","
        final_frozen = final_frozen[:-1] + "]"
        print(final_frozen)
        outfile.write(final_frozen)
    outfile.close()

word_freq()