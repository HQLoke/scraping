from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd 
import requests
import datetime

begin = datetime.datetime.now()

path = r"/Users/jakoh/Desktop/priceshop/chromedriver_87"
chrome_options = Options()
chrome_options.add_argument("--incognito")
prefs = {'profile.default_content_setting_values': {'images': 2,'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(path, options=chrome_options)
wait = WebDriverWait(driver, 3)

links = pd.read_csv("~/Desktop/priceshop/selenium/Lazada Links.csv")
# links_arr = list(links["Lazada Link"])
links.drop(columns=['Unnamed: 1', 'Notes for cadets'], inplace=True)
# for l in links["Lazada Link"]:
# 	print(l)
url = []
name = []
price = []
quantity = []
storage = []
word = 0
for link in links["Lazada Link"]:
	word = 0
	driver.get(link)
	n = driver.find_element(By.XPATH, '//*[@id="module_product_title_1"]/div/div/h1').get_attribute("innerHTML")
	p = driver.find_element(By.XPATH, '//*[@id="module_product_price_1"]/div/div/span').get_attribute("innerHTML")
	q = driver.find_element(By.XPATH, '//*[@id="module_quantity-input"]/div/div/span').get_attribute("innerHTML")
	s = ""
	try:
		h6 = driver.find_elements(By.XPATH, '//*[@id="module_sku-select"]/div/div/div/h6')
		i = 0
		for h in h6:
			i += 1
			lower = h.text.lower()
			if "storage" in lower or "spec" in lower:
				word = 1
				txt = driver.find_elements(By.XPATH, f'//*[@id="module_sku-select"]/div/div[{i}]/div/div/div[2]/span')
				for t in txt:
					t.click()
					n = driver.find_element(By.XPATH, '//*[@id="module_product_title_1"]/div/div/h1').get_attribute("innerHTML")
					p = driver.find_element(By.XPATH, '//*[@id="module_product_price_1"]/div/div/span').get_attribute("innerHTML")
					q = driver.find_element(By.XPATH, '//*[@id="module_quantity-input"]/div/div/span').get_attribute("innerHTML")
					s = t.text
					url.append(link)
					name.append(n)
					price.append(p)
					quantity.append(q)
					storage.append(s)
					time.sleep(1)
				break
	except:
		print("banana")
	if word == 0:
		url.append(link)
		name.append(n)
		price.append(p)
		quantity.append(q)
		storage.append(s)
	time.sleep(2)

df = pd.DataFrame({
	"productURL" : url,
	"productName from URL" : name,
	"price": price,
	"quantity": quantity,
	"storage": storage
})
df.to_csv(r'~/Desktop/priceshop/test.csv')
print(datetime.datetime.now() - begin)


# prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2, 
#                             'plugins': 2, 'popups': 2, 'geolocation': 2, 
#                             'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
#                             'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
#                             'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
#                             'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
#                             'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
#                             'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
#                             'durable_storage': 2}}