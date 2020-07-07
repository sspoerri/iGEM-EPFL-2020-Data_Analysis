import pandas as pd
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
    
df = get_dataframe_from_xlsx('data/plate1.xlsx')
df[['A1', 'B1', 'C1']].plot() #select columns here
plt.show()