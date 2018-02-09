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
        finalData.class.push(data[i][getFilteredColumn(data[6],'Sl')]);
        finalData.numberOfHoldings.push(data[i][getFilteredColumn(data[6],'Holdings')]);
        finalData.irrigatedArea.push(data[i][getFilteredColumn(data[6],'Irrigated')]);
        finalData.UnirrigatedArea.push(data[i][getFilteredColumn(data[6],'Unirrigated')]);
        finalData.totalArea.push(data[i][getFilteredColumn(data[6],'Total')]);
      }
    })
  })
});

const getLastElement = (s) => s.split('CROP ')[1];

const getFilteredColumn = (arr, s) => arr.indexOf(arr.filter((x) => x.includes(s))[0]);
