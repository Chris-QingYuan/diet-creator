import os

os.chdir("..")

import utilities as util

paras = util.text_to_dictionary(open("paras").read())
print(paras)