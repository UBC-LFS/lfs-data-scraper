# Scraping Roads Data

This script takes data from HTML tables from http://omms.nic.in/ and generates CSV files.

1. Install Python 3.6.5

2. Download the driver for your preferred browser. The Python project is set up to work with Chrome.

   Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads <br>
   Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ <br>
   Firefox:	https://github.com/mozilla/geckodriver/releases <br>
   Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/

   After downloading the driver, make sure the path to the executable is visible in your PATH environment variable. For example, for the Chrome driver, you should be able to run `chromedriver` in your terminal and see a reasonable output.

3. Run `python -m pip install selenium` to install selenium

4. Run `python road_data_scraper.py` or `python .\road_data_scraper.py` 

5. CSV files should be created in road_data_scraper/output/

# Merging CSVs

1. Type `npm install`

2. Run `npm run section1` to merge Status Of Connectivity

3. Run `npm run section3` to merge Phasewise Summary

3. Merged files will be created in lfs-data-scraper/road_data_scraper