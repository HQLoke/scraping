from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from math import nan
from os import sep
import numpy as np
import pandas as pd
import re

str = "SAMSUNG GALAXY A22 LTE/ A22 (5G) (8GB+128GB)NEW MODEL [ORIGINAL SAMSUNG MALAYSIA]*A22 5G*(READY STOCK)"
broadband = "\(*[3-5][Gg]\)*"

rgx = re.findall(broadband, str)
i = 0
while (i < len(rgx)):
	print(rgx[i])
	i += 1