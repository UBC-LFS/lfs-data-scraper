import time
import csv
import os
import re
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

def combine_csvs():
  # TODO
  return 0
  
def generate_csvs():
  start_time = time.time()

  driver = webdriver.Chrome()
  driver.implicitly_wait(5) 
  driver.get('http://omms.nic.in/')

  completed_road_works_button = driver.find_element_by_css_selector("div.small-box.bg-red > a")
  completed_road_works_button.click()

  # Select a state
  state_select = Select(driver.find_element_by_css_selector("select[title='State']"))
  state_options = state_select.options

  state_start_index = 1
  if len(sys.argv) > 1:
    state_start_index = int(sys.argv[1])

  for i in range(state_start_index, len(state_options)):
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
      file_name = state_name + ' - ' + district_name + '.csv'

      print('\n')
      print(file_name)
      print('i=' + str(i) + ' j=' + str(j))

      # Returns True if data scraping was successful, False otherwise
      def create_csv_file(file_name):
        with open(directory_name + '/' + file_name, 'w', newline='') as csvfile:
          wr = csv.writer(csvfile)
          
          # 1. Status of Connectivity
          try:
            table_1a = driver.find_element_by_css_selector("div#divContentSPConnStat").find_element_by_tag_name("table")
            for row in table_1a.find_elements_by_css_selector('tr'):
              wr.writerow([d.text for d in row.find_elements_by_css_selector('th,td')]) 
          except StaleElementReferenceException:
            csvfile.truncate(0)
            print('StaleElementReferenceException thrown, trying again')
            return False
          except NoSuchElementException:
            print('no status of connectivity table found')
            pass

          try:
            table_1b = driver.find_element_by_css_selector("div#divContentSPHabCoverage").find_element_by_tag_name("table").find_element_by_tag_name("tbody")
            # grab habitation years, use it as column name for 2 iterations  
            habitation_years_name = None

            for row in table_1b.find_elements_by_xpath('./tr'):
              habitation_coverage_row = []
              for d in row.find_elements_by_xpath('./td'):
                if d.text.strip().startswith('Habitations'): # grab habitation years
                  habitation_years_name = d.text.strip()
                elif not re.search(r'\d', d.text): # not a number
                  habitation_coverage_row.append(habitation_years_name + ' ' + d.text)
                else: # number
                  habitation_coverage_row.append(d.text)
              wr.writerow(habitation_coverage_row) 

          except StaleElementReferenceException:
            csvfile.truncate(0)
            print('StaleElementReferenceException thrown, trying again')
            return False
          except NoSuchElementException:
            print('no status of connectivity table found')
            pass

          # Write empty row
          wr.writerow([])

          # 2. Status of Executing Machinery
          try:
            table_2 = driver.find_element_by_css_selector("div#divContentSPExecOfficers").find_element_by_tag_name("table")
            for row in table_2.find_elements_by_css_selector('tr'):
              wr.writerow([d.text for d in row.find_elements_by_css_selector('th,td')]) 
          except StaleElementReferenceException:
            csvfile.truncate(0)
            print('StaleElementReferenceException thrown, trying again')
            return False
          except NoSuchElementException:
            print('no status of executing machinery table found')
            pass

          # Write empty row
          wr.writerow([])

          # 3. Phasewise Summary
          try:
            table_3 = driver.find_element_by_css_selector("div#divContentSPPhaseSummary").find_element_by_tag_name("table")
            for row in table_3.find_elements_by_css_selector('tr'):
              wr.writerow([d.text for d in row.find_elements_by_css_selector('th,td')])
          except StaleElementReferenceException:
            csvfile.truncate(0)
            print('StaleElementReferenceException thrown, trying again')
            return False
          except NoSuchElementException:
            print('no phasewise summary found')
            pass
            
          # Write empty row
          wr.writerow([])

          # 4. Batchwise Summary (there's an arbitrary number of tables for different years)
          try:
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

              try:
                for row in batchwise_table.find_elements_by_css_selector('tr'):
                  wr.writerow([d.text for d in row.find_elements_by_css_selector('th,td')]) 
                
                # Write empty row
                wr.writerow([])
              except StaleElementReferenceException:
                csvfile.truncate(0)
                print('StaleElementReferenceException thrown, trying again')
                return False
          except NoSuchElementException:
            print('no batchwise summary table found')
            pass

          # Write empty row
          wr.writerow([])
          
          # Quality Control Monitoring by 2nd Tier
          try:
            table_qc2 = driver.find_element_by_css_selector("div#divContentSP2TierQM").find_element_by_tag_name("table")
            for row in table_qc2.find_elements_by_css_selector('tr'):
              wr.writerow([d.text for d in row.find_elements_by_css_selector('th,td')]) 
          except NoSuchElementException:
            print('no qc2 table found')

          # Write empty row
          wr.writerow([])

          # Quality Control Monitoring by 3rd Tier
          try: 
            table_qc3 = driver.find_element_by_css_selector("div#divContentSP3TierQM").find_element_by_tag_name("table")
            for row in table_qc3.find_elements_by_css_selector('tr'):
              wr.writerow([d.text for d in row.find_elements_by_css_selector('th,td')]) 
          except NoSuchElementException:
            print('no qc3 table found')

        print('Successfully scraped ' + file_name)
        return True

      result = create_csv_file(file_name)
      attempt = 3
      while not result: # continue trying until it succeeds
        if attempt > 0:
          result = create_csv_file(file_name)
          attempt -= 1
        else:
          print('Failed to scrape ' + file_name)
          break
        
  print('Successfully finished scraping all data')

  end_time = time.time()
  print('Total seconds taken: ')
  print(end_time - start_time)

def main():
  generate_csvs()
  combine_csvs()

if __name__ == "__main__":
  main()
      


