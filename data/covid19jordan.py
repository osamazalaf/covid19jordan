import pandas as pd

cd4=pd.read_csv('Coviddaily.csv')


cd=cd4.groupby('City').sum()['Confirmed'].reset_index()
cd['OBJECTID']=cd4['OBJECTID']


cd=cd.T
t=list(cd.columns)
t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10],t[11]=t[8],t[11],t[4],t[0],t[10],t[1],t[3],t[7],t[5],t[9],t[6],t[2]
cd=cd[t]
cd=cd.T.reset_index()

cd.drop('index',axis=1,inplace=True)

cd.to_csv('covidmap.csv')

