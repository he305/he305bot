import requests
import xmltodict
import datetime
import math

week_days = [
    'понедельник',
    'вторник',
    'среду',
    'четверг',
    'пятницу',
    'субботу',
    'воскресенье'
]

def day_conjugation(day):
    if day == 1:
        return ' день'
    elif day < 5:
        return ' дня'
    return ' дней'

def get_anime(user='he3050'):
    par = {'u' : user, 'status' : 'all', 'type' : 'anime'}
    r = requests.get('http://myanimelist.net/malappinfo.php', params=par)

    #Check for 404 error, it shouldn't happen after all, but still
    if r.status_code == 404:
        print('error 404')
        return

    doc = xmltodict.parse(r.text)['myanimelist']

    for value in doc['anime']:
        if value['my_status'] == '1':
            msg = ''

            msg += value['series_title'] + " - " + value['my_watched_episodes'] + ' серий.\n'

            series_start = datetime.datetime.strptime(value['series_start'], '%Y-%m-%d').date()
            date_diff = datetime.date.today() - series_start
            all_eps = date_diff.days / 7 + 1
            all_eps = math.floor(all_eps)
            
            total_eps = int(value['series_episodes'])
            if all_eps > total_eps and not total_eps == 0:
                all_eps = total_eps

            if not int(value['my_watched_episodes']) == all_eps:
                eps_not_watched = all_eps - int(value['my_watched_episodes'])
                msg += str(eps_not_watched) + ' не отсмотрено.\n'

            if int(value['series_status']) == 1:
                i = 0
                while i - date_diff.days < 0:
                    i += 7
                msg += 'Новая серия через ' + str(i-date_diff.days) + day_conjugation(i-date_diff.days) + '. В ' + week_days[series_start.weekday()]
            msg += '\n'
            yield msg 

if __name__ == "__main__":
    for i in get_anime():
        print(i)