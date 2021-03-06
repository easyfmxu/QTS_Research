import quandl
import datetime
import pickle as pkl
from pathlib import Path
import numpy as np
import os

class Pricing_Database:
    current_date = np.datetime64(datetime.date.today())
    pricing_date = np.datetime64(datetime.date.today())
    trading_days = 250

    def __init__(self):
        pass

def add_pricing_date(i=0,in_place=True):
    if in_place:
        Pricing_Database.pricing_date += np.timedelta64(i, 'D')
        return None
    else:
        return Pricing_Database.pricing_date + np.timedelta64(i, 'D')

def add_date(npdate,i=0):
    return npdate + np.timedelta64(i,'D')

def set_pricing_date(dt):
    Pricing_Database.pricing_date = dt

def to_datetime(dt):
    return datetime.datetime(dt.tolist())

def date_diff(dt1,dt2):
    if(isinstance(dt1,int)):
        dt1 = add_pricing_date(dt1,in_place=False)
    if(isinstance(dt2,int)):
        dt2 = add_pricing_date(dt2,in_place=False)

    return (dt2-dt1)/np.timedelta64(1,'D')

class Cache:
    cache_dict = dict()
    def __init__(self):
        pass

    def get_price_quandl(self,ticker ):
        try:
            df = quandl.get("WIKI/"+ticker)
        except quandl.errors.quandl_error.NotFoundError as e:
            print("WIKI/"+ticker)
            raise e

        df = df[['Adj. Open',  'Adj. High',  'Adj. Low',  'Adj. Close', 'Adj. Volume']]
        df.rename(columns={'Adj. Open':'Open','Adj. High':'High',  'Adj. Low':'Low',  'Adj. Close':'Close', 'Adj. Volume':'Volume'},inplace = True)
        df.dropna(inplace=True)
        return df

    def get_ticker_data(self,ticker):
        key = ticker + str(Pricing_Database.current_date)
        if key in Cache.cache_dict.keys():
            return Cache.cache_dict[key]

        try:
            directory = os.path.dirname(__file__) + "\\data"
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError as exception:
            pass

        file_name = os.path.dirname(__file__) + "\\data\\"+ ticker + str(Pricing_Database.current_date)
        my_file = Path(file_name)
        if my_file.is_file():
            with open(file_name,"rb") as file:
                data = pkl.load(file)
        else:
            data = self.get_price_quandl(ticker)
            with open(file_name,"wb") as file:
                pkl.dump(data,file,protocol=pkl.HIGHEST_PROTOCOL)

        Cache.cache_dict[key] = data
        return data

    def get_ticker_dates(self,ticker):
        data = self.get_ticker_data(ticker)
        dates = data.index.values
        return dates

