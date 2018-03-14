const puppeteer = require('puppeteer')
const yearSelector = '_ctl0_ContentPlaceHolder1_ddlYear'
const socialGroupSelector = '_ctl0_ContentPlaceHolder1_ddlSocialGroup'
const stateSelector = '_ctl0_ContentPlaceHolder1_ddlState'
const districtSelector = '_ctl0_ContentPlaceHolder1_ddlDistrict'
const tablesSelector = '_ctl0_ContentPlaceHolder1_ddlTables'
const cropSelector = '_ctl0_ContentPlaceHolder1_ddlCrop'
const submitForm = '#_ctl0_ContentPlaceHolder1_btnSubmit'
const excelDownload = '#ReportViewer1__ctl5__ctl4__ctl0_Menu > div:nth-child(5) > a';

(async () => {
  const browser = await puppeteer.launch({
    headless: false
  })

  const downloadPage = async () => {
    const page = await browser.newPage()
    page.on('console', msg => console.log('PAGE LOG:', msg.text()))
    await page.goto('http://agcensus.dacnet.nic.in/DistCharacteristic.aspx')
    await page._client.send('Page.setDownloadBehavior', {behavior: 'allow', downloadPath: './'})

    const getOptions = (page, selector) => page.evaluate(sel => {
      const children = document.getElementById(sel).children
      const options = Array.from(children).map(x => x.value)
      console.log(options)
      return options
    }, selector)

    const setSelectVal = async (sel, val) =>
      page.evaluate(data =>
        (document.getElementById(data.sel).value = data.val), { sel, val })

    // const year = await page.select('#_ctl0_ContentPlaceHolder1_ddlYear')
    const yearOptions = await getOptions(page, yearSelector)
    await setSelectVal(yearSelector, yearOptions[2])

    const stateOptions = await getOptions(page, stateSelector)
    await setSelectVal(stateSelector, stateOptions[0])

    const tablesOptions = await getOptions(page, tablesSelector)
    await setSelectVal(tablesSelector, tablesOptions[0])

    await Promise.all([
      page.click(submitForm),
      page.waitForNavigation()
    ])

    await page.evaluate(btn => {
      document.querySelector(btn).click()
    }, excelDownload)
    return page.close()
  }

  let numberOfPages = 7
  while (numberOfPages > 0) {
    downloadPage()
    numberOfPages--
  }
  // setInterval(function () { downloadPage() }, 5000)
})()
