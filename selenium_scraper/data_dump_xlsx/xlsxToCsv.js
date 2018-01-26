let fs = require("fs");
let xlsx = require("node-xlsx");
let dir = fs.readdirSync(__dirname);

// filter out .xlsx files
dir = dir.filter(function (a) {
    return a.includes('.xlsx');
});


dir.forEach(function(file) {
    let xlsxObj = xlsx.parse(__dirname + '/' + file);
    let rows = [];
    xlsxObj.map(function (sheet) {
        //loop through all rows in the sheet and extract it
        sheet.data.map(function(j) {
            rows.push(j);
        });
        let writeStr = '';
        rows.map(function (s) {
            writeStr += s.join(',') + '\n';
        });
        fs.writeFile(__dirname + '/' + file.split('.')[0] + '.csv', writeStr, function (err) {
            if (err) {
                return console.log(err);
            }
            console.log(file + " was saved in the current directory!");
        });
    })
});
