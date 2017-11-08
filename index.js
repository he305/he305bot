const TelegramBot = require('node-telegram-bot-api');
var fs = require('fs');
var https = require('https');

var commands = require('./commands');
var anime = require('./anime');
var kancolle = require('./kancolle');

const TOKEN = "455027497:AAHFoH9rc8sSoRqVd5PqzKqBhpAMT7H9tDQ"

const bot = new TelegramBot(TOKEN, {polling: true});

class User {

	constructor(name, chatId, mal=null) {
		this.name = name;
		this.chatId = chatId;
		this.mal = mal;
	}

	formJson() {
		return JSON.stringify({
			'name' : this.name,
			'mal' : this.mal
		});
	}
}

var users = new Array();


fs.readdir("sessions/", (err, files) => {
	if (err) return console.log(err);
	files.forEach(file => {
		fs.readFile("sessions/" + file, 'utf8', function(err, data) {
			if (err) return console.log(err);
			user_data = JSON.parse(data);
			user = new User(user_data['name'], file.split('.')[0], user_data['mal']);
			users.push(user);
		});
	});
});

bot.onText(/\/help$/, (msg) => {
	for (command in commands.commands) {
		bot.sendMessage(msg.chat.id, command + ' - ' + commands.commands[command]);
	}
});

bot.onText(/\/start$/, (msg) => {
	for (var i = 0; i < users.length; i++) {
		if (users[i].chatId === msg.chat.id.toString()) {
			bot.sendMessage(msg.chat.id, "Кулити, " + users[i].name);
			return;
		}
	}

	bot.sendMessage(msg.chat.id, "Кулити, как звать то (/start имя)");
});

bot.onText(/\/start (.*)/, function(msg, match) {

	for (var i = 0; i < users.length; i++) {
		if (users[i].chatId === msg.chat.id.toString()) {
			bot.sendMessage(msg.chat.id, users[i].name + ", ты шо ретурд?");
			return;
		}
	}

	var user = new User(match[1], msg.chat.id);
	fs.writeFile("sessions/" + msg.chat.id + ".json", user.formJson(), function(err) {
		if (err)
			return console.log(err);
		users.push(user);
		console.log(match[1] + " created");
	});

	bot.sendMessage(msg.chat.id, "Кулити, " + match[1]);
});

bot.onText(/\/add_mal (.*)/, function(msg, match) {
	mal = match[1];
	https.get("https://myanimelist.net/malappinfo.php?u=" + mal + "&status=all", function(res) {
		data = '';
        res.setEncoding('utf8');
		res.on('data', function (chunk) {
		    data += chunk;
		});

		res.on('end', function() {

			//Very stupid way to check for 404, but i don't see any other (status code always 200)
			if (data.length == 66) {
				bot.sendMessage(msg.chat.id, 'Ты шо долбоёб? Нет такого пользователя');
				return;
			}

			for (var i = 0; i < users.length; i++) {
				if (users[i].chatId === msg.chat.id.toString()) {
					users[i].mal = mal;
					fs.writeFile("sessions/" + msg.chat.id + ".json", users[i].formJson(), function(err) {
						if (err)
							return console.log(err);
					});
					bot.sendMessage(msg.chat.id, "Готово");
				}
			}
		});
	});	
});

bot.onText(/\/anime_watching/, (msg) => {
	for (var i = 0; i < users.length; i++) {
		if (users[i].chatId === msg.chat.id.toString()) {
			if (users[i].mal == null) {
				bot.sendMessage(msg.chat.id, "Мала нет, зарегай, /add_mal (nickname)");
				return
			}

			bot.sendMessage(msg.chat.id, "Работает папсназ");

			anime.get_anime(users[i].mal, (result) => {
				bot.sendMessage(msg.chat.id, result);
			});
		}
	}
});


bot.onText(/\/get_ship (.*) ([1-5])?/, (msg, match) => {
	shipName = match[1];
	shipNumber = match[2];

	kancolle.getShip(shipName, shipNumber, function(result) {
		bot.sendMessage(msg.chat.id, result);
	});
});

bot.onText(/\/get_ship (.*)/, (msg, match) => {
	shipName = match[1];
	shipNumber = 1;

	kancolle.getShip(shipName, shipNumber, function(result) {
		bot.sendMessage(msg.chat.id, result);
	});
});


bot.onText(/.*[нН]авальн.*/, (msg) => {
	bot.sendMessage(msg.chat.id, "20!8");
});

bot.onText(/.*[яЯ]рик пидор.*/, (msg) => {
	bot.sendMessage(msg.chat.id, "Тут соглы+++", {reply_to_message_id : msg.message_id});
});

bot.onText(/\/happy/, (msg) => {
	bot.sendPhoto(msg.chat.id, 'pics/happy.png');
});

bot.onText(/^\(*$/, (msg) => {
	bot.sendMessage(msg.chat.id, ")))", {reply_to_message_id : msg.message_id});
});