import numpy as np 
import pandas as pd 
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
def giveAllBooks():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT title from user_book")
    return cur.fetchall()
    # return books
def frequentBooksGenerator (books, users,ratings, minNumReviewsBook, minNumReviewsUser, bookName):
    ratingsWithBookNameJoined = ratings.merge(books,on='isbn')
    numRatingdf = ratingsWithBookNameJoined.groupby('title').count()['rating'].reset_index()
    numRatingdf.rename(columns={'rating':'Total-Ratings'},inplace=True)
    userWithMoreThanMinReviews = ratingsWithBookNameJoined.groupby('user_id').count()['rating'] > minNumReviewsUser
    frequentReviewers = userWithMoreThanMinReviews[userWithMoreThanMinReviews].index
    frequentRatings = ratingsWithBookNameJoined[ratingsWithBookNameJoined['user_id'].isin(frequentReviewers) ]
    avgRatingFrequentdf = frequentRatings.groupby('title')['rating'].mean().reset_index()
    popularBookFrequentdf = numRatingdf.merge(avgRatingFrequentdf,on='title')
    popularBookFrequentdf.rename(columns={'rating':'avg-Rating'},inplace=True)
    booksWithFrequentReviewersANDMinRatings= popularBookFrequentdf[popularBookFrequentdf['Total-Ratings']>=minNumReviewsBook].sort_values('avg-Rating',ascending=False)
    # print(booksWithFrequentReviewersANDMinRatings.columns)
    # print(ratingsWithBookNameJoined.columns)
    # if(bookName not in booksWithFrequentReviewersANDMinRatings['title']):
    #     booksWithFrequentReviewersANDMinRatings.loc[len(booksWithFrequentReviewersANDMinRatings)] = ratingsWithBookNameJoined[ratingsWithBookNameJoined['title']==bookName] 
    books_to_include = list(booksWithFrequentReviewersANDMinRatings['title']) + [bookName]
    frequentRatingsFiltered = ratingsWithBookNameJoined[ratingsWithBookNameJoined['title'].isin(books_to_include)]
    return frequentRatingsFiltered

def recommend(book_name,pt, similarity_scores,Len,books):
    # index fetch
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:Len]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['author'].values))
        item.extend(list(temp_df.drop_duplicates('title')['year'].values))
        item.extend(list(temp_df.drop_duplicates('title')['publisher'].values))
        item.extend(list(temp_df.drop_duplicates('title')['image_l'].values))
        
        data.append(item)
    
    return data

def giveBooks(minNumReviewsUser,minNumReviewsBook,bookName,Len):
    con = sqlite3.connect("db.sqlite3")
    books = pd.read_sql_query("SELECT * from user_book", con)
    users = pd.read_sql_query("SELECT * from user_usermanager", con)
    ratings = pd.read_sql_query("SELECT * from user_rating", con)
    # print("Books", len(books))
    # print("Users",len(users))
    # print("Ratings",len(ratings))
    ratings.rename(columns={'isbn_id':'isbn'},inplace=True)
    ratings.rename(columns={'user_id_id':'user_id'},inplace=True)
    # print(ratings.columns)
    minNumReviewsUser = 100
    minNumReviewsBook = 100
    frequentBooksGen = frequentBooksGenerator(books,users,ratings,minNumReviewsBook,minNumReviewsUser,bookName)
    # frequentBooksGen = frequentBooksGen.reset_index()
    # with open('test.txt','w') as f:
    #     for i in range(len(frequentBooksGen)):
    #         f.write(frequentBooksGen['title'][i])
    #         f.write('\n')
    # f.close()
    pt = frequentBooksGen.pivot_table(index='title',columns='user_id',values='rating')
    pt.fillna(0,inplace=True)
    print(len(frequentBooksGen))

    similarity_scores = cosine_similarity(pt)
    li = recommend(bookName,pt, similarity_scores,Len+1,books)
    # print(li)
    # print((books[books['Book-Title'] == li[0][0]]))
    # print(np.where(books.index==li[0]))
    # print(books[['Book-Title']==li[0]])

    return li
# giveBooks(10,10,"Harry Potter and the Chamber of Secrets (Book 2)",5)