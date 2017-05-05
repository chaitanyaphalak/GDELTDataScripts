import csv

def word_freq():
    map = {}
    c15_reader = []
    new_map = {}
    new_map['Anger'] = 0
    new_map['Sad'] = 0
    new_map['Hatred'] = 0
    new_map['Happy'] = 0
    new_map['Fear'] = 0

    with open('whitelist.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            s = row['Emotion']
            t = row['c15']
            if len(t) > 0:
                c15_reader.append(t)
            map[t] = s

    with open('FinalData.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter = '\t')
        for row in reader:
            s = row['GCam']
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
                new_map[map[max_key]] = new_map[map[max_key]] + float(max_val)

    with open('donut_chart_data.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["emotion", "totalcount"])
        for key, value in new_map.items():
            writer.writerow([key, value])

    print(new_map)

word_freq()