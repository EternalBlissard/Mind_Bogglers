import numpy as np 
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity

def frequentBooksGenerator (books, users,ratings, minNumReviewsBook, minNumReviewsUser):
    ratingsWithBookNameJoined = ratings.merge(books,on='ISBN')
    numRatingdf = ratingsWithBookNameJoined.groupby('Book-Title').count()['Book-Rating'].reset_index()
    numRatingdf.rename(columns={'Book-Rating':'Total-Ratings'},inplace=True)
    userWithMoreThanMinReviews = ratingsWithBookNameJoined.groupby('User-ID').count()['Book-Rating'] > minNumReviewsUser
    frequentReviewers = userWithMoreThanMinReviews[userWithMoreThanMinReviews].index
    frequentRatings = ratingsWithBookNameJoined[ratingsWithBookNameJoined['User-ID'].isin(frequentReviewers) ]
    avgRatingFrequentdf = frequentRatings.groupby('Book-Title')['Book-Rating'].mean().reset_index()
    popularBookFrequentdf = numRatingdf.merge(avgRatingFrequentdf,on='Book-Title')
    popularBookFrequentdf.rename(columns={'Book-Rating':'avg-Rating'},inplace=True)
    booksWithFrequentReviewersANDMinRatings= popularBookFrequentdf[popularBookFrequentdf['Total-Ratings']>=minNumReviewsBook].sort_values('avg-Rating',ascending=False).head(50)
    frequentRatingsFiltered = ratingsWithBookNameJoined[ratingsWithBookNameJoined['Book-Title'].isin(booksWithFrequentReviewersANDMinRatings['Book-Title'])]
    return frequentRatingsFiltered

def recommend(book_name,pt, similarity_scores):
    # index fetch
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        
        data.append(item)
    
    return data

books = pd.read_csv('Books.csv')
users = pd.read_csv('Users.csv')
ratings = pd.read_csv('Ratings.csv')
minNumReviewsUser = 10
minNumReviewsBook = 50
frequentBooksGen = frequentBooksGenerator(books,users,ratings,minNumReviewsBook,minNumReviewsUser)
pt = frequentBooksGen.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')
pt.fillna(0,inplace=True)
similarity_scores = cosine_similarity(pt)
li = recommend("Harry Potter and the Chamber of Secrets (Book 2)",pt, similarity_scores)
print((books[books['Book-Title'] == li[0][0]]))
# print(np.where(books.index==li[0]))
# print(books[['Book-Title']==li[0]])


