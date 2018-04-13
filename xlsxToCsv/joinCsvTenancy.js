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
    'Partly owned, Partly Leased-in and Partly Otherwise Operated Holdings (Total Area)'
  ]
  await fsWriteFile(__dirname + '/output/' + outputName, header + '\r\n')
}

const readCSVs = async dir => {
  writeHeader()
  dir.forEach(async inputPath => {
    const file = await fsReadFile(__dirname + '/csv/' + inputPath)
    parse(file, { relax_column_count: true }, (err, data) => {
      assert.equal(null, err)
      console.log(data)
      return
      try {
        const year = data[2][6]
        const crop = 
      }
      catch (e) {
        console.log('invalid spreadsheets!: ', inputPath)
      }
    })
  })
}

readCSVs(dir)
