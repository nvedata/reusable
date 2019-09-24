import numpy as np
import pandas as pd

class HistogramCompressor:
    def __init__(self, bins=1000):
    #TODO only existing values in bins
        '''
        Compress values of series in histogram.
        
        Parameters
        ---------
        bins: int
        
        '''
        self.bins = bins
    
    def fit(self, values):
        '''
        Build histogram for values.
        Parameters
        ----------
        values: pd.Series of numeric
        '''
        hist = np.histogram(values, bins=self.bins)
        self.hist = pd.Series(hist[0], index=hist[1][1:])
    
    def update(self, value):
        '''
        Update histogram with single value.
        value: numeric
        '''
        if not hasattr(self, 'hist'):
            raise AttributeError('update before initial fit')
        
        if value < self.hist.index[0]:
            upd_idx = self.hist.index.tolist()
            upd_idx[0] = value
            self.hist.index = upd_idx

        elif value > self.hist.index[-1]:
            upd_idx = self.hist.index.tolist()
            upd_idx[-1] = value
            self.hist.index = upd_idx

        greater_mask = self.hist.index >= value
        upper_margin = self.hist.loc[greater_mask].index[0]
        self.hist[upper_margin] += 1
        
    def batch_update(self, values):
        #TODO performance test for
        #pd.Series(a).groupby(pd.cut(a, bins=hist.index)).count()
        #instead loop
        '''
        Update histogram with series of new values.
        values: pd.Series of numeric
        '''   
        for v in values.values:
            self.update(v)
        
    def quantile(self, q):
        '''
        Calculate quantile from histogram
        q: float
        From 0 to 1.
        '''
        cdf = self.hist.cumsum() / self.hist.sum()
        quantile = cdf[cdf < q].index[-1]
        return quantile
