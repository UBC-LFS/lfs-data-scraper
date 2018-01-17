from selenium import webdriver
import logging

log = logging.getLogger('scraper_log')
logging.basicConfig(level=logging.INFO, filename='./scraper.log')
log.setLevel(logging.INFO)

driver = webdriver.Chrome()
driver.get("http://agcensus.dacnet.nic.in/DistCharacteristic.aspx")
driver.set_page_load_timeout(60)

num_retries = 0

def submitForm():
    """
    this function submits the form and saves the results as an excel file
    :param year: index of the option in the year dropdown
    :param socialGroup: index of the option in the social group dropdown
    :param state: index of the option in the state dropdown
    :param district: index of the option in the district dropdown
    :param tables: index of the option in the tables dropdown
    :param crops: index of the option in the crops dropdown
    :return: None
    """
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

def configureDropdowns(options):
    """
    this form configures the dropdown options based on the indices specified in the arguments
    :param options: a list of tuples. The tuple MUST be of length 2. The first item of the tuple is the string ID of the
                    dropdown element. The second item is the index of the option to choose from that dropdown.
                    (for example: [('year', 2), ('state', 1)] is a valid argument)
    :return: list of the string values used for each dropdown option, in the same order as the parameter.
            (for example: ['2005', 'California'] would be a return value for the example input above)
    """
    # Make the unique combination of options from the 6 dropdowns
    return_array = []

    for option in options:
        elementID = option[0]
        index = option[1]
        dropdown = driver.find_element_by_id(elementID)
        current_option = dropdown.find_elements_by_tag_name("option")[index]
        current_option.click()
        return_array.append(current_option.text)

def findIndexByText(dropdownElement, text):
    """
    :param dropdownElement: selenium dropdown element
    :param text: string to match with option
    :return: index of the option in the specified dropdown, where the text matches the option's text
    """
    for i in range (0, len(dropdownElement.find_elements_by_tag_name('option'))):
        print(dropdownElement.find_elements_by_tag_name('option')[i].text)
        if dropdownElement.find_elements_by_tag_name('option')[i].text == text:
            return i
    raise Exception('No option with text: ' + text + ' was found')


dropdown_year = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlYear")
num_options_year = len(dropdown_year.find_elements_by_tag_name("option"))
# Nested for-loops to try every possible combination of the options in the 8 dropdowns
for index_year in range(0, num_options_year):
    # Need to click the current year because the other dropdown options change based on this
    print(index_year)
    dropdown_year.find_elements_by_tag_name('option')[index_year].click()

    dropdown_social_group = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlSocialGroup")
    # We only want the option with "ALL SOCIAL GROUPS" for this project
    all_social_groups_index = findIndexByText(dropdown_social_group, 'ALL SOCIAL GROUPS')
    dropdown_social_group.find_elements_by_tag_name('option')[all_social_groups_index].click()

    dropdown_state = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlState")
    num_options_state = len(dropdown_year.find_elements_by_tag_name("option"))

    for index_state in range(0, num_options_state):
        dropdown_state.find_elements_by_tag_name('option')[index_state].click()
        dropdown_district = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlDistrict")
        num_options_district = len(dropdown_district.find_elements_by_tag_name("option"))

        for index_district in range(0, num_options_district):
            dropdown_tables = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlTables")
            cropping_pattern_table_index = findIndexByText(dropdown_tables, 'CROPPING PATTERN')
            dropdown_tables.find_elements_by_tag_name('option')[cropping_pattern_table_index].click()

            dropdown_crops = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlCrop")
            num_options_crops = len(dropdown_crops.find_elements_by_tag_name('option'))

            for index_crops in range(0, num_options_crops):

                dropdown_input = [('_ctl0_ContentPlaceHolder1_ddlYear', index_year),
                                  ('_ctl0_ContentPlaceHolder1_ddlSocialGroup', all_social_groups_index),
                                  ('_ctl0_ContentPlaceHolder1_ddlState', index_state),
                                  ('_ctl0_ContentPlaceHolder1_ddlDistrict', index_district),
                                  ('_ctl0_ContentPlaceHolder1_ddlTables', cropping_pattern_table_index),
                                  ('_ctl0_ContentPlaceHolder1_ddlCrop', index_crops)]
                options = configureDropdowns(dropdown_input)
                # If anything in this try block fails, we will re-try the same configuration up to 3 times before
                # we move on to the next one
                try:
                    submitForm()

                except:
                    log.error('There was an error while submitting the form for options:\n' +
                              'Year: ' + str(options[0]) + '\n' +
                              'Social Group: ' + str(options[1]) + '\n' +
                              'State: ' + str(options[2]) + '\n' +
                              'District: ' + str(options[3]) + '\n' +
                              'Table: ' + str(options[4]) + '\n' +
                              'Crop: ' + str(options[5]) + '\n')
                    # TODO: re-try the failed configuration up to 3 times before moving onto the next
                    num_retries += 1
                    # Retry here

                    # Move onto next




driver.close()

