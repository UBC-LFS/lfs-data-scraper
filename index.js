const request = require('request')
const cheerio = require('cheerio')
const assert = require('assert')

const url = 'http://inputsurvey.dacnet.nic.in/districttables.aspx'
request(url, (error, response, html) => {
  assert.equal(null, error)
  const $ = cheerio.load(html)

  const yearSelector = $('#_ctl0_ContentPlaceHolder2_ddlYear')
  const statesSelector = $('#_ctl0_ContentPlaceHolder2_ddlStates')
  const districtSelector = $('#_ctl0_ContentPlaceHolder2_ddldistrict')
  const tableSelector = $('#_ctl0_ContentPlaceHolder2_ddlTables')

  const temp = ['1', 'Table1-Parcels per holding & Area per parcel', '1', 'ANDAMAN', '23a', 'A & N ISLANDS', '1996', '1996-1997']
  const postData = JSON.stringify({ values: temp })
  request.post({
    url: 'http://inputsurvey.dacnet.nic.in/districttables.aspx/FillSession',
    data: postData,
    dataType: 'JSON',
    type: 'post',
    async: false,
    contentType: "application/json; charset=utf-8"
  }, (err, httpResponse, body) => {
    console.log(httpResponse)
  })
})
