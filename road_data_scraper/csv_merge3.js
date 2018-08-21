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
     
        // data repeated for each state + district (initially -1, changed to actual values if found in individual CSVs)
        let TotalNumberOfHabitationsEnteredAsOn01042000 = ['NA','NA','NA','NA','NA','NA','NA','NA']
        let TotalNumberOfHabitationsEntered = ['NA','NA','NA','NA','NA','NA','NA','NA']
        let TotalNumberOfConnectedHabitationsAsOn01042000 = ['NA','NA','NA','NA','NA','NA','NA','NA']
        let TotalNumberOfConnectedHabitationsEntered = ['NA','NA','NA','NA','NA','NA','NA','NA']
        
        let TotalNumberOfUnConnectedHabitations01042000 = ['NA','NA','NA','NA','NA','NA','NA','NA']
        let TotalNumberOfUnConnectedHabitationsEntered = ['NA','NA','NA','NA','NA','NA','NA','NA']
        let StatusOfConnectivityUnderStateScheme = ['NA','NA','NA','NA','NA','NA','NA','NA']
        let NoOfUnconnectedHabitations = ['NA','NA','NA','NA','NA','NA','NA','NA']

        for(let i = 0; i < data.length; i++) {
          if(data[i].length > 0 && data[i][0].includes('Total number of Habitations (As on 01-04-2000)')) {
            TotalNumberOfHabitationsEnteredAsOn01042000 = data[i].slice(1)
          } else if(data[i].length > 0 && data[i][0].includes('Total number of Habitations Entered')) {
            TotalNumberOfHabitationsEntered = data[i].slice(1)
          } else if(data[i].length > 0 && data[i][0].includes('Total number of Connected Habitations (As on 01-04-2000)')) {
            TotalNumberOfConnectedHabitationsAsOn01042000 = data[i].slice(1)
          } else if(data[i].length > 0 && data[i][0].includes('Total number of Connected Habitations Entered')) {
            TotalNumberOfConnectedHabitationsEntered = data[i].slice(1)
          } else if(data[i].length > 0 && data[i][0].includes('Total number of UnConnected Habitations (As on 01-04-2000)')) {
            TotalNumberOfUnConnectedHabitations01042000 = data[i].slice(1)
          } else if(data[i].length > 0 && data[i][0].includes('Total number of UnConnected Habitations Entered')) {
            TotalNumberOfUnConnectedHabitationsEntered = data[i].slice(1)
          } else if(data[i].length > 0 && data[i][0].includes('Status of connectivity of Habitations covered')) {
            StatusOfConnectivityUnderStateScheme = data[i].slice(1)
          } else if(data[i].length > 0 && data[i][0].includes('No of Unconnected Habs after deducting Habs')) {
            NoOfUnconnectedHabitations = data[i].slice(1)
          }
        }

        // find the start of the data for 'Habitations covered by PMGSY: 2xxx - 2xxx
        let habitationsCoveredStartIndex = 0;
        for(let i = 0; i < data.length; i++) {
          if(data[i].length > 0 && data[i][0].includes('Habitations covered by PMGSY: 2000')) {
            habitationsCoveredStartIndex = i;
            break;
          }
        }

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