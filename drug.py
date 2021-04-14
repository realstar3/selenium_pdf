import os
import pandas as pd
import json
import time
from selenium import webdriver





def working(url):
    chrome_options = webdriver.ChromeOptions()
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
             'savefile.default_directory': save_dir}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROMEDRIVER_PATH)
    # driver, err_msg = create_driver(driver_location=CHROMEDRIVER_PATH, logger=logger, proxy=None,
    #                                     headless=headless, disable_image_load=False)
    # driver.get("https://www.rxlist.com/babybig-drug.htm")
    driver.get(url)
    btn = driver.find_elements_by_xpath("//button[@class='eugdpr-consent-button']")
    if len(btn) > 0:
        btn[0].click()
        time.sleep(1)
    driver.execute_script('window.print();')
    time.sleep(15)
    driver.quit()


def get_urls(url, csv_file):
    f = open(csv_file, "w")
    f.write(csv_file + '\n')
    f = open(csv_file, "a")

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROMEDRIVER_PATH)
    driver.get(url)
    btn = driver.find_elements_by_xpath("//button[@class='eugdpr-consent-button']")
    if len(btn) > 0:
        btn[0].click()
        time.sleep(1)
    # driver.set_window_size(1300, 900)
    all_li_tags = driver.find_elements_by_xpath("//ul/li")
    count = 1
    for li_tag in all_li_tags:
        if '\n- FDA' in li_tag.text:
            m_url = li_tag.find_element_by_xpath('.//a').get_attribute('href')
            f.write(m_url + '\n')
            print(count, ':', m_url, '\n')
            count = count + 1

    driver.close()


if __name__ == '__main__':
    KEYWORD = "q"
    first_url = "https://www.rxlist.com/drugs/alpha_"+ KEYWORD + ".htm"
    save_dir = os.path.abspath(os.path.join(os.path.curdir, "pdf/" + KEYWORD))
    os.makedirs(save_dir, exist_ok=True)
    

    CHROMEDRIVER_PATH = './chromedriver'
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    date_fmt = '%Y-%m-%d'
    log_location = './logs'
    # logger = create_logger(log_location, 'drug' + datetime.now().strftime(date_fmt))
    # logger.info('Started ---------- {}'.format(datetime.now().strftime(fmt)))    
    driver_location = "./chromedriver"
    headless = False

    basename = os.path.splitext(os.path.split(first_url)[1])[0]
    fname = basename + ".csv"
    _csv_file = os.path.join(save_dir, fname)

    get_urls(first_url, _csv_file)
    df = pd.read_csv(_csv_file)

    df.drop_duplicates(keep="first", inplace=True)
    df.to_csv(_csv_file, index=False)

    n_total = len(df)
    start = 0
    for i in range(start, n_total):
        try:
            u = df.iloc[i, 0]
            working(u)
            i = i + 1
            print(f"completed {i} /{n_total}, {u}")
        except Exception as e:
            print(f"failed {i} / {n_total}:  {e}")
