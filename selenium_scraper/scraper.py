from selenium import webdriver
import logging

log = logging.getLogger('scraper_log')
logging.basicConfig(level=logging.INFO, filename='./scraper.log')
log.setLevel(logging.INFO)

driver = webdriver.Chrome()
driver.get("http://agcensus.dacnet.nic.in/DistCharacteristic.aspx")
driver.set_page_load_timeout(60)

dropdown_year = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlYear")
num_options_year = len(dropdown_year.find_elements_by_tag_name("option"))

counter_total = 0
counter_year = 0
counter_social_group = 0
counter_state = 0
counter_district = 0
counter_tables = 0
counter_crops = 0

num_retries = 0

# Nested for-loops to try every possible combination of the options in the 8 dropdowns
for index_year in range(0, num_options_year):
    dropdown_social_group = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlSocialGroup")
    # Count only the options where the value matches "ALL SOCIAL GROUPS"
    for y in dropdown_social_group.find_elements_by_tag_name("option"):
        print(y.get_attribute('value'))
    num_options_social_group = len([x for x in dropdown_social_group.find_elements_by_tag_name("option")
                                    if x.get_attribute('value') == '4'])

    for index_social_group in range(0, num_options_social_group):
        dropdown_state = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlState")
        num_options_state = len(dropdown_year.find_elements_by_tag_name("option"))

        for index_state in range(counter_state, num_options_state):
            dropdown_district = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlDistrict")
            num_options_district = len(dropdown_district.find_elements_by_tag_name("option"))

            if counter_state == num_options_state - 1:
                counter_state = 0
            else:
                counter_state += 1

            for index_district in range(0, num_options_district):
                dropdown_tables = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlTables")
                num_options_tables = len([x for x in dropdown_tables.find_elements_by_tag_name("option")
                                    if x.get_attribute('value') == '6b'])

                for index_tables in range(0, num_options_tables):
                    [x for x in dropdown_tables.find_elements_by_tag_name("option")
                     if x.get_attribute('value') == '6b'][0].click()
                    dropdown_crops = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCrop")
                    num_options_crops = len(dropdown_crops.find_elements_by_tag_name('option'))

                    for index_crops in range(counter_crops, num_options_crops):
                        log.info('Starting unique combination #' + str(counter_total))

                        # Make the unique combination of options from the 6 dropdowns
                        dropdown_year = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlYear")
                        current_option_year = dropdown_year.find_elements_by_tag_name("option")[index_year]
                        value_year = current_option_year.get_attribute('value')

                        dropdown_social_group = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlSocialGroup")
                        # Click only the "ALL SOCIAL GROUPS" option
                        current_option_social_group = [x for x in dropdown_social_group.find_elements_by_tag_name("option") if
                         x.get_attribute('value') == '4'][index_social_group]
                        value_social_group = current_option_social_group.get_attribute('value')

                        dropdown_state = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlState")
                        current_option_state = dropdown_year.find_elements_by_tag_name("option")[index_state]
                        value_state = current_option_state.get_attribute('value')

                        dropdown_district = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlDistrict")
                        current_option_district = dropdown_district.find_elements_by_tag_name("option")[index_district]
                        value_district = current_option_district.get_attribute('value')

                        dropdown_tables = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlTables")
                        current_option_tables = [x for x in dropdown_tables.find_elements_by_tag_name("option")
                            if x.get_attribute('value') == '6b'][index_tables]
                        value_tables = current_option_tables.get_attribute('value')

                        dropdown_crops = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCrop")
                        current_option_crops = dropdown_crops.find_elements_by_tag_name("option")[index_crops]
                        value_crops = current_option_crops.get_attribute('value')

                        # Click the current unique combination of dropdown options
                        current_option_year.click()
                        current_option_social_group.click()
                        current_option_state.click()
                        current_option_district.click()
                        current_option_tables.click()
                        current_option_crops.click()

                        # If anything in this try block fails, we will re-try the same configuration up to 3 times before
                        # we move on to the next one
                        try:
                            # Click submit button to load the page with data tables
                            button_submit = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_btnSubmit")
                            button_submit.click()

                            # Download the data as a CSV
                            button_save = driver.find_element_by_xpath('//*[@id="ReportViewer1__ctl5__ctl4__ctl0_ButtonImg"]')
                            button_save.click()
                            button_excel = driver.find_element_by_xpath('//*[@id="ReportViewer1__ctl5__ctl4__ctl0_Menu"]/div[5]/a')
                            button_excel.click()

                            # Click back button to go to main page
                            button_back = driver.find_element_by_id("btnBack")
                            button_back.click()
                            log.info('Successfully downloaded file for combination #' + str(counter_total))
                            counter_total += 1

                            # If we reach the last option for any of the dropdowns, reset to 0. Otherwise, increment
                            # We need to do this because if we get an error, we want to start over without repeating
                            # the configurations we have already downloaded.
                            if counter_crops == num_options_crops - 1:
                                counter_crops = 0
                            else:
                                counter_crops += 1

                            if counter_district == num_options_district - 1:
                                counter_district = 0
                            else:
                                counter_district += 1

                            if counter_tables == num_options_tables - 1:
                                counter_tables = 0
                            else:
                                counter_tables += 1

                            if counter_tables == num_options_tables - 1:
                                counter_tables = 0
                            else:
                                counter_tables += 1

                            if counter_year == num_options_year - 1:
                                counter_year = 0
                            else:
                                counter_year += 1

                        except:
                            log.error('There was an error while submitting the form for options:\n' +
                                      'Year: ' + str(current_option_year) + '\n' +
                                      'Social Group: ' + str(current_option_social_group) + '\n' +
                                      'State: ' + str(current_option_state) + '\n' +
                                      'District: ' + str(current_option_district) + '\n' +
                                      'Table: ' + str(current_option_tables) + '\n' +
                                      'Crop: ' + str(current_option_crops) + '\n')
                            # TODO: re-try the failed configuration up to 3 times before moving onto the next
                            num_retries += 1
                            # Retry here

                            # Move onto next
                            if num_retries >= 3:



driver.close()
