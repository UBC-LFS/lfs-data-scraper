const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: false
  })
  const page1 = await browser.newPage()
  page1.on('console', msg => console.log('PAGE LOG:', msg.text()))
  await page1.goto('http://agcensus.dacnet.nic.in/DistCharacteristic.aspx')

  // const page2 = await browser.newPage()
  // await page2.goto('http://agcensus.dacnet.nic.in/DistCharacteristic.aspx')

  const yearSelector = '_ctl0_ContentPlaceHolder1_ddlYear'
  const socialGroupSelector = '_ctl0_ContentPlaceHolder1_ddlSocialGroup'
  const stateSelector = '_ctl0_ContentPlaceHolder1_ddlState'
  const districtSelector = '_ctl0_ContentPlaceHolder1_ddlDistrict'
  const tablesSelector = '_ctl0_ContentPlaceHolder1_ddlTables'
  const cropSelector = '_ctl0_ContentPlaceHolder1_ddlCrop'

  // const year = await page1.select('#_ctl0_ContentPlaceHolder1_ddlYear')
  await page1.evaluate(() => {
    document.getElementById('_ctl0_ContentPlaceHolder1_ddlYear').selectedIndex = 3
  })

  await page1.evaluate(() => {
    document.getElementById('_ctl0_ContentPlaceHolder1_ddlTables').selectedIndex = 7
  })

  await page1.click('#_ctl0_ContentPlaceHolder1_btnSubmit')
})()
