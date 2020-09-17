import pandas as pd
from functools import partial
pd.DataFrame.i_ = partial(pd.DataFrame.set_index, drop=False)
