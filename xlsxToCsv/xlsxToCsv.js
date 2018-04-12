const fs = require('fs')
const xlsx = require('node-xlsx')
let dir = fs.readdirSync(__dirname + '/xlsx/Archive/')

// filter out .xlsx files
dir = dir.filter(file => file.includes('.xlsx'))

dir.forEach(file => {
  const xlsxObj = xlsx.parse(__dirname + '/xlsx/Archive/' + file)
  let rows = []
  xlsxObj.map(sheet => {
    // loop through all rows in the sheet and extract it
    sheet.data.map(row => rows.push(row))
    let writeStr = ''
    rows.map(s => (writeStr += s.join(',') + '\n'))
    fs.writeFile(__dirname + '/csv/' + file.split('.')[0] + '.csv', writeStr, err => {
      if (err) {
        console.log(err)
      }
    })
  })
})
