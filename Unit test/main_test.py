import os

os.chdir("..")

import main as m
import random
import numpy as np
from datetime import datetime as dt

f = open("test.txt", "w")
f.write("124312")
f.write({"a": 1, "b": 2}.__str__())
f.write({"a": 1, "b": 2}.__str__())
