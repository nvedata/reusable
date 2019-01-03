def excel_date(date):
    '''Converting date to Excel date or from Excel date
    
    Parameters
    ----------
    date : float, int OR str, datetime.datetime, pd.Timestamp
    Excel date as float/int OR date recognized by pandas. 
    
    Returns
    ----------
    date : float, int OR pd.Timestamp
    Excel date as float/int or date as pd.Timestamp.
    '''
    
    if isinstance(date, (str, datetime.datetime, pd.Timestamp)):
        return (pd.to_datetime(date)-pd.Timestamp(year=1899, month=12, day=31)).days+1
    
    elif isinstance(date, (np.int, np.float)):
        return pd.Timestamp(year=1899, month=12, day=31)+pd.Timedelta(days=date-1)
        
    else:
        raise TypeError('expected str, datetime, float, int, got ', type(date))
