from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import csv

def logistic(x,x0,y0,k,L):
    return L/(1+np.exp(-k*(x-x0))) + y0

def convert_time(time):
    h,m,s = time.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def convert_time_list(list):
    l = [] 
    for t in list:
        l.append(convert_time(t))
    return l
    
def get_columns_from_csv(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        headers = []
        c = []
        for row in csv_reader:
            if line_count == 0:
                headers = row
                c = [[] for i in range(len(row))]
                line_count += 1
            else:
                for i in range(len(row)):
                    c[i].append(row[i])
                line_count += 1
        return c

data = get_columns_from_csv('data/plate1.csv')
x = np.array(convert_time_list(data[0]))

for i in range(1,len(data)):
    od = np.array(data[i],dtype=float)

    init_vals = [30000, 0, 0.00001, 2]  # for [amp, cen, wid]
    best_vals, covar = curve_fit(logistic, x, od, p0=init_vals)
    print(f'x0: {best_vals[0]}, y0: {best_vals[1]}, k: {best_vals[2]}, L: {best_vals[3]}')
    
    plt.title(f'Column {i}')
    plt.plot(x,od)
    plt.plot(x,logistic(x,best_vals[0],best_vals[1],best_vals[2],best_vals[3]))
    plt.legend(['data','fit'])
    plt.show()