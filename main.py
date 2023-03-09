from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import multiprocessing as mp
import pandas as pd
import warnings
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
warnings.simplefilter(action='ignore', category=FutureWarning)



def scrape_image(row):
   
    
    url = f"https://pixabay.com/images/search/?order=ec&pagi={row}"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.set_page_load_timeout(10000)

    driver.get(url)
    
    count = 1
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    new_height = 1000
    

    while True:
        driver.execute_script(f"window.scrollTo(0, {new_height});")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = new_height + 1000
        if new_height>=last_height:
            break

    classitem = driver.find_elements(By.CLASS_NAME,'photo-result-image')
    urls = []

    for i in classitem:
        url = i.get_attribute('src')
        # print(url)
        if url.endswith('.jpg'):
            improve_url = url.replace("_360", "960_720")
            improve_url = improve_url.replace("_340", "960_720")
            print(improve_url)
            urls.append(improve_url)
            count = count + 1
            print(count)

    driver.close()

    return urls
  
if __name__ == '__main__':
    
   
    columns = ['Page', 'Image URL']
    df = pd.DataFrame(columns=columns)
    pool = mp.Pool(processes=8)

    results = pool.map(scrape_image, range(1, 10000))
    for i, page_urls in enumerate(results):
        for url in page_urls:
            df = df.append({'Page': i+1, 'Image URL': url}, ignore_index=True)

    
    df.to_excel('image_urls_9000_to_10000.xlsx', index=False)
    
    pool.close()
    pool.join()
