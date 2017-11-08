const http = require('http');

function* generator() {
    for (var i = 0; i < 10; i++) {
        yield i;
    }
}

function call(_callback) {
    for (let i = 0; i < 10; i++) {
        _callback(i);
    }
}

function main() {
    var gen = [...generator()];
    for (var value in gen) {
        console.log(value);
    }

    call(function(result){
        console.log(result);
    });
}


function test() {
    var vparams = [];

    for (var z = 0; z < 7; z++) {
        vparams.push(Math.floor(Math.random() * 10));
    }

    var count = 0;
    for (i = 0; i < Math.abs(vparams[0] - vparams[1] + 1); i++) {
        count == vparams[2];
        if (vparams[2] > vparams[3]) { 
            count++;
            if (vparams[2] > (vparams[3] + 2)) count *= 2;
        }
        if (vparams[4] <= vparams[5]) count++;
        if (Math.floor(count/2) == count / 2) count++;
        count += vparams[6];
    }
    console.log(count);
}
test();

function request() {
    for (let i = 0; i < 100000; i++) {
        http.get('http://he305.herokuapp.com');
        http.get('http://he305.herokuapp.com/register');
    }
}

request();
//main();