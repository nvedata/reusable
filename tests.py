from string import ascii_uppercase

import numpy as np
import pandas as pd

import utils

#generate data
df=np.random.rand(100, 10)
idx=pd.date_range(start='2019-01-01', periods=df.shape[0], freq='10min')
cols=list(ascii_uppercase)[:df.shape[1]]
df=pd.DataFrame(df, index=idx, columns=cols)

#columnwise_shift
offsets=pd.Series(range(df.columns.size), index=X.columns)
print(columnwise_shift(df, offsets, 'h').apply(lambda x: x.dropna().index.min()))

#columnwise_rolling
windows=pd.Series(range(df.columns.size), index=X.columns)
print(columnwise_rolling(df, windows, 'mean').count())
