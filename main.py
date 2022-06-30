from math import nan
from os import sep
import numpy as np
import pandas as pd
import re

str = "Apple  iPad Pro 11-inch (2021) (2TB) Wi-Fi"
regex = "\(*[1-9]+[MmGgTb][Bb]\)*"
rgx = re.findall(regex, str)

if (len(rgx) > 0):
	print(rgx[0])