const fs = require('fs')
let dir = fs.readdirSync(__dirname + '/output/')
const { promisify } = require('util')
const parse = require('csv-parse')
const assert = require('assert')

const fsWriteFile = promisify(fs.writeFile)
const fsReadFile = promisify(fs.readFile)
const outputName = 'Status of Connectivity.csv'
const stream = fs.createWriteStream(__dirname + '/output/' + outputName, { flags: 'a' })

const writeHeader = async () => {
  const header = [
    'District',
    'State',
    'Year',
    'New Connectivity (1000+)',
    'Upgradation (1000+)',
    'New Connectivity (999-500)',
    'Upgradation (999-500)',
    'New Connectivity (Eligible 499 - 250)',
    'Upgradation (Eligible 499 -250)',
    'New Connectivity (Total Eligible)',
    'Upgradation (Total Eligible)',
    'New Connectivity (Total 499-250)',
    'Upgradation (Total 499-250)',
    'New Connectivity (Eligible 249-100)',
    'Upgradation (Eligible 249-100)',
    'New Connectivity (Less Than 250)',
    'Upgradation (Less Than 250)',
    'New Connectivity (Grand Total)',
    'Upgradation (Grand Total)',
    'Total number of Habitations (As on 01-04-2000) (1000+)',
    'Total Number of Habitations (As on 01-04-2000) (999-500)',
    'Total Number of Habitations (As on 01-04-2000) (499-250)',
    'Total Number of Habitations (As on 01-04-2000) (Eligible 499-250)',
    'Total Number of Habitations (As on 01-04-2000) (Total Eligible)',
    'Total Number of Habitations (As on 01-04-2000) (Total 499-250)',
    'Total Number of Habitations (As on 01-04-2000) (Eligible 249-100)',
    'Total Number of Habitations (As on 01-04-2000) (Less Than 250)',
    'Total Number of Habitations (As on 01-04-2000) (Grand Total)',
    'Total Number of Habitations Entered (1000+)',
    'Total Number of Habitations Entered (999-500)',
    'Total Number of Habitations Entered (Eligible 499-250)',
    'Total Number of Habitations Entered (Total Eligible)',
    'Total Number of Habitations Entered (Total 499-250)',
    'Total Number of Habitations Entered (Eligible 249-100)',
    'Total Number of Habitations Entered (Less Than 250)',
    'Total Number of Habitations Entered (Grand Total)',
    'Total Number of Connected Habitations (As on 01-04-2000) (1000+)',
    'Total Number of Connected Habitations (As on 01-04-2000) (999-500)',
    'Total Number of Connected Habitations (As on 01-04-2000) (Eligible 499-250)',
    'Total Number of Connected Habitations (As on 01-04-2000) (Total Eligible)',
    'Total Number of Connected Habitations (As on 01-04-2000) (Total 499 - 250)',
    'Total Number of Connected Habitations (As on 01-04-2000) (Eligible 249 - 100)',
    'Total Number of Connected Habitations (As on 01-04-2000) (Less Than 250)',
    'Total Number of Connected Habitations (As on 01-04-2000) (Grand Total)',
    'Total Number of Connected Habitations Entered (1000+)',
    'Total Number of Connected Habitations Entered (999 - 500)',
    'Total Number of Connected Habitations Entered (Eligible 499 - 250)',
    'Total Number of Connected Habitations Entered (Total Eligible)',
    'Total Number of Connected Habitations Entered (Total 499 - 250)',
    'Total Number of Connected Habitations Entered (Eligible 249 - 100',
    'Total Number of Connected Habitations Entered (Less Than 250)',
    'Total Number of Connected Habitations Entered (Grand Total)',
    'Total Number of Unconnected Habitations (As on 01-04-2000) (1000+',
    'Total Number of Unconnected Habitations (As on 01-04-2000) (999 - 500)',
    'Total Number of Unconnected Habitations (As on 01-04-2000) (Eligible 499 - 250)',
    'Total Number of Unconnected Habitations (As on 01-04-2000) (Total Eligible)',
    'Total Number of Unconnected Habitations (As on 01-04-2000) (Total 499 - 250)',
    'Total Number of Unconnected Habitations (As on 01-04-2000) (Eligible 249 - 100)',
    'Total Number of Unconnected Habitations (As on 01-04-2000) (Less Than 250)',
    'Total Number of Unconnected Habitations (As on 01-04-2000) (Grand Total)',
    'Total Number of Unconnected Habitations Entered (1000+)',
    'Total Number of Unconnected Habitations Entered (999 - 500)',
    'Total Number of Unconnected Habitations Entered (Eligible 499 - 250)',
    'Total Number of Unconnected Habitations Entered (Total Eligible)',
    'Total Number of Unconnected Habitations Entered (Total 499 - 250',
    'Total Number of Unconnected Habitations Entered (Eligible 249 - 100)',
    'Total Number of Unconnected Habitations Entered (Less Than 250)',
    'Total Number of Unconnected Habitations Entered (Grand Total)',
    'Status of Connectivity of Habitations covered under State Scheme (1000+)',
    'Status of Connectivity of Habitations covered under State Scheme (999 - 500)',
    'Status of Connectivity of Habitations covered under State Scheme (Eligible 499 - 250)',
    'Status of Connectivity of Habitations covered under State Scheme (Total Eligible)',
    'Status of Connectivity of Habitations covered under State Scheme (Total 499 - 250)',
    'Status of Connectivity of Habitations covered under State Scheme (Eligible 249 - 100)',
    'Status of Connectivity of Habitations covered under State Scheme (Less Than 250)',
    'Status of Connectivity of Habitations covered under State Scheme (Grand Total)',
    'No of Unconnected Habs after deducting Habs benefitted under State Programme (1000+)	',
    'No of Unconnected Habs after deducting Habs benefitted under State Programme (999 - 500)',
    'No of Unconnected Habs after deducting Habs benefitted under State Programme (Eligible 499 - 250)',
    'No of Unconnected Habs after deducting Habs benefitted under State Programme (Total Eligible)',
    'No of Unconnected Habs after deducting Habs benefitted under State Programme (Total 499 - 250)',
    'No of Unconnected Habs after deducting Habs benefitted under State Programme (Eligible 249 - 100)',
    'No of Unconnected Habs after deducting Habs benefitted under State Programme (Less Than 250)',
    'No of Unconnected Habs after deducting Habs benefitted under State Programme (Grand Total)',
  ]
  await fsWriteFile(__dirname + '/output/' + outputName, header + '\r\n')
}

