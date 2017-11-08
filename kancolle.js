var fs = require('fs');
var prompt = require('prompt');

var shipData = {};

module.exports = {
    getShip : function(shipName, shipNumber, cb) {

        shipName = shipName.charAt(0).toUpperCase() + shipName.slice(1);

        for (shipClass in shipData) {
            for (ship in shipData[shipClass]) {
                if (ship == shipName) {
                    ship_table = shipData[shipClass][ship][Object.keys(shipData[shipClass][ship])[shipNumber-1]];

                    if (ship_table == undefined) {
                        return;
                    }

                    let msg = '';
                    msg += 'Name : ' + Object.keys(shipData[shipClass][ship])[shipNumber-1] + '\n';
                    msg += 'Japanese name : ' + ship_table['Japanese name'] + '\n';
                    msg += 'HP : ' + ship_table['HP'] + '\n';
                    msg += 'Firepower : ' + ship_table['Firepower'] + '\n';
                    msg += 'Armor : ' + ship_table['Armor'] + '\n';
                    msg += 'Torpedo : ' + ship_table['Torpedo'] + '\n';
                    msg += 'Evasion : ' + ship_table['Evasion'] + '\n';
                    msg += 'AA : ' + ship_table['AA'] + '\n';
                    msg += 'Aircraft : ' + ship_table['Aircraft'] + '\n';
                    msg += 'ASW : ' + ship_table['ASW'] + '\n';
                    msg += 'Speed : ' + ship_table['Speed'] + '\n';
                    msg += 'LOS : ' + ship_table['LOS'] + '\n';
                    msg += 'Range : ' + ship_table['Range'] + '\n';
                    msg += 'Luck : ' + ship_table['Luck'] + '\n';
                    msg += 'Class : ' + shipClass + '\n';
                    msg += 'image : ' + ship_table['image'];

                    cb(msg);
                    return;
                }
            }
        }

        cb('Ты шо долбоёб? Нет такого корабля');
    }
}


fs.readFile("ships.json", 'utf8', function(err, data) {
   if (err) throw err;
   shipData = JSON.parse(data);
});


if (require.main === module) {

    prompt.start();

    prompt.get(['shipName', 'number'], (err, result) => {
        if (err) throw err;
        module.exports.getShip(result.shipName, parseInt(result.number), function(result) {
            console.log(result);  
        });
    });
}