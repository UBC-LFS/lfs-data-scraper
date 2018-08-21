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
    'From Accounts (Rs. in Lacs) (Roads + LSB)'
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

        const numberOfLines = data.length
        const numberOfYears = numberOfLines - 5
        
        for(let i = 0; i < numberOfYears; ++i) {
          // data starts from row 2
          stream.write([state, district].concat(data[i+2]) + '\r\n')
        }
      }
      catch (e) {
        console.log('Error parsing ' + inputPath + '\n' + e)
      }
    })
  })
}

dir = dir.filter(file => file.includes('.csv'))
readCSVs(dir)