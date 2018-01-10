Setup Steps:

1. Download the driver for your preferred browser. The Python project is set up to work with Chrome.

Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Firefox:	https://github.com/mozilla/geckodriver/releases
Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/

After downloading the driver, make sure the path to the executable is visible in your PATH environment variable. For example, for the Chrome driver, you should be able to run `chromedriver` in your terminal and see a reasonable output.

2. Run `python -m pip install -r requirements.txt` to install the required Python packages

3. Run `python scraper.py`
