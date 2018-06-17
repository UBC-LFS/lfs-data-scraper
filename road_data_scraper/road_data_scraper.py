from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import time
import csv

driver = webdriver.Chrome()
driver.implicitly_wait(5) 
driver.get('http://omms.nic.in/')

completed_road_works_button = driver.find_element_by_css_selector("div.small-box.bg-red > a")
completed_road_works_button.click()

# Select a state
state_select = Select(driver.find_element_by_css_selector("select[title='State']"))
state_options = state_select.options
for i in range(1, len(state_options)):
  state_select.select_by_index(i)

  # For each state, select a district
  district_select = Select(driver.find_element_by_css_selector("select#ddlSPDistrict"))
  district_options = district_select.options

  for j in range(1, len(district_options)):
    district_select.select_by_index(j)

    # Select all option for Collboration and Agency
    Select(driver.find_element_by_css_selector("select[name='Collaboration']")).select_by_index(0)
    Select(driver.find_element_by_css_selector("select[name='Agency']")).select_by_index(0)

    view_details_button = driver.find_element_by_css_selector("input#btnViewSPDetails")
    time.sleep(1)
    view_details_button.click()
    time.sleep(2) # wait until data has loaded

    # Create csv file
    state_name = state_select.first_selected_option.text
    district_name = district_select.first_selected_option.text
    file_name = state_name + ' ' + district_name + '.csv'

    with open(file_name, 'w', newline='') as csvfile:
      wr = csv.writer(csvfile)
      
      # 1. Status of Connectivity
      table_1 = driver.find_element_by_css_selector("div#divContentSPConnStat").find_element_by_tag_name("table")
      for row in table_1.find_elements_by_css_selector('tr'):
        wr.writerow([d.text for d in row.find_elements_by_css_selector('*')]) # TODO select th or td

      # 2. Status of Executing Machinery
      table_2 = driver.find_element_by_css_selector("div#divContentSPExecOfficers").find_element_by_tag_name("table")
      for row in table_2.find_elements_by_css_selector('tr'):
        wr.writerow([d.text for d in row.find_elements_by_css_selector('td')]) 

      # 3. Phasewise Summary
      table_3 = driver.find_element_by_css_selector("div#divContentSPPhaseSummary").find_element_by_tag_name("table")
      for row in table_3.find_elements_by_css_selector('tr'):
        wr.writerow([d.text for d in row.find_elements_by_css_selector('*')])
        



