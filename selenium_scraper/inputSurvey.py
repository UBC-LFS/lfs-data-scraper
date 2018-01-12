from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://inputsurvey.dacnet.nic.in/districttables.aspx")
driver.set_page_load_timeout(60)

# Get the 8 dropdowns from this page and put their options in their respective list
dropdown_year = driver.find_element_by_id("_ctl0_ContentPlaceHolder2_ddlYear")
num_options_year = len(dropdown_year.find_elements_by_tag_name("option"))

# Nested for-loops to try every possible combination of the options in the 8 dropdowns
for index_year in range(0, num_options_year):
    dropdown_state = driver.find_element_by_id("_ctl0_ContentPlaceHolder2_ddlStates")
    num_options_state = len(dropdown_year.find_elements_by_tag_name("option"))

    for index_state in range(0, num_options_state):
        dropdown_district = driver.find_element_by_id("_ctl0_ContentPlaceHolder2_ddldistrict")
        num_options_district = len(dropdown_district.find_elements_by_tag_name("option"))

        for index_district in range(0, num_options_district):
            dropdown_tables = driver.find_element_by_id("_ctl0_ContentPlaceHolder2_ddlTables")
            num_options_tables = len(dropdown_tables.find_elements_by_tag_name("option"))

            dropdown_tables = driver.find_element_by_id("_ctl0_ContentPlaceHolder2_ddlTables")
            dropdown_tables.find_elements_by_tag_name("option")[index_tables]

            for index_tables in range(0, num_options_tables):

                dropdown_tables = driver.find_element_by_id("_ctl0_ContentPlaceHolder2_ddlTables")
                dropdown_tables.find_elements_by_tag_name("option")[index_tables].click()

                # Click submit button to load the page with data tables
                button_submit = driver.find_element_by_id("_ctl0_ContentPlaceHolder2_cmdSubmit")
                button_submit.click()

                # Download the data as a CSV

                # Click back button to go to main page
                button_back = driver.find_element_by_id("btnBack")
                button_back.click()

driver.close()
