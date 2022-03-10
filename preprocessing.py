import pandas as pd
import json

data = pd.read_csv("tmdb_5000_credits.csv") 
data.head()

castDf = pd.DataFrame({'movieId':[], 'person_name':[], 'role':[]})

for index, row in data.iterrows():
    movieId = row['movie_id'] 
    c = pd.DataFrame.from_dict(json.loads(row['cast']))
    for index, row in c.iterrows():
        castDf.loc[len(castDf)] = [str(movieId), row['name'], row['character']]  
print(castDf.head())
print(castDf.count())

castDf.to_csv('castDf.csv')

castDf = pd.read_csv('../input/intermediate/castDf.csv')
print(list(castDf.columns))
castDf.drop(castDf.filter(regex="Unnamed"),axis=1, inplace=True)
print(castDf.head())
print(castDf.count())

d = {}
for i in castDf['person_name']:
    d[i] = d.get(i,0) + 1
    
newdf = pd.DataFrame(list(d.items()),columns = ['person_name','count'])
print(newdf)

newdf = newdf[newdf['count']>5]
newdf

l = list(newdf['person_name'])

castDf = castDf[castDf['person_name'].isin(l)]
castDf.count()

directorDf = pd.DataFrame({'movieId':[], 'person_name':[]})

for index, row in data.iterrows():
    movieId = row['movie_id']
    crew = pd.DataFrame.from_dict(json.loads(row['crew']))
    if (not (crew.empty)):
        nameList = crew[crew['job']=='Director']['name'].values
        if (len(nameList)>0):
            directorDf.loc[len(directorDf)] = [str(movieId), nameList[0]]  
directorDf.count()

d = {}
for i in directorDf['person_name']:
    d[i] = d.get(i,0) + 1


newdf = pd.DataFrame(list(d.items()),columns = ['person_name','count'])
newdf

newdf = newdf[newdf['count']>3]
newdf


l = list(newdf['person_name'])

directorDf = directorDf[directorDf['person_name'].isin(l)]
directorDf.count()


castDf.to_csv('/kaggle/working/roles.csv')
directorDf.to_csv('/kaggle/working/directors.csv')
