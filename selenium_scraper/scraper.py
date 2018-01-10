from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://agcensus.dacnet.nic.in/tehsilsummarytype.aspx")
elem = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_btnSubmit")
elem.click()
driver.close()