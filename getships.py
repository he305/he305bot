import urllib.request
from bs4 import BeautifulSoup
import json
import re


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse_ship_data(html):
    data = {}
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find_all('table', class_='typography-xl-optout infobox infobox-kai infobox-ship')

    for table in tables:
        rows = table.find_all('tr')
        name = rows[0].td.p.span.b.text
        data[name] = {}

        data[name]['Japanese name'] = rows[0].find_all('div')[1].find('span', lang='ja').text
        data[name]['Description'] = rows[0].find_all('p')[1].b.text
        data[name]['HP'] = rows[3].find_all('td')[1].b.text
        data[name]['Firepower'] = rows[3].find_all('td')[3].b.text
        data[name]['Armor'] = rows[4].find_all('td')[1].b.text
        data[name]['Torpedo'] = rows[4].find_all('td')[3].b.text
        data[name]['Evasion'] = rows[5].find_all('td')[1].b.text
        data[name]['AA'] = rows[5].find_all('td')[3].b.text
        data[name]['Aircraft'] = rows[6].find_all('td')[1].b.text
        data[name]['ASW'] = rows[6].find_all('td')[3].b.text
        data[name]['Speed'] = rows[7].find_all('td')[1].b.text
        data[name]['LOS'] = rows[7].find_all('td')[3].b.text
        data[name]['Range'] = rows[8].find_all('td')[1].b.text
        data[name]['Luck'] = rows[8].find_all('td')[3].b.text

        data[name]['image'] = rows[1].find('a', href=True)['href']

        if rows[11].find('td').b.text == "Remodel Level":
            data[name]["Remodel Level"] = rows[12].find('td').b.text

        equipment = [
            rows[14].find_all('td')[1].text.strip(),
            rows[15].find_all('td')[1].text.strip(),
            rows[16].find_all('td')[1].text.strip(),
            rows[17].find_all('td')[1].text.strip()
        ]

        data[name]['Equipment'] = equipment

    return data


def parse_ships(html):
    data = {}
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', class_="wikitable")
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        name = cols[0].a.text
        print("Parsing class " + name + "....")
        data[name] = {}
        ships = cols[1].find_all('a', href=True)
        total_ships_done = 0
        for ship in ships:
            print("Parsing " + ship.text + "....")
            data[name][ship.text] = parse_ship_data(get_html("http://kancolle.wikia.com" + ship['href']))
            total_ships_done += 1
            print("Parsed " + str(total_ships_done) + " of " + str(len(ships)))
    return data

def parse_equip(html):
    data = {}
    soup = BeautifulSoup(html, 'lxml')

    tables = soup.find_all('table', class_='wikitable typography-xl-optout')

    for table in tables:
        rows = table.find_all('tr')

        for row in rows[1:-1]:
            cols = row.find_all('td')

            equip_class = cols[3].text.rstrip()

            found = False
            for k in data:
                if equip_class == k:
                    found = True

            if not found:
                data[equip_class] = {}

            name = cols[2].text.rstrip()

            data[equip_class][name] = {}
            data[equip_class][name]['Classes'] = cols[5].text.rstrip()
            data[equip_class][name]['Craftable'] = cols[6].text.rstrip()
            data[equip_class][name]['Stats'] = {}

            stats_num = re.findall(r'</a>(.*?)<', str(cols[4]), re.DOTALL)

            index = 0
            for stat in cols[4].find_all('a'):
                data[equip_class][name]['Stats'][stat['title']] = stats_num[index]

    return data


def main():
    print("Ship = 0, Equipment = 1")
    a = input()
    if a == '0':
        data_ships = parse_ships(get_html("http://kancolle.wikia.com/wiki/Ship"))
        with open('ships.json', 'w') as f:
            json.dump(data_ships, f)
    else:
        data_equip = parse_equip(get_html("http://kancolle.wikia.com/wiki/Equipment"))
        with open('equip.json', 'w') as f:
            json.dump(data_equip, f)


if __name__ == "__main__":
    main()


