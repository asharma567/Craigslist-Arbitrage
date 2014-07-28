import numpy as np

def make_pricing_panel(df_recs, pxs):    
    '''
    INPUT   DataFrame with field url_to_post ie hyperlinks to posts
    OUTPUT  DataFrame with cleansed of dead links
    '''    
    
    df_recs['year'] = df_recs['year'].astype(int)
    df_recs['ebay_price'] = df_recs['year'].apply(lambda x: pxs[x][0])
    df_recs['num_auctions'] = df_recs['year'].apply(lambda x: pxs[x][2])
    df_recs['spread'] = df_recs['ebay_price'] - df_recs['px']

    return df_recs

def find_indices(y_hat, y):
    '''
    Calculate the residuals versus the model and sorts by largest negatives first
    INPUT  numpy array predicted (modeled) points and observed points
    OUTPUT numpy array of sorted indices
    '''
    delta = y - y_hat
    indices = np.argsort(delta)

    return indices
