class IQRClassifier:
    def __init__(self, n_iqr=2, window='10d'):
        self.n_iqr = n_iqr
        self.window = window
    
    def fit_transform(self, X, warm_start=False):
        
        if warm_start:
            if not (hasattr(self, 'median') or hasattr(self, 'iqr')):
                raise AttributeError('warm start before initial fit')
        else:
            self.__fit__(X)
            
        outlier_mask=self.__get_outlier_mask__(X, self.n_iqr)
        return outlier_mask
            
    def __fit__(self, df):
        self.median = df.median()
        self.iqr = df.quantile(0.75) - df.quantile(0.25)
        self.hist= np.histogram(X, bins=100)

    def __get_outlier_mask__(self, df, n_iqr):
        outlier_mask = df > (self.median + n_iqr * self.iqr)
        outlier_mask |= df < (self.median - n_iqr * self.iqr)
        return outlier_mask
