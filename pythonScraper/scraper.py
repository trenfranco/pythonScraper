from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.yogonet.com/international/"
driver.get(url)

#waits dinamycally
wait = WebDriverWait(driver, 10)
articles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'noticia')]/div[div[@class='imagen']]")))

#articles = driver.find_elements(By.XPATH, "//div[contains(@class, 'noticia')]/div[div[@class='imagen']]")
print("Total articles: " + str(len(articles)))

scrapedArticles = []
for item in articles[:2]:
    try:
        title = item.find_element(By.XPATH, ".//h2/preceding-sibling::div[1]").text
        kicker = item.find_element(By.XPATH, ".//h2").text
        url = item.find_element(By.XPATH, ".//h2/a").get_attribute("href")
        image = item.find_element(By.XPATH, "./div[@class='imagen']/a/img").get_attribute("src")
        
        scrapedArticles.append({
            "Title": title,
            "Kicker": kicker,
            "Image URL": image,
            "Url": url
        })
    except Exception as e:
        print("Error scraping article:", e)

driver.quit()

for article in scrapedArticles:
    print(article)