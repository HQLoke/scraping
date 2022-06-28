from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime
import numpy as np 
import pandas as pd 
import requests
import time

begin = datetime.datetime.now()

path = r"./tool/chromedriver_87"
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

links = pd.read_csv("./data/lazada_links.csv")
# links_arr = list(links["Lazada Link"])
links.drop(columns=['Unnamed: 1', 'Notes for cadets'], inplace=True)
# for l in links["Lazada Link"]:
# 	print(l)
name = []
price = []
quantity = []
storage = []
word = "storage"
for link in links["Lazada Link"][:10]:
	driver.get(link)
	# wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="module_product_title_1"]/div/div/h1')))
	# driver.execute_script("window.stop();")
	n = driver.find_element(By.XPATH, '//*[@id="module_product_title_1"]/div/div/h1').get_attribute("innerHTML")
	p = driver.find_element(By.XPATH, '//*[@id="module_product_price_1"]/div/div/span').get_attribute("innerHTML")
	q = driver.find_element(By.XPATH, '//*[@id="module_quantity-input"]/div/div/span').get_attribute("innerHTML")
	# get h6 if store in h6
	# find for sku-variable-name-selected and click to deselect all
	# get all element with sku-variable-name
	# loop through each element with sku-variable-name
	# get title
	print(driver.get_cookies())
	try:
		driver.find_element(By.CLASS_NAME, 'sku-variable-name-selected').click()
		variable = driver.find_element(By.CLASS_NAME, 'sku-variable-name')
		print(variable)
		for var in variable:
			print(var.title)
	except:
		print("nothing to click")

	name.append(n)
	price.append(p)
	quantity.append(q)
	time.sleep(2)

df = pd.DataFrame({
	"productURL" : links["Lazada Link"][:10],
	"productName from URL" : name,
	"price" : price,
	"Stock Status from URL" : quantity
})
df.to_csv(r'./test.csv')
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