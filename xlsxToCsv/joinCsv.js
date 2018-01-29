const fs = require('fs')
let dir = fs.readdirSync(__dirname + '/dataCsv/')
const parse = require('csv-parse')
const assert = require('assert')

dir = dir.filter(file => file.includes('.csv'))

dir.forEach(inputPath => {
  fs.readFile(__dirname + '/dataCsv/' + inputPath, (err, fileData) => {
    assert.equal(null, err)
    parse(fileData, {from: 3, columns: true, relax_column_count: true}, (err, data) => {
      assert.equal(null, err)
      console.log(data)
    })
  })
})
