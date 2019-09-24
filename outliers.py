class IQRClassifier:
    def __init__(self, n_iqr=2, window='10d'):
        '''
        Classifier of outliers in series by interquantile range.
        
        Parameters
        ---------
        n_iqr: float
        #TODO rolling
        window: str 
        
        '''
        self.n_iqr = n_iqr
        self.window = window
    
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
            
            #TODO performance test for
            #pd.Series(a).groupby(pd.cut(a, bins=hist.index)).count()
            #instead loop
            for v in df.values:
                self.__update__(v)
            
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
        #TODO only existing values in bins
        hist = np.histogram(df, bins=1000)
        self.hist = pd.Series(hist[0], index=hist[1][1:])

    def __update__(self, value):
        '''
        Update clasifier with new value in df.
        '''
        if value < self.hist.index[0]:
            self.hist.index.values[0] = value
            self.hist.iloc[0] += 1
        elif value > self.hist.index[-1]:
            self.hist.index.values[-1] = value
            self.hist.iloc[-1] += 1
        else:
            greater_mask = self.hist.index >= value
            upper_margin = self.hist[greater_mask].index[0]
            self.hist[upper_margin] += 1
            
        self.median = self.__hist_quantile__(self.hist, 0.5)
        self.iqr = self.__hist_quantile__(self.hist, 0.75) - self.__hist_quantile__(self.hist, 0.25)
            
    def __hist_quantile__(self, hist, q):
        '''
        Calculate quantile from histogram
        '''
        cdf = hist.cumsum() / hist.sum()
        quantile = cdf[cdf < q].index[-1]
        return quantile

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
