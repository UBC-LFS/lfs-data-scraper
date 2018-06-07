from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome('C:/Users/Jeong/Downloads/chromedriver_win32/chromedriver.exe') # PATH TO DRIVER
driver.implicitly_wait(5) # seconds

driver.get('http://omms.nic.in/')

completed_road_works_button = driver.find_element_by_css_selector("div.small-box.bg-red > a")
completed_road_works_button.click()

# select a state
state_select = Select(driver.find_element_by_css_selector("select[title='State']"))
state_options = state_select.options
for i in range(1, len(state_options)):
  state_select.select_by_index(i)

  # for each state, select a district
  district_select = Select(driver.find_element_by_css_selector("select#ddlSPDistrict"))
  district_options = district_select.options
  print(len(district_options))

  for j in range(1, len(district_options)):
    district_select.select_by_index(j)

    # Select all option for Collboration and Agency
    Select(driver.find_element_by_css_selector("select[name='Collaboration']")).select_by_index(0)
    Select(driver.find_element_by_css_selector("select[name='Agency']")).select_by_index(0)

    view_details_button = driver.find_element_by_css_selector("input#btnViewSPDetails")
    # view_details_button.click()

        



