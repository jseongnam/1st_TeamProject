import pandas as pd
import glob
import datetime

data_path = glob.glob('./crawling_data/*.csv')
print(data_path)
df = pd.DataFrame()