import csv
from geopy.geocoders import Nominatim

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def word_freq():
    countries_map = {}
    map = {}
    c15_reader = []
    new_map = {}
    new_map['Anger'] = 0
    new_map['Sad'] = 0
    new_map['Hatred'] = 0
    new_map['Happy'] = 0
    new_map['Fear'] = 0
    geolocator = Nominatim()

    with open('countries_medialist.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            s = row['country']
            countries_map[s.strip()] = {'Sad': 0, 'Happy': 0, 'Anger': 0, 'Hatred': 0, 'Fear': 0}

    print(countries_map)

    with open('whitelist.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            s = row['Emotion']
            t = row['c15']
            if len(t) > 0:
                c15_reader.append(t)
            map[t] = s

    with open('FinalData_emo.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter = '\t')
        for row in reader:
            s = row['GCam']
            u = row['Locations']
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
                #print(map[max_key], max_val)
                location = geolocator.reverse(str(lat)+","+ str(long), language='en')
                add = location.address
                add = add.split(",")
                add = add[-1].strip()
                print(map[max_key], add)
                try:
                    countries_map[add][map[max_key]] = countries_map[add][map[max_key]] + float(max_val)
                    print(countries_map[add][map[max_key]])
                    new_map[map[max_key]] = new_map[map[max_key]] + float(max_val)
                    #print(new_map)
                    #print(countries_map)
                except KeyError:
                    pass
    '''            
    with open('data.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["emotion", "totalcount"])
        for key, value in new_map.items():
            writer.writerow([key, value])
    '''
    print(new_map)
    #print(map)
    print(countries_map)

word_freq()