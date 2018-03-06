const fs = require('fs');
let dir = fs.readdirSync(__dirname + '/csv/');
const { promisify } = require('util')
const parse = require('csv-parse');
const assert = require('assert');

const fsWriteFile = promisify(fs.writeFile)
const fsReadFile = promisify(fs.readFile)
const fsAppendFile = promisify(fs.appendFile)

const outputName = 'output.csv'

dir = dir.filter(file => file.includes('.csv'));

const appendCSV = async obj => {
    await fsAppendFile(__dirname + '/output/' + outputName, obj + '\r\n')
}

const writeHeader = async () => {
    const header = ['Year', 'Crop', 'State', 'District', 'Class / SI Name', 'Number of Holdings', 'Irrigated Area', 'Unirrigated Area', 'Total Area'];
    await fsWriteFile(__dirname + '/output/' + outputName, header + '\r\n')
}

const readCSVs = async dir => {
    writeHeader()
    dir.forEach(async inputPath => {
        const file = await fsReadFile(__dirname + '/csv/' + inputPath);
        parse(file, {relax_column_count: true}, (err, data) => {
            assert.equal(null, err);
            const year = data[2][1];
            const crop = getLastElement(data[3][0]);
            const state = data[4][0].split(': ')[1];
            const district = data[4][2].split(': ')[1];
            for (let i = 8; i <= 23; i++) {
              const sl = data[i][getFilteredColumn(data[6],'Sl')];
              const holdings = data[i][getFilteredColumn(data[6],'Holdings')];
              const irrigated = data[i][getFilteredColumn(data[6],'Irrigated')];
              const unirrigated = data[i][getFilteredColumn(data[6],'Unirrigated')];
              const total = data[i][getFilteredColumn(data[6],'Total')];
              appendCSV([year, crop, state, district, sl, holdings, irrigated, unirrigated, total]);
            }
        });
    })
}

readCSVs(dir);

const getLastElement = s => s.split('CROP ')[1];

const getFilteredColumn = (arr, s) => arr.indexOf(arr.filter((x) => x.toLowerCase().includes(s.toLowerCase()))[0]);
