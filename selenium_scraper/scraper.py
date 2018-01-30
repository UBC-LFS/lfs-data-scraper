from selenium import webdriver
import logging
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process
import time
import os

log = logging.getLogger('scraper_log')
logging.basicConfig(level=logging.INFO, filename='./scraper.log')
log.setLevel(logging.INFO)

def submitForm(driver, year, counter):
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

    # Rename the file so OS doesn't interrupt
    old_file = os.path.join('C:\\Users\\eric\\Downloads', 'DistTableDisplay6b.xlsx')
    while not os.path.exists(old_file):
        time.sleep(1)
    new_file = os.path.join('C:\\Users\\eric\\Downloads', 'DistTableDisplay6b - ' + str(year) + '-' + str(counter) + '.xlsx')
    os.rename(old_file, new_file)
    counter += 1

    # Click back button to go to main page
    button_back = driver.find_element_by_id("btnBack")
    button_back.click()

def configureDropdowns(driver, options):
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
        if dropdownElement.find_elements_by_tag_name('option')[i].text == text:
            return i
    raise Exception('No option with text: ' + text + ' was found')


def count(index_year):
    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.get("http://agcensus.dacnet.nic.in/DistCharacteristic.aspx")
    counter = 0
    file = open('./mapping-' + str(index_year) + '.txt', 'w')
    # Need to click the current year because the other dropdown options change based on this
    dropdown_year = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlYear")
    dropdown_year.find_elements_by_tag_name('option')[index_year].click()

    dropdown_social_group = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlSocialGroup")
    # We only want the option with "ALL SOCIAL GROUPS" for this project
    all_social_groups_index = findIndexByText(dropdown_social_group, 'ALL SOCIAL GROUPS')
    dropdown_social_group.find_elements_by_tag_name('option')[all_social_groups_index].click()

    dropdown_state = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlState")
    num_options_state = len(dropdown_state.find_elements_by_tag_name("option"))

    for index_state in range(0, num_options_state):
        try:
            dropdown_state = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlState")
            dropdown_state.find_elements_by_tag_name('option')[index_state].click()
            dropdown_district = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlDistrict")
            num_options_district = len(dropdown_district.find_elements_by_tag_name("option"))
        except UnexpectedAlertPresentException:
            print("caught error")
            alert = driver.switch_to.alert
            alert.accept()
            continue

        for index_district in range(0, num_options_district):
            try:
                dropdown_district = driver.find_element_by_id("_ctl0_ContentPlaceHolder1_ddlDistrict")
                dropdown_district.find_elements_by_tag_name('option')[index_district].click()
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
                    # If anything in this try block fails, we will re-try the same configuration up to 3 times before
                    # we move on to the next one
                    try:
                        options = configureDropdowns(driver, dropdown_input)
                        submitForm(driver, index_year, counter)

                    except Exception as e:
                        # If configureDropdowns failed, then options will be null
                        if (options != None):
                            log.error('There was an error while submitting the form for options:\n' +
                                      'Year: ' + str(options[0]) + '\n' +
                                      'Social Group: ' + str(options[1]) + '\n' +
                                      'State: ' + str(options[2]) + '\n' +
                                      'District: ' + str(options[3]) + '\n' +
                                      'Table: ' + str(options[4]) + '\n' +
                                      'Crop: ' + str(options[5]) + '\n')
                        else:
                            log.error('There was an error while submitting the form for options:\n' +
                                      'Year index: ' + str(index_year) + '\n' +
                                      'Social Group index: ' + str(all_social_groups_index) + '\n' +
                                      'State index: ' + str(index_state) + '\n' +
                                      'District index: ' + str(index_district) + '\n' +
                                      'Table index: ' + str(cropping_pattern_table_index) + '\n' +
                                      'Crop index: ' + str(index_crops) + '\n')
                        for i in range(0, 2):
                            # Retry up to 3 more times. First success breaks out of for-loop
                            try:
                                driver.get("http://agcensus.dacnet.nic.in/DistCharacteristic.aspx")
                                configureDropdowns(driver, dropdown_input)
                                submitForm(driver, index_year, counter)
                                break
                            except (NoSuchElementException, TimeoutException) as e:
                                # Keep trying the same configuration
                                continue
                        # Okay.. current configuration isn't working. Stop trying and move onto the next.
                        continue

                dropdown_input = [('_ctl0_ContentPlaceHolder1_ddlYear', index_year),
                                  ('_ctl0_ContentPlaceHolder1_ddlSocialGroup', all_social_groups_index),
                                  ('_ctl0_ContentPlaceHolder1_ddlState', index_state),
                                  ('_ctl0_ContentPlaceHolder1_ddlDistrict', index_district),
                                  ('_ctl0_ContentPlaceHolder1_ddlTables', cropping_pattern_table_index)]
                # If anything in this try block fails, we will re-try the same configuration up to 3 times before
                # we move on to the next one
                options = configureDropdowns(driver, dropdown_input)
                for i in range(0, num_options_crops):
                    file.write(str(index_year) + ',' + str(all_social_groups_index) + ',' + str(index_state) +
                               ',' + str(index_district) + ',' + str(cropping_pattern_table_index) +
                               ',' + str(i) + '\n')
                counter += num_options_crops
                print(str(counter))
            except UnexpectedAlertPresentException:
                print("caught error")
                alert = driver.switch_to.alert
                alert.accept()
                continue
    print('There are this many unique combinations: ' + str(counter))

if __name__ == '__main__':
    processes = []

    for year in range(0, 4):
        p = Process(target=count, args=(year,))
        p.start()
        processes.append(p)
        # seems like we need to stagger the spawning of processes for all the browsers to load the initial page properly
        time.sleep(2)

    for p in processes:
        p.join()

