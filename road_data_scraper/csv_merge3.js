// Script for merging section 3 (Phasewise Summary)

const fs = require('fs')
let dir = fs.readdirSync(__dirname + '/output/')
const { promisify } = require('util')
const parse = require('csv-parse')
const assert = require('assert')

const fsWriteFile = promisify(fs.writeFile)
const fsReadFile = promisify(fs.readFile)

const outputName = 'Phasewise Summary.csv'
const stream = fs.createWriteStream(__dirname + '/' + outputName, { flags: 'a' })

const writeHeader = async () => {
  const header = [
    'District',
    'State',
    'Year',
    'Total Value of Projects [Roads + LSB] (Rs. in Lacs)',
    'Net No. of Road Works',
    'Total Value of Road Works (Rs. in Lacs)',
    'Total No. of Habitations Covered',
    'Total length of Road Works (in Km)',
    'Total No. of LSB Works',
    'Total value of LSB Works (Rs. in Lacs)',
    'Net length of LSB Works (in Mts)',
    'Total No of Dropped Works',
    'Net No. of Road Works',
    'Total No. of Habitations Benefitted',
    'Total Length of Road Works Completed (in Kms.)',
    'Balance Length of Road Work to be Completed (in Kms)',
    'Total No. of LSB Works',
    'Net length of LSB Works (in Mts)',
    'From ACcounts (Rs. in Lacs) (Roads + LSB)'
  ]
  stream.write(header + '\r\n')
}

const readCSVs = async dir => {
  writeHeader()
  dir.forEach(async inputPath => {
    const file = await fsReadFile(__dirname + '/output/' + inputPath)
    parse(file, { relax_column_count: true }, (err, data) => {
      assert.equal(null, err) // check for errors
      try {
        let splitIndex = inputPath.indexOf('-');
        const state = inputPath.slice(0,splitIndex).trim();
        const district = inputPath.slice(splitIndex + 1).split('.csv')[0].trim();

        // TODO get number of lines and figure out number of years 

        for (let i = 0; i <= 18; i++) {
          const years = (2000 + i).toString() + '-' + (2000 + i + 1).toString()

          const nc1000 = data[habitationsCoveredStartIndex + i*2][1]
          const u1000  = data[habitationsCoveredStartIndex + i*2 + 1][1]
          const nc999  = data[habitationsCoveredStartIndex + i*2][2]
          const u999   = data[habitationsCoveredStartIndex + i*2 + 1][2]

          const ncE499 = data[habitationsCoveredStartIndex + i*2][3]
          const uE499  = data[habitationsCoveredStartIndex + i*2 + 1][3]
          const ncTE = data[habitationsCoveredStartIndex + i*2][4]
          const uTE  = data[habitationsCoveredStartIndex + i*2 + 1][4]

          const ncT499 = data[habitationsCoveredStartIndex + i*2][5]
          const uT499  = data[habitationsCoveredStartIndex + i*2 + 1][5]
          const ncE249 = data[habitationsCoveredStartIndex + i*2][6]
          const uE249  = data[habitationsCoveredStartIndex + i*2 + 1][6]

          const ncL250 = data[habitationsCoveredStartIndex + i*2][7]
          const uL250  = data[habitationsCoveredStartIndex + i*2 + 1][7]
          const ncGT = data[habitationsCoveredStartIndex + i*2][8]
          const uGT  = data[habitationsCoveredStartIndex + i*2 + 1][8]
          
          stream.write([state, district, years, 
            nc1000, u1000, nc999, u999,
            ncE499, uE499, ncTE, uTE,
            ncT499, uT499, ncE249, uE249,
            ncL250, uL250, ncGT, uGT].concat(
              TotalNumberOfHabitationsEnteredAsOn01042000,
              TotalNumberOfHabitationsEntered,
              TotalNumberOfConnectedHabitationsAsOn01042000,
              TotalNumberOfConnectedHabitationsEntered,
              TotalNumberOfUnConnectedHabitations01042000,
              TotalNumberOfUnConnectedHabitationsEntered,
              StatusOfConnectivityUnderStateScheme,
              NoOfUnconnectedHabitations
            ) + '\r\n')
        };
      }
      catch (e) {
        console.log('Error parsing ' + inputPath + '\n' + e)
      }
    })
  })
}

dir = dir.filter(file => file.includes('.csv'))
readCSVs(dir)