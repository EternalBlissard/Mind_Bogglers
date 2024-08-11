import numpy as np 
import pandas as pd 
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import os
books = pd.read_csv('Books.csv')
users = pd.read_csv('Users.csv')
ratings = pd.read_csv('Ratings.csv')
bookCountdf=pd.DataFrame(books['Book-Title'].value_counts())
bookCountdf.reset_index(inplace=True)

print(bookCountdf.head())
for i in tqdm(range(len(bookCountdf))):
    isbn = books[books['Book-Title']==bookCountdf['Book-Title'][i]]
    isbn.reset_index(inplace=True)
    if(len(isbn)>1):
        for j in range(1,len(isbn)):
            ratings.loc[ratings['ISBN'] == isbn['ISBN'][j], "ISBN"] = isbn['ISBN'][0]
            indexAge = books[ (books['ISBN'] == isbn['ISBN'][j])].index
            books.drop(indexAge , inplace=True)
    else:
        break
books.to_csv('Books.csv',index=False)
ratings.to_csv('Ratings.csv',index=False)