const readCSVs = async dir => {
  writeHeader()
  // dir.forEach(async inputPath => {
  //   const file = await fsReadFile(__dirname + '/csv/' + inputPath)
  //   parse(file, { relax_column_count: true }, (err, data) => {
  //     assert.equal(null, err)
  //     try {
  //       const year = data[2][1]
  //       const crop = getLastElement(data[3][0])
  //       const state = data[4][0].split(': ')[1]
  //       const district = data[4][2].split(': ')[1]
  //       for (let i = 8; i <= 23; i++) {
  //         const sl = data[i][getFilteredColumn(data[6], 'Sl')]
  //         const holdings = data[i][getFilteredColumn(data[6], 'Holdings')]
  //         const irrigated = data[i][getFilteredColumn(data[6], 'Irrigated')]
  //         const unirrigated = data[i][getFilteredColumn(data[6], 'Unirrigated')]
  //         const total = data[i][getFilteredColumn(data[6], 'Total')]
  //         stream.write([year, crop, state, district, sl, holdings, irrigated, unirrigated, total, inputPath] + '\r\n')
  //       };
  //     }
  //     catch (e) {
  //       console.log('invalid spreadsheets!: ', inputPath)
  //     }
  //   })
  // })
}

dir = dir.filter(file => file.includes('.csv'))
console.log(dir)
readCSVs(dir)


