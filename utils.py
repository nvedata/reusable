import numpy as np
import pandas as pd
import datetime

def excel_date(date):
    '''
    Converting date to Excel date or from Excel date
    
    Parameters
    ----------
    date : float, int OR str, datetime.datetime, pd.Timestamp
    Excel date as float/int OR date recognized by pandas. 
    
    Returns
    ----------
    date : float, int OR pd.Timestamp
    Excel date as float/int or date as pd.Timestamp.
    '''
    
    #unlike python, 29.02.1900 exists in excel
    #since 01.03.2019 pandas and excel calendar has equal dates
    cons_date = pd.Timestamp(year=1900, month=3, day=1)
    excel_cons_date = 61
    
    if isinstance(date, (str, datetime.datetime, pd.Timestamp)):
        return (pd.to_datetime(date) - cons_date).days + excel_cons_date
    
    elif isinstance(date, (np.int, np.float)):
        return cons_date + pd.Timedelta(days=date - excel_cons_date)
        
    else:
        raise TypeError('expected str, datetime, float, int, got ', type(date))

def time_derivative(series, time_unit=pd.Timedelta('1s')):
    '''
    Calculate time derivative from right for each point in series. Ignores NaN.
    
    Parameters
    ---------
    series: pd.Series with numeric data with pd.DatetimeIndex
    time_unit: pd.Timedelta
    
    Returns
    ---------
    dsdt : pd.Series
    '''
    
    ds=series.dropna().diff()
    dt=ds.index.to_series().diff()
    dsdt=ds/(dt/time_unit)
    return dsdt

def isnumber(a):
    try:
        float(a)
        return True
    except:
        return False
    
def convert_cyr_month(series):
    '''
    Parameters
    ----------
    series: pd.Series of str
    
    Returns
    ----------
    series: pd.Series
    '''
    series=series.copy()
    
    repl_dict={
    'янв\\w*' : '01',    
    'фев\\w*' : '02',    
    'мар\\w*' : '03',
    'апр\\w*' : '04',
    'май\\w*' : '05',
    'июн\\w*' : '06',
    'июл\\w*' : '07',
    'авг\\w*' : '08',
    'сен\\w*' : '09',
    'окт\\w*' : '10',
    'ноя\\w*' : '11',
    'дек\\w*' : '12'
    }
    
    for k, v in repl_dict.items():
        series=series.str.replace(k, v)
    
    return series
