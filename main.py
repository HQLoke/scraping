from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from multiprocessing.sharedctypes import Value
from unicodedata import category
import pandas as pd
import string

# target = "samsung galaxy a03"
# testcases = ["samsung galaxy a3", "samsunggalaxy a3", "samsung galaxy a 3", "samsung galaxy",
# 			"galaxy a3 samsung", "galaxy a03 samsung"]

# for i in testcases:
# 	print(fuzz.ratio(target, i))

# df = pd.read_csv(r"./data/link_name.csv")

# data = df[r"productName from URL"]

# for i in data:
# 	print(i.lower())

# Split product key into tokens
pk = pd.read_csv(r"./data/product_key.csv")
pk = pk[pk['category'] == "Mobile"]
pk_data = pk[(r"PSmodelName")]

for data in pk_data:
	space = data.index(' ')
	try:
		bracket = data.rfind(r'(')
		print(data[0:space], end='')
		print(data[space:bracket], end='')
		print(data[bracket:])
	except ValueError as ve:
		print("", end='')
		print(data[0:space], end='')
		print(data[space+1:])

# # Reading link names
# ln = pd.read_csv(r"./data/link_name.csv")
# linkname = ln["productName"]

# for data in linkname:
# 	data = data.lower()
# 	if (data.find('apple') != -1):
# 		print("TRUE")
# 	else:
# 		print("FALSE")
