const fs = require('fs')
let dir = fs.readdirSync(__dirname + '/csv/')
const { promisify } = require('util')
const parse = require('csv-parse')
const assert = require('assert')

const fsWriteFile = promisify(fs.writeFile)
const fsReadFile = promisify(fs.readFile)
const outputName = 'output.csv'
const stream = fs.createWriteStream(__dirname + '/output/' + outputName, { flags: 'a' })

dir = dir.filter(file => file.includes('.csv'))

const writeHeader = async () => {
  const header = [
    'Year',
    'State',
    'District',
    'SI No',
    'Size Class (HA)',
    'Total Holdings (Number)',
    'Total Holdings (Area)',
    'Wholly Owned and Self Operated Holdings (Number)',
    'Wholly Owned and Self Operated Holdings (Area)',
    'Wholly Leased-In Holdings (Number)',
    'Wholly Leased-In Holdings (Area)',
    'Wholly Otherwise Operated Holdings (Number)',
    'Wholly Otherwise Operated Holdings (Area)',
    'Partly owned, Partly Leased-in and Partly Otherwise Operated Holdings (Number)',
    'Partly owned, Partly Leased-in and Partly Otherwise Operated Holdings (Owned Area)',
    'Partly owned, Partly Leased-in and Partly Otherwise Operated Holdings (Leased-in Area)',
    'Partly owned, Partly Leased-in and Partly Otherwise Operated Holdings (Otherwise Operated Area)',
    'Partly owned, Partly Leased-in and Partly Otherwise Operated Holdings (Total Area)', 
    'File Name'
  ]
  await fsWriteFile(__dirname + '/output/' + outputName, header + '\r\n')
}

const readCSVs = async dir => {
  writeHeader()
  dir.forEach(async inputPath => {
    const file = await fsReadFile(__dirname + '/csv/' + inputPath)
    parse(file, { relax_column_count: true }, (err, data) => {
      assert.equal(null, err)
      try {
        const year = data[1][6]
        const state = data[3][0].split(': ')[1]
        const district = data[3][5].split(': ')[1]
        for (let i = 8; i <= 23; i++) {
          stream.write([
            year,
            state,
            district,
            data[i][0],
            data[i][1],
            data[i][2],
            data[i][3],
            data[i][4],
            data[i][5],
            data[i][6],
            data[i][7],
            data[i][8],
            data[i][9],
            data[i][10],
            data[i][11],
            data[i][12],
            data[i][13],
            data[i][14],
            inputPath
          ] + '\r\n')
        }
      }
      catch (e) {
        console.log('invalid spreadsheets!: ', inputPath)
      }
    })
  })
}

readCSVs(dir)
