from sklearn.feature_extraction import text 
from sklearn import decomposition
from time import time

'''
Used for EDA
clustering on the posting's body to find interesting trends within the sample "good" deals
eg What were common words or phrases being used? 
Why were people leaving this items at a discount?
'''


def NMF(bag_of_words, n_topics, n_top_words):

    #timing the clustering process
    t0 = time()
    tfidf = get_tfv()

    #NMF for grouped comments
    counts = tfidf.fit_transform(bag_of_words)
    X = TfidfTransformer().fit_transform(counts)
    vocab = tfidf.get_feature_names()

    nmf = decomposition.NMF(n_components=n_topics).fit(X)

    print("done in %0.3fs." % (time() - t0))
    for topic_idx, topic in enumerate(nmf.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join( [vocab[i] for i in topic.argsort()[:-n_top_words - 1:-1]] ))        


def get_tfv():
    '''
    Bag of words method used for topic detection within sample of "good" deals and all postings
    '''
    additional_stop_words = ['www','http','\n','\\n','macbook','air','13']
    tfidf = text.TfidfVectorizer(min_df=10, 
                                     stop_words=text.ENGLISH_STOP_WORDS.union(additional_stop_words),
                                     sublinear_tf=True,
                                     ngram_range=(1,2),
                                     smooth_idf=True,
                                     )
    return tfidf
