from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from math import nan
from os import sep
import numpy as np
import pandas as pd
import re

print(fuzz.token_set_ratio("hello", "hello    hello    hello hell"))