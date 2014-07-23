def grab_data_for_analysis(metro):
    
    #Grabbing the data
    all_metro_df = pd.read_sql_table('training' + metro + '_df', engine)
    print 'Total scraped - ',len(all_metro_df)
    all_metro_df = remove_duplicates(all_metro_df,'heading')
    
    #Removing the NA
    df = all_metro_df[all_metro_df['year'] != 'NaN']
    tmpdf = all_metro_df[all_metro_df['year'] == 'NaN']
    df = remove_key_words(df, 'repair')
    df = price_filtering(df, 1300, 350)
    print 'Filtered down - ', len(df)
    return df

def modeled_indices(X, y, model_type= 'RF'):
    
    model = {
                'L1'        : Lasso(alpha= 1, tol= .01, warm_start= False, positive= False),
                'SVR_lin'   : SVR('linear', C= 6.3095734448019298, gamma= 0.1, degree= 1),
                'RF'        : RandomForestRegressor(min_samples_split= 2, n_estimators= 10),
            }
    y_hat = model[model_type].fit(X, y).predict(X)
    
    return find_indices(y_hat, y)

def make_pricing_panel(df_recs, pxs= PXS):    
    
    ebay_price = lambda x: pxs[x][0]
    num_auctions = lambda x: pxs[x][2]
    df_recs['year'] = df_recs['year'].astype(int)
    
    df_recs['ebay_price'] = df_recs['year'].apply(ebay_price)
    df_recs['num_auctions'] = df_recs['year'].apply(num_auctions)
    df_recs['spread'] = df_recs['ebay_price'] - df_recs['px']
    return df_recs

