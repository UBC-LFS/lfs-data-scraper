const request = require('request')
const cheerio = require('cheerio')
const assert = require('assert')

const url = 'http://inputsurvey.dacnet.nic.in/districttables.aspx'
request(url, (error, response, html) => {
  assert.equal(null, error)
  const $ = cheerio.load(html)
  console.log($)
})
