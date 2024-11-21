from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import pandas as pd

def scrape_union_addresses():
    '''
    This function scrapes all state of the union addresses from The American Presidency Project (presidency.ucsb.edu) and saves them as .txt files together with an overview .csv file.
    '''
    url = "https://www.presidency.ucsb.edu/documents/app-categories/spoken-addresses-and-remarks/presidential/state-the-union-addresses"

    driver = webdriver.Firefox()
    time.sleep(5)
    driver.get(url)

    speech_result = []

    last_page = False
    while (last_page == False):
        
        time.sleep(0.2)
        speeches = driver.find_elements(By.CLASS_NAME, 'view-content')[0].find_elements(By.CLASS_NAME, 'row')
        
        for i in range(1,len(speeches)+1):
            speech = driver.find_element(By.XPATH, f'/html/body/div[2]/div[4]/div/section/div/section/div/div[4]/div[{i}]')
            link = speech.find_element(By.CLASS_NAME, "field-title").find_element(By.TAG_NAME, "a").get_attribute("href")
            date = speech.find_element(By.CLASS_NAME, "date-display-single").text
            speaker_name = speech.find_element(By.CLASS_NAME, "col-sm-4.margin-top").find_element(By.TAG_NAME, "p").text

            time.sleep(0.2)
            driver.get(link)
            try: 
                speech = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "field-docs-content"))).text

            except:
                current_url = driver.current_url
                time.sleep(5)
                driver.get(current_url)
                time.sleep(5)
                speech = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "field-docs-content"))).text
                
            filename = speaker_name.lower() + "_" + date.lower()
            filename = filename.replace(" ", "_").replace(".","").replace(",","")
            with open(f"Data/{filename}.txt", "w", encoding = "utf-8") as f:
                f.write(speech)
                f.close()
            driver.back()
            time.sleep(0.2)

            speech_result.append({"Date":date,"Speaker": speaker_name, "Link": link, "File": f"Data/{filename}.txt"})
            print(f"Saving speech by {speaker_name} from {date}.")

        try:
            driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a").click()
        except:
            last_page = True
            print("Scraping finished. All data is saved in Data directory. Have a nice day and goodbye!")
            driver.close()
    pd.DataFrame(speech_result).to_csv("Data/speeches_overview.csv")