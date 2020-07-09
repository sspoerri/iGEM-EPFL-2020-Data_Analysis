import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

def get_dataframe_from_xlsx(path):
    df = pd.read_excel(path)

    df_list = np.split(df, df[df.isnull().all(1)].index)
    df_list = np.delete(df_list,0)

    df_list_new = []
    for df in df_list:
        df.dropna(how='all') #remove first empty line
        df.columns = df.iloc[1] #set header
        df = df.iloc[2:] #delete first row (header)
        df = df.set_index('Kinetic read') #set index
        df = df[df.columns.dropna()] #remove empty columns
        df = df.dropna() #remove all empty lines
        df_list_new.append(df)
    return pd.concat(df_list_new,axis=1)

def logistic(x,x0,y0,k,L):
    return L/(1+np.exp(-k*(x-x0))) + y0

def convert_time(time):
    h,m,s = (time.hour,time.minute,time.second)
    return int(h) * 3600 + int(m) * 60 + int(s)

def convert_time_list(list):
    l = [] 
    for t in list:
        l.append(convert_time(t))
    return l

def get_fit(df,col):
    t = convert_time_list(np.array(df.index))
    od = np.array(df[col],dtype=float)
    init_vals = [30000, 0, 0.00001, 2]
    try:
        best_vals, covar = curve_fit(logistic, t, od, p0=init_vals)
        return best_vals
    except:
        return [0,0,0,0]
    
def get_series(df,n,r,c):
    return [get_fit(df,r+str(c+i))[n] for i in range(6)]