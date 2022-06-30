from curses.ascii import isdigit
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from multiprocessing.sharedctypes import Value
from unicodedata import category
import pandas as pd
import string

# Split product keys into a list of usable info
# Brand, Model, Model Year, Size
pk = pd.read_csv(r"./data/product_key.csv")
pk = pk[pk['category'] != "Laptop"]
pk_data = pk[(r"PSmodelName")]

product_key = []
for data in pk_data:
	list = []
	data = data.lower()
	space = data.index(' ')
	size_bracket = data.rfind(r'(')
	if (size_bracket != -1):
		year_bracket = data.index(r'(')
		list.append(data[0:space])
		if (year_bracket != size_bracket):
			list.append(data[space+1:year_bracket-1])
			list.append(data[year_bracket:size_bracket-1])
		else:
			list.append(data[space+1:size_bracket-1])
			list.append('NULL')
		list.append(data[size_bracket:].replace(' ', ''))
	else:
		list.append(data[0:space])
		list.append(data[space+1:])
	product_key.append(list)

# Simplified scraped data
db = pd.read_csv(r"./data/complete.csv")
database = db["productName from URL"]

for i in range(len(database)):
	l = 0
	if (database[i][0].isalnum() == False):
		while (database[i][l].isalpha() == False):
			l += 1
	delim = l
	while delim < len(database[i]):
		if (database[i][delim] == r'(' or database[i][delim] == r'[' or database[i][delim] == r'*'):
			break
		delim += 1
	database[i] = database[i][l:delim].lower()

# Remove the brand name from each database entry
def cleanse(database, product_key):
	for i in range(len(database)):
		for key in product_key:
			if (database[i].find(key[0]) != -1):
				database[i] = database[i].replace(r"\"", '').strip()
				break

cleanse(database, product_key)

# To see if a product key matches with a database entry
def matching(key, data):
	if (data.find(key[0]) != -1 and (data.find(key[1] + ' ') != -1 or data.find(key[1] + r'/') != -1)):
		return True
	return False

count = 0
# # Reading link names
for data in database:
	data = data.lower()
	for key in product_key:
		if (matching(key, data) == True):
			print("TRUE")
			print("KEY  = ", key)
			print("DATA = ", data)
			print("")
			count += 1
			break
		else:
			pass

print(count)
