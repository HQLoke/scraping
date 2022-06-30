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
broadband = "\(*[3-5][Gg][^Bb]\)*"
display = "[0-9]+[.]*[0-9]+[- ]inch"
generation = "... gen"
network = "wi-fi[ ]*[+][ ]*cellular|wi-fi[ ]*[+][ ]*mobile network|wi-fi"
ram = "\(6gb|\(8gb|\(16gb"
product_storage = "\(*[0-9]+[MmGgTb]*[Bb]*[ ]*[+][ ]*[0-9]+[ ]*[MmGgTb][Bb]\)*"
product_storage_apple = "1[Tt][Bb]|2[Tt][Bb]|\(*[1-9]+[MmGgTb][Bb]\)*"
scraped_storage = "\(.+\)|[0-9]+[MmGgTb][Bb]"
year = "20[1-2][0-9]"

def dict_add(dict_new, regex, key_name, name, add_dict):
	temp = name
	rgx = re.findall(regex, name)
	dict_new.update({key_name:None})
	i = 0
	while (i < len(rgx)):
		temp = name.replace(rgx[i], '')
		if (add_dict == True):
			dict_new.update({key_name:rgx[0]})
		i += 1
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
		name = dict_add(dict_new, broadband, 'Broadband', name, True)
		name = dict_add(dict_new, display, 'Display', name, True)
		name = dict_add(dict_new, generation, 'Generation', name, True)
		name = dict_add(dict_new, network, 'Network', name, True)
		name = dict_add(dict_new, year, 'Year', name, True)
		if (code == 1):
			if (dict_new['Brand'] != 'apple'):
				name = dict_add(dict_new, product_storage, 'Storage', name, True)
			else:
				name = dict_add(dict_new, product_storage_apple, 'Storage', name, True)
		elif (code == 2):
			name = dict_add(dict_new, scraped_storage, 'Storage', name, True)
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
	if (pd.isna(temp2[i]) != True):
		s['Storage'] = temp2[i]		
	name = str(s['Storage'])
	name = rm_tuple_from_name(name, symbol)
	name = name.replace(' ', '')
	if (len(name) <= 0):
		s['Storage'] = None
	else:
		s['Storage'] = name
	s.update({'StockStatus':temp3[i]})
	i += 1

# for p in product:
# 	print(p)

# for s in scraped:
# 	print(s['Storage'])