import csv
import datetime
import reverse_geocoder as rg
import json
import jsonpickle
import glob

class MainJson(object):
    category = ""
    date = 0.0
    countries_map = {}
    score = 0

    def update_date(self, date):
        if self.date == 0:
            date2 = datetime.datetime.strptime(date, "%Y%m%d%H%M%S")
            epoch = datetime.datetime.utcfromtimestamp(0)
            self.date = ((date2 - epoch).total_seconds()*1000.0)

    def update_score(self):
        self.score = self.score + 1

    def __init__(self, category):
        self.category = category
        self.countries_map = {}
        self.date = 0.0
        self.score = 0.0

def get_date_in_ms(date):
    date2 = datetime.datetime.strptime(date, "%Y%m%d%H%M%S")
    epoch = datetime.datetime.utcfromtimestamp(0)
    return ((date2 - epoch).total_seconds()) * 1000.0

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def word_freq():
    map_of_objects = {}
    category_map = {}
    with open('CategoryList.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category_name = row['Name']
            obj = MainJson(category_name)
            map_of_objects[category_name] = obj
            countries_map = {}
            with open('countries_medialist.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    s = row['country']
                    countries_map[s.strip()] = {'Sad': 0, 'Happy': 0, 'Anger': 0, 'Hatred': 0, 'Fear': 0}
            category_map[category_name] = countries_map

    map = {}
    c15_reader = []
    new_map = {}
    new_map['Anger'] = 0
    new_map['Sad'] = 0
    new_map['Hatred'] = 0
    new_map['Happy'] = 0
    new_map['Fear'] = 0

    #print(countries_map)

    with open('whitelist.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            s = row['Emotion']
            t = row['c15']
            if len(t) > 0:
                c15_reader.append(t)
            map[t] = s

    for gkg_csv_file in glob.glob('*.gkg.csv'):
        print(gkg_csv_file)
        word = ""
        with open(gkg_csv_file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter = '\t')
            for row in reader:
                s = row['GCam']
                u = row['Locations']
                date_l = row['Date']
                event_counts = row['EventCounts']
                if (len(event_counts) != 0):
                    category = event_counts[0:event_counts.index('#')]
                else:
                    continue

                #print(category)
                if category not in category_map.keys():
                    continue

                map_of_objects[category_name].update_date(date_l)
                map_of_objects[category_name].update_score()

                #print("Object " + str(map_of_objects[category_name].date))

                fourth_index = find_nth(u, "#", 4) + 1
                fifth_index_1 = find_nth(u, "#", 5)
                fifth_index_2 = fifth_index_1 + 1
                sixth_index = find_nth(u, "#", 6)
                if(len(u[fourth_index:fifth_index_1]) != 0):
                    lat = float(u[fourth_index:fifth_index_1])
                if(len(u[fifth_index_2:sixth_index]) != 0):
                    long = float(u[fifth_index_2:sixth_index])

                y = s.strip().split(",")
                max_key = ""
                max_val = 0
                for i in y:
                    if((i[0] != 'w' and i[0] != 'v' and len(i) != 0)):
                        try:
                            word = i.split(':')[0]
                            val = i.split(':')[1]
                            if (len(word) > 0 and len(val) > 0):
                                if word in c15_reader:
                                    if (float(val) > float(max_val)):
                                        max_val = val
                                        max_key = word
                        except IndexError:
                            pass

                if len(max_key) > 0:
                    add = rg.search((lat, long))[0]['cc']
                    #print(add)
                    try:
                        category_map[category][add][map[max_key]] = category_map[category][add][map[max_key]] + float(max_val)
                    except KeyError:
                        pass
        csvfile.close()
        
    for k, v in category_map.items():
        map_of_objects[k].countries_map = category_map[k]
        print(map_of_objects[k].date)

    with open('emotions_jsonlist.json', 'w') as outfile:
        final_frozen = "["
        for key, value in map_of_objects.items():
            print(value.date)
            frozen = jsonpickle.encode(value)
            final_frozen = final_frozen + frozen + ","
        final_frozen = final_frozen[:-1] + "]"
        print(final_frozen)
        outfile.write(final_frozen)
    outfile.close()

word_freq()
