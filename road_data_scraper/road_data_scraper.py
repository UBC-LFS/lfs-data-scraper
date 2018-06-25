import time
import csv
import os
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

def main():
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
      time.sleep(3)
      view_details_button.click()
      time.sleep(3) # wait until data has loaded

      # Create csv file
      directory_name = 'output'
      if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        
      state_name = state_select.first_selected_option.text
      district_name = district_select.first_selected_option.text
      print('\n')
      print(state_name + '+' + district_name)

      file_name = state_name + ' ' + district_name + '.csv'

      def create_csv_file(file_name):
        with open(directory_name + '/' + file_name, 'w', newline='') as csvfile:
          wr = csv.writer(csvfile)
          
          # 1. Status of Connectivity
          table_1 = driver.find_element_by_css_selector("div#divContentSPConnStat").find_element_by_tag_name("table")
          for row in table_1.find_elements_by_css_selector('tr'):
            wr.writerow([d.text for d in row.find_elements_by_css_selector('*')]) 

          # Write empty row
          wr.writerow([])

          # 2. Status of Executing Machinery
          table_2 = driver.find_element_by_css_selector("div#divContentSPExecOfficers").find_element_by_tag_name("table")
          for row in table_2.find_elements_by_css_selector('tr'):
            wr.writerow([d.text for d in row.find_elements_by_css_selector('td')]) 

          # Write empty row
          wr.writerow([])

          # 3. Phasewise Summary
          table_3 = driver.find_element_by_css_selector("div#divContentSPPhaseSummary").find_element_by_tag_name("table")
          for row in table_3.find_elements_by_css_selector('tr'):
            wr.writerow([d.text for d in row.find_elements_by_css_selector('*')])
            
          # Write empty row
          wr.writerow([])

          # 4. Batchwise Summary (there's an arbitrary number of tables for different years)
          batchwise_tables = driver.find_elements_by_css_selector('div.box.box-warning.collapsed-box')
          for element in batchwise_tables:
            batchwise_table_title = element.text
            wr.writerow([batchwise_table_title])
            dropdown_button = element.find_element_by_css_selector('div.box-tools.pull-right').find_element_by_tag_name('button')
            dropdown_button.click()
            time.sleep(3)

            # Get table for each year
            year = re.search(r"[0-9]{4}", batchwise_table_title).group(0)
            batchwise_table = element.find_element_by_css_selector('div#divContentSPPhaseSummaryYear' + year)

            for row in batchwise_table.find_elements_by_css_selector('tr'):
              wr.writerow([d.text for d in row.find_elements_by_css_selector('*')]) # TODO select th or td
          
          # Quality Control Monitoring by 2nd Tier
          try:
            table_qc2 = driver.find_element_by_css_selector("div#divContentSP2TierQM").find_element_by_tag_name("table")
            for row in table_qc2.find_elements_by_css_selector('tr'):
              wr.writerow([d.text for d in row.find_elements_by_css_selector('*')]) # TODO select th or td
          except NoSuchElementException:
            print('no qc2 table found')

          # Quality Control Monitoring by 3rd Tier
          try: 
            table_qc3 = driver.find_element_by_css_selector("div#divContentSP3TierQM").find_element_by_tag_name("table")
            for row in table_qc3.find_elements_by_css_selector('tr'):
              wr.writerow([d.text for d in row.find_elements_by_css_selector('*')]) # TODO select th or td
          except NoSuchElementException:
            print('no qc3 table found')
        return True

      create_csv_file(file_name)

  print('Successfully finished')


if __name__ == "__main__":
  main()
      



