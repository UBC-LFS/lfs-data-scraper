from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://agcensus.dacnet.nic.in/DistCharacteristic.aspx")
driver.set_page_load_timeout(60)

# Get the 8 dropdowns from this page and put their options in their respective list
dropdown_year = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlYear")
num_options_year = len(dropdown_year.find_elements_by_tag_name("option"))

# Nested for-loops to try every possible combination of the options in the 8 dropdowns
for index_year in range(0, num_options_year):
    dropdown_social_group = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlSocialGroup")
    # Count only the options where the value matches "ALL SOCIAL GROUPS"
    num_options_social_group = len([x for x in dropdown_social_group.find_elements_by_tag_name("option")
                                    if x.get_attribute('value') == 'ALL SOCIAL GROUPS'])

    for index_social_group in range(0, num_options_social_group):
        dropdown_state = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlState")
        num_options_state = len(dropdown_year.find_elements_by_tag_name("option"))

        for index_state in range(0, num_options_state):
            dropdown_district = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlDistrict")
            num_options_district = len(dropdown_district.find_elements_by_tag_name("option"))

            for index_district in range(0, num_options_district):
                dropdown_tables = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlTables")
                num_options_tables = len(dropdown_tables.find_elements_by_tag_name("option"))

                for index_tables in range(0, num_options_tables):
                    dropdown_crops = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCrop")
                    num_options_crops = len([x for x in dropdown_tables.find_elements_by_tag_name("option")
                                    if x.get_attribute('value') == 'TENANCY' or x.get_attribute('value') == 'CROPPING PATTERN'])

                    for index_crops in range(0, num_options_crops):
                        # Make the unique combination of options from the 8 dropdowns
                        dropdown_year = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlYear")
                        dropdown_year.find_elements_by_tag_name("option")[index_year].click()

                        dropdown_social_group = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlSocialGroup")
                        # Click only the "ALL SOCIAL GROUPS" option
                        [x for x in dropdown_social_group.find_elements_by_tag_name("option") if
                         x.get_attribute('value') == 'ALL SOCIAL GROUPS'][index_social_group].click()

                        dropdown_state = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlState")
                        dropdown_state.find_elements_by_tag_name("option")[index_state].click()

                        dropdown_district = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlDistrict")
                        dropdown_district.find_elements_by_tag_name("option")[index_district].click()

                        dropdown_tables = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlTables")
                        [x for x in dropdown_tables.find_elements_by_tag_name("option")
                            if x.get_attribute('value') == 'TENANCY' or x.get_attribute('value') == 'CROPPING PATTERN'][index_tables].click()

                        dropdown_crops = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCrop")
                        dropdown_crops.find_elements_by_tag_name("option")[index_crops].click()



                        # Click submit button to load the page with data tables
                        button_submit = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_btnSubmit")
                        button_submit.click()

                        # Download the data as a CSV

                        # Click back button to go to main page
                        button_back = driver.find_element_by_id("btnBack")
                        button_back.click()

driver.close()
