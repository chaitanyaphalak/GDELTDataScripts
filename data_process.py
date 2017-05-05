import csv
import json
import datetime

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def word_freq():
    #take categories from file
    #if eventcounts blank look at another column
    map = {}
    new_map = {}

    with open('CategoryList.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            s = row['Name']
            map[s] = 0
    #print(map)

    with open('FinalData.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter = '\t')
        for row in reader:
            s = row['EventCounts']
            t = row['Organizations']
            u = row['Locations']
            date = row['Date']
            date2 = datetime.datetime.strptime(date, '%Y%m%d%H%M%S').date()

            fourth_index = find_nth(u, "#", 4) + 1
            fifth_index_1 = find_nth(u, "#", 5)
            fifth_index_2 = fifth_index_1 + 1
            sixth_index = find_nth(u, "#", 6)
            if(len(u[fourth_index:fifth_index_1]) != 0):
                lat = float(u[fourth_index:fifth_index_1])
            if(len(u[fifth_index_2:sixth_index]) != 0):
                long = float(u[fifth_index_2:sixth_index])
            #print(lat, long)
            event_list = []
            event_list.append({'lat': lat, 'long': long, 'organizations': t })
            print(event_list)

            if(len(s) != 0):
                word = s[0:s.index('#')]
                if(word in map.keys()):
                    map[word] = map[word] + 1

    json_list = []
    for key in map.keys():
        json_list.append({'id': key , 'score': map[key]})
    data = json.dumps(json_list)
    with open('jsonlist.json', 'w') as outfile:
        json.dump(data, outfile)

word_freq()