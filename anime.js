var https = require('https');
var xml2js = require('xml2js');
parser = new xml2js.Parser();

days = [
    'воскресенье',
    'понедельник',
    'вторник',
    'среду',
    'четверг',
    'пятницу',
    'субботу'
];

function dayConjuguation(day) {
    if (day == 1) {
        return 'день';
    }
    else if (day < 5) {
        return 'дня';
    }
    return 'дней';
}

module.exports = {
    get_anime : function (mal, _callback) {
        https.get("https://myanimelist.net/malappinfo.php?u=" + mal + "&status=all", function(res) {
            var response_data = '';
            res.setEncoding('utf8');
            res.on('data', function(chunk) {
                response_data += chunk;
            });

            res.on('end', function() {
                parser.parseString(response_data, function(err, result) {
                    if (err) console.log(err.message);
                    else {
                        result = JSON.parse(JSON.stringify(result));

                        for (var i = 0; i < result['myanimelist']['anime'].length; i++) {
                            let anime = result['myanimelist']['anime'][i];
                            if (anime['my_status'][0] === '1') {
                                let info = '';

                                info += anime['series_title'][0] + ' - ' + anime['my_watched_episodes'][0] + ' серий\n';
                                date = new Date(anime['series_start'][0]);
                                diffDays = (new Date() - date)/1000/3600/24;
                                let all_eps = Math.floor(diffDays/7+1);

                                if (anime['series_status'][0] == '2') {
                                    all_eps = parseInt(anime['series_episodes'][0]);
                                }

                                if (parseInt(anime['my_watched_episodes'][0]) != all_eps) {
                                    eps_not_watched = all_eps - parseInt(anime['my_watched_episodes'][0])
                                    info += eps_not_watched.toString() + ' не отсмотрено\n';
                                }

                                if (parseInt(anime['series_status'][0]) == 1) {
                                    index = 0;
                                    while (index - diffDays <= 0) {
                                        index += 7;
                                    }
                                    daysToNew = Math.ceil(index - diffDays);
                                    info += 'Новая серия через ' + daysToNew.toString() + ' ' + dayConjuguation(daysToNew) + '. В ' + days[date.getDay()] + '\n';
                                }

                                if (require.main !== module) {
                                    info += anime['series_image'];
                                }

                                _callback(info);
                            }
                        }
                    }
                });
            });

            res.on('error', function(err) {
                console.log(err.message);
            });
        });
    }
}

if (require.main === module) {
    module.exports.get_anime('he3050', function(result) {
      console.log(result);  
    });
}