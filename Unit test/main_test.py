import os
os.chdir("..")


import main as m

m.collect_daily_cal()
print(m.daily_calories)
