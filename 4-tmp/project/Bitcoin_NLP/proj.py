# -*- coding: utf-8 -*-
# """
# Created on Fri Jan 28 16:20:41 2022

# @author: DE
# """
# imports 
from time import sleep
import json
import pandas as pd
import io
import re
import numpy as np
from tqdm import tqdm
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tnrange, tqdm_notebook, tqdm

from sklearn import preprocessing
import matplotlib.pyplot as plt
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
init_notebook_mode(connected=True) 

# CURRENCY = "bitcoin"
# CURRENCY_SYMBOL = "BTC"

# ## personal config
# TWEETS_FOLDER    = "data/crypto/%s"%(CURRENCY) # Relative path to historical data
# SEP_CHAR         = '~' # character seperating dates from and to in filename
# ENVS             = ['CRYPTO', 'LINE_COUNT', 'MOST_RECENT_FILE', 'MOST_RECENT_ID'] # Stored in var.csv
# MAX_ROW_PER_FILE = 20000 # Each file storing data has a maximum amount of rows

# tweets_raw_file = 'data/twitter/%s/%s_tweets_raw.csv'%(CURRENCY_SYMBOL,CURRENCY)
tweets_raw_file   = 'data/Bitcoin_tweets.csv'
tweets_clean_file = 'data/Bitcoin_tweets_clean.csv'
bit_price_file = 'data/bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv'
# query = '#%s OR #%s'%(CURRENCY,CURRENCY_SYMBOL) ####TODO PUT BACK  OR {CURRENCY} OR ${CURR
df_raw = pd.read_csv(tweets_raw_file,low_memory=False)
print(df_raw.shape)
df_raw.head(5)