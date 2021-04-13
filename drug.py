from datetime import datetime
import random
# from insta_lib import *
from selenium.webdriver.common.by import By
import os
import pandas as pd
from selenium import webdriver
import json
import time

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
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')    
    
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROMEDRIVER_PATH)
    # driver, err_msg = create_driver(driver_location=CHROMEDRIVER_PATH, logger=logger, proxy=None,
    #                                     headless=headless, disable_image_load=False)
    # driver.get("https://www.rxlist.com/babybig-drug.htm")
    driver.get(url)
    driver.execute_script('window.print();')   
    time.sleep(15)     
    driver.quit()
      

def get_urls(URL, fileName):
    f = open('./pdf/' + fileName, "w")
    f.write(fileName + '\n')
    f = open('./pdf/' + fileName, "a")
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROMEDRIVER_PATH)
    driver.get(URL)
    # driver.set_window_size(1300, 900)
    all_li_tags = driver.find_elements_by_xpath("//ul/li")
    count = 1
    for li_tag in all_li_tags:
        if '\n- FDA' in li_tag.text:
            m_url = li_tag.find_element_by_xpath('.//a').get_attribute('href')
            f.write(m_url + '\n')                             
            print(count,':', m_url, '\n')
            count = count + 1    
            
    driver.close()    


if __name__ == '__main__':
    first_url = "https://www.rxlist.com/drugs/alpha_c.htm"

    CHROMEDRIVER_PATH = './chromedriver'
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    date_fmt = '%Y-%m-%d'    
    log_location = './logs'
    # logger = create_logger(log_location, 'drug' + datetime.now().strftime(date_fmt))
    # logger.info('Started ---------- {}'.format(datetime.now().strftime(fmt)))    
    driver_location = "./chromedriver"
    headless = False
    log_location = './logs'
    folder = 'pdf'
   
    fileName = first_url.split('/')[-1]
    fileName = fileName[:-4] + ".csv"
   
    if not os.path.isdir(folder):
            os.makedirs(folder)
    
    get_urls(first_url, fileName)
    df = pd.read_csv('./pdf/' + fileName)
    count = len(df)
    start = 0
    for i in range(start, count):
        try:
            u = df.iloc[i,0]
            working(u)
            print("completed {} /{}, {}".format(i, count, u))
        except Exception as e:
            print(e)
            print("failed {} /{}, {}".format(i, count, u))

    
    
