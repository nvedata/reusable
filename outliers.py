import numpy as np
import pandas as pd
from tdigest import TDigest
from histcomp import HistogramCompressor

class IQRClassifier:
    '''Interquantile range classifier'''
    def __init__(self, n_iqr=2, window='10d', method='histcomp'):
        #TODO rolling
        '''Classifier of outliers in series by interquantile range.
        
        Parameters
        ---------
        n_iqr: float
        window: str
        method: str
        'histcomp' or 'tdigest' algorithm for streaming quantiles
        
        '''
        self.n_iqr = n_iqr
        self.window = window
        self.method = method
    
    def fit_predict(self, df, warm_start=False):
        '''
        Fit classifier and returns outlier mask.
        
        Parameters
        ---------
        df: pd.Series of numeric
        warm_start: bool
        If True update classifier with new data in df, if False fit classifier only on data in df and reset previous state of IQRClassifier.
        
        Returns
        ---------
        outlier_mask: pd.Series with same index as df of bool
        '''

        if warm_start:
            if not hasattr(self, 'median'):
                raise AttributeError('warm start before initial fit')
            
            self.__update__(df)
            
        else:
            self.__fit__(df)
                
            
        outlier_mask=self.predict(df)
        return outlier_mask
            
    def __fit__(self, df):
        '''
        Fit classifier only on data in df and reset previous state of IQRClassifier.
        '''
        self.median = df.median()
        self.iqr = df.quantile(0.75) - df.quantile(0.25)
        
        if self.method == 'histcomp':
            self.compressor=HistogramCompressor()
            self.compressor.fit(df)
            
        elif self.method == 'tdigest':
            self.compressor=TDigest()
            self.compressor.batch_update(df)

    def __update__(self, values):
        '''
        Update clasifier with new value in df.
        '''
        
        self.compressor.batch_update(values)
        
        if self.method == 'histcomp':
            self.median = self.compressor.quantile(0.5)
            self.iqr = self.compressor.quantile(0.75) - self.compressor.quantile(0.25)
            
        elif self.method == 'tdigest':
            self.median = self.compressor.percentile(50)
            self.iqr = self.compressor.percentile(75) - self.compressor.percentile(25)
            
    def predict(self, df):
        '''
        Returns outlier mask without update classifier
        
        Parameters
        ---------
        df: pd.Series of numeric
        
        Returns
        ---------
        outlier_mask: pd.Series with same index as df of bool
        '''
        outlier_mask = df > (self.median + self.n_iqr * self.iqr)
        outlier_mask |= df < (self.median - self.n_iqr * self.iqr)
        return outlier_mask
