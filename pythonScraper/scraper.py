from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import pandas as pd
from bigqueryUploader import upload_to_bigquery


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

chrome_options.binary_location = "/usr/bin/google-chrome"
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.yogonet.com/international/"
driver.get(url)

#dinamycally wait time
wait = WebDriverWait(driver, 10)
articles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'noticia')]/div[div[@class='imagen']][.//h2/preceding-sibling::div[contains(@class, 'volanta')]]")))

scrapedArticles = []

#scrape logic using XPATH
for item in articles:
    try:
        title = item.find_element(By.XPATH, ".//h2/preceding-sibling::div[1]").text
        kicker = item.find_element(By.XPATH, ".//h2").text
        url = item.find_element(By.XPATH, ".//h2/a").get_attribute("href")
        image = item.find_element(By.XPATH, "./div[@class='imagen']/a/img").get_attribute("src")

        #post metrics
        word_count = len(title.split())
        char_count = len(title)
        capitalized_words = [word for word in title.split() if word[0].isupper()]
        
        scrapedArticles.append({
            "Title": title,
            "Kicker": kicker,
            "Image": image,
            "URL": url,
            "Word_Count": word_count,
            "Character_Count": char_count,
            "Capitalized_Words": capitalized_words
        })
    except Exception as e:
        print("Error scraping article:", e)

driver.quit()

#convert to DataFrame
df = pd.DataFrame(scrapedArticles)

success = upload_to_bigquery(df)

if not success:
    print("Uploading process Error")
else:
    print("Success!")

