let fs = require("fs");
let dir = fs.readdirSync(__dirname + '/dataCsv/');
let csv = require('csv');
var parse = require('csv-parse');
require('should');
dir = dir.filter(function (a) {
    return a.includes('.csv');
});

dir.forEach(function (inputPath) {
    fs.readFile(__dirname + '/dataCsv/' + inputPath, function (err, fileData) {
        parse(fileData, {from: 3, columns: true, relax_column_count: true}, function (data) {
            console.log(data)
        });
    })
});
