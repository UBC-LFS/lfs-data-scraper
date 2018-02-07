const fs = require('fs')
let dir = fs.readdirSync(__dirname + '/dataCsv/');
const parse = require('csv-parse');
const assert = require('assert');

dir = dir.filter(file => file.includes('.csv'));

dir.forEach(inputPath => {
    let finalData = {
        year: '',
        crop: '',
        state: '',
        district: '',
        class: [],
        numberOfHoldings: [],
        irrigatedArea: [],
        UnirrigatedArea: [],
        totalArea: [],
    };
  fs.readFile(__dirname + '/dataCsv/' + inputPath, (err, fileData) => {
    assert.equal(null, err);
    parse(fileData, {relax_column_count: true}, (err, data) => {
      assert.equal(null, err);
      finalData.year = data[2][1];
      finalData.crop = getLastElement(data[3][0]);
      finalData.state = getLastElement(data[0][0]);
      finalData.district = getLastElement(data[2][0]);
      for (let i = 8; i <= 23; i++) {
          finalData.class.push(data[i][data[6].indexOf('Sl No')]);
        finalData.numberOfHoldings.push(data[i][data[6].indexOf('No. of Holdings')]);
        finalData.irrigatedArea.push(data[i][data[6].indexOf('Irrigated Area')]);
        finalData.UnirrigatedArea.push(data[i][data[6].indexOf('Unirrigated Area ')]);
        finalData.totalArea.push(data[i][data[6].indexOf('Total Area')]);
      }
    })
  })
});

const getLastElement = (s) => s.split('CROP ')[1];
