# Instructions

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

Or to start from a certain state, pass in the dropdown index as an argument. (e.g. `python road_data_scraper.py 5`)

5. CSV files should be created in road_data_scraper/output/
