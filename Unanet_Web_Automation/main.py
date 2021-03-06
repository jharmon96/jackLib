import csv
import os
import time
from selenium import webdriver


# starts google chrome in either headless (export) or standard (import) mode.
def hello(name):
	print("My name is " + name)


def init_brwsr(downloadDir, headless=True, driver_path="", browser=""):
    if browser == "Chrome":
        from selenium.webdriver.chrome.options import Options
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory": downloadDir}
        chromeOptions.add_experimental_option("prefs", prefs)
        if headless:
            chromeOptions.add_argument("--headless")
        if not driver_path:
            driver = webdriver.Chrome(chrome_options=chromeOptions)
        else:
            driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chromeOptions)
        print("browser opened")
    elif browser == "Firefox":
        from selenium.webdriver.firefox.options import Options
        options = Options()
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", downloadDir)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip, text/csv, csv, application/download")
        if headless:
            options.headless = True
        if not driver_path:
            driver = webdriver.Firefox(options=options, firefox_profile=profile)
        else:
            driver = webdriver.Firefox(options=options, executable_path=driver_path, firefox_profile=profile)
        print("browser opened")
    return driver


# logs into the browser with credentials provided in settings.py

def login(driver, URL, username, password):
    '''Logs into unanet. Takes four arguments: driver, URL, username, password'''

    driver.get(URL + "/home")

    id_box = driver.find_element_by_name('username')
    id_box.send_keys(username)

    pass_box = driver.find_element_by_name('password')
    pass_box.send_keys(password)

    login_button = driver.find_element_by_name('button_ok')
    login_button.click()
    print("Logging in...")


print("loaded")

def mkRefFile(table, ref_file, clmPadding, x, y, z):

    """ Creates csv from Unanet table
        Fields:
            tbody - html table
            ref_file - save file name
            clmPadding - column padding in case headers don't line up to values
            x - Skip # of header records (int)
            y - Skip # of rows in table body (int)
            z - Skip # of attributes in table body rows (int)
    """

    head = table.find_element_by_tag_name('thead')
    body = table.find_element_by_tag_name('tbody')

    file_data = []

    head_line = head.find_element_by_tag_name("tr")
    file_header = [header.text.replace('\n', ' ') for header in head_line.find_elements_by_tag_name('td')[x:]]

    print(str(file_header))

    for x in range(clmPadding):
        file_header.insert(0, '')
    file_header.insert(0,'key')
    file_data.append(",".join(file_header))

    body_rows = body.find_elements_by_tag_name('tr')
    for row in body_rows[y:]:
        tds = row.find_elements_by_tag_name('td')
        key = row.get_attribute("id").strip("k_").strip("r")
        file_row = []
        for td in tds[z:]:
            td_text = td.text
            file_row.append(td_text)
        file_row.insert(0, key)
        file_data.append(",".join(file_row))

    with open(ref_file, "w") as f:
        f.write("\n".join(file_data))