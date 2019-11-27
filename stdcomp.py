import pandas as pd

class StdCompressor:
    '''Object for storing distribution statistics for evaluating standard deviation on streaming dataframes.
    Standard deviation for each series in dataframe is stored in in .std attribute.
    '''
    
    def __init__(self):
        pass
    
    def fit(self, df, warm_start=False):
        '''
        Calculate standard deviations for dataframe.
        
        Parameters
        ----------
        df: pd.DataFrame of numeric
        warm_start: bool
        If True update object with new data in df, if False fit only on data in df and reset previous state of the object.
        '''
        
        n = df.count()
        s = df.sum()
        qs = (df ** 2).sum()
        
        if warm_start:
            
            if not hasattr(self, 'count'):
                raise AttributeError('update before initial fit')
                
            self.count += n
            self.sum += s
            self.qsum += qs
            self.std = self.calc_std(self.count, self.sum, self.qsum)
            
        else:
            self.count = n
            self.sum = s
            self.qsum = qs
            self.std = df.std()
        
    def calc_std(self, n, summ, q_summ):
        '''Alternative algorithm for calculating standard deviation for streaming dataframe
        
        n: int or pd.Series of int
        df.count()
        
        summ: float or pd.Series of float
        df.sum()
        
        q_summ: float or pd.Series of float
        (df**2).sum()
        '''
        std = ((n * q_summ - summ ** 2) / (n * (n - 1)))**0.5
        
        return std
