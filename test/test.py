from math import nan
from os import sep
import numpy as np
import pandas as pd
import re

# Brute force method
# Using tuples of keywords to extract specific and remove redundant info
brand = ("apple", "honor", "huawei", "infinix", "nokia", "oppo", "realme",
		 "redmi", "samsung", "vivo", "xiaomi")
color = ("emerald green", "mystic silver", "silver", "space gray", "space grey")
useless = ("1 year", "2 years", "2 year", "bag", "by", "chinese", "dual",
		   "extended", "free", "language", "laptop", "malaysia", "malaysai",
		   "model", "mouse", "new", "original", "ram", "ready", "set",
		   "sim", "stock",  "warranty", "wireless")
symbol = ("*", "[", "]", "(", ")", "【", "】", ",")

# Regex method
# Add info to dictionary
display = "[0-9]+[.]*[0-9]+[- ]inch"
generation = "... gen"
network = "wi-fi[ ]*[+][ ]*cellular|wi-fi[ ]*[+][ ]*mobile network|wi-fi"
ram = "8gb|16gb"
storage = "\([^5].*[Gg][Bb]\)|64[ ]*[Gg]*[Bb]*|128[ ]*[Gg]*[Bb]*|256[ ]*[Gg]*[Bb]*|512[ ]*[Gg]*[Bb]*|1tb|2tb"
year = "20[1-2][0-9]"

def dict_add(dict_new, regex, key_name, name, add_dict):
	temp = name
	rgx = re.findall(regex, name)
	dict_new.update({key_name:None})
	if (len(rgx) > 0):
		temp = name.replace(rgx[0], '')
		if (add_dict == True):
			dict_new.update({key_name:rgx[0]})
	return temp

def rm_tuple_from_name(name, tuple):
	temp = name
	for t in tuple:
		temp = temp.replace(t, '')
	return temp

# Code == 1, product_key separation
# Code == 2, scrape_data separation
def separation(list, code):
	output = []
	for l in list:
		dict_new = dict()
		name = l.casefold()
		for b in brand:
			if name.find(b) != -1:
				dict_new.update({'Brand':b})
				name = name.replace(b, '')
		name = rm_tuple_from_name(name, color)
		name = rm_tuple_from_name(name, useless)
		name = dict_add(dict_new, display, 'Display', name, True)
		name = dict_add(dict_new, generation, 'Generation', name, True)
		name = dict_add(dict_new, network, 'Network', name, True)
		name = dict_add(dict_new, year, 'Year', name, True)
		name = name.replace(r'(', '')
		name = name.replace(r')', '')
		if (code == 1):
			name = dict_add(dict_new, storage, 'Storage', name, True)
		elif (code == 2):
			name = dict_add(dict_new, storage, 'Storage', name, False)
		name = dict_add(dict_new, ram, 'RAM', name, False)
		name = rm_tuple_from_name(name, symbol)
		idx = name.find(r'/')
		if (idx != -1):
			name = name[0:idx]
		dict_new.update({'model':name.strip()})
		output.append(dict_new)
	return output

# Product key
output_product = pd.read_csv("./data/product_key.csv")
output_product = output_product[r"PSmodelName"]
product = separation(output_product, 1)

# Scraped data
output_scraped = pd.read_csv("./data/scraped_data.csv")
output_to_scraped = output_scraped[r"productName from URL"]
scraped = separation(output_to_scraped, 2)

temp = output_scraped[r"productURL"]
temp2 = output_scraped[r"Variant from URL"]
temp3 = output_scraped[r"Stock Status from URL"]
i = 0
for s in scraped:
	s.update({'URL':temp[i]})
	s['Storage'] = temp2[i]
	if (pd.isna(temp2[i])):
		s['Storage'] = None
	s.update({'StockStatus':temp3[i]})
	i += 1

for p in product:
	print(p)