from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.feature_extraction import text as txt
from sklearn import decomposition
from time import time


def NMF(bag_of_words, n_topics, n_top_words):
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
        print


def get_tfv(params=None):
    additional_stop_words = ['www','http','\n','\\n','macbook','air','13']
    tfidf = TfidfVectorizer(min_df = 10, 
                         #max_df =.99,
                         #max_features = n_features, 
                         stop_words = txt.ENGLISH_STOP_WORDS.union(additional_stop_words),
                         sublinear_tf=True,
                         ngram_range=(1,2),
                         smooth_idf =True,
                         )
    return tfidf
