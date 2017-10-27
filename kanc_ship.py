import json
import io
import pprint
import re

stats_list = [
    'Firepower',
    'Armor',
    'Evasion',
    'Torpedo',
    'AA',
    'HP',
    'ASW',
    'LOS',
    'Luck'
]

def load_data():
    with open('ships.json') as data_file:
        data = json.load(data_file)
        return data

def strongest_by_class(ship_class):
    data = load_data()

    max_stat = 0

    ship_dict = {}

    pattern = re.compile('\((\d+)\)')

    for ship_full in data[ship_class]:
        ship = data[ship_class][ship_full]
        for ship_subtype in ship.values():
            stats = 0
            
            for stat in stats_list:
                if pattern.search(ship_subtype[stat]) == None:
                    continue
                stats += int(pattern.search(ship_subtype[stat]).group()[1:-1])

            ship_dict[ship_full] = stats

            if stats > max_stat:
                max_stat = stats
                ship_name = ship_full


    d = sorted(ship_dict.items(), key=lambda x: x[1], reverse=True)
    i = 0
    for k, v in d:
        if i == 25: break
        print(k + ' ' + str(v))
        i += 1
    return ''

def strongest_by_class_and_stat(ship_class, stat):
    data = load_data()

    stat_max = 0

    for ship_full in data[ship_class]:
        ship = data[ship_class][ship_full]
        for ship_subtype in ship.values():
            stat_cur = int(re.findall('\((\d+)\)', ship_subtype[stat])[0])
            if stat_cur > stat_max:
                stat_max = stat_cur
                ship_name = ship_full

    return ship_name

def get_ship(name):
    name = name.title()
    data = load_data()
    #print(data['Battleship']['Yamato'])
    for class_ship in data:
        if name in data[class_ship]:
            ship = data[class_ship][name]
            for ship_subtype in ship.values():
                msg = ''
                msg += 'Japanese name - ' + ship_subtype['Japanese name'] + '\n'
                msg += 'HP - ' + ship_subtype['HP'] + '\n'
                msg += 'Firepower - ' + ship_subtype['Firepower'] + '\n'
                msg += 'Armor - ' + ship_subtype['Armor'] + '\n'
                msg += 'Torpedo - ' + ship_subtype['Torpedo'] + '\n'
                msg += 'Evasion - ' + ship_subtype['Evasion'] + '\n'
                msg += 'AA - ' + ship_subtype['AA'] + '\n'
                msg += 'Aircraft - ' + ship_subtype['Aircraft'] + '\n'
                msg += 'ASW - ' + ship_subtype['ASW'] + '\n'
                msg += 'Speed - ' + ship_subtype['Speed'] + '\n'
                msg += 'LOS - ' + ship_subtype['LOS'] + '\n'
                msg += 'Range - ' + ship_subtype['Range'] + '\n'
                msg += 'Luck - ' + ship_subtype['Luck'] + '\n'
                yield msg
            return    


if __name__ == '__main__':
    print(strongest_by_class("Destroyer"))

    # print("Input name", end=' ')
    # #name = input()
    # for i in get_ship('Yuudachi'):
    #     print(i)