import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
from functools import reduce


def get_lots(n_pages,category):
    lots_df = pd.DataFrame()

    for p in range(1,n_pages):
        try:
            # Make the request
            r = requests.get('https://www.catawiki.it/buyer/api/v1/categories/' + str(
                category) + '/lots?locale=it&per_page=100&page=' + str(p) + '&q=')
            # Extract content
            c = r.content
            # We convert json to dictionary
            result = json.loads(c)
            # we extract the lot
            lots = result["lots"]

            for i in range(len(lots) - 1):
                single_lot_id = pd.DataFrame.from_dict(lots[i], orient='index').T
                lots_df = pd.concat([lots_df, single_lot_id], ignore_index=True)
        except:
            pass

    return lots_df

def extract_ids(lots_df):
    lots_list = lots_df['id'].tolist()
    return  lots_list

def get_item_auction_details(id_list):
    items_df = pd.DataFrame()
    for id in id_list:
        try:
            r = requests.get('https://www.catawiki.it/buyer/api/v1/lots/live?ids=' + str(id))
            c = r.content
            # We convert json to dictionary
            result = json.loads(c)
            # we extract the lot
            lots = pd.DataFrame.from_dict(result["lots"][0], orient='index').T
            items_df = pd.concat([items_df, lots], ignore_index=True)
            print(id)
        except:
            pass
    return items_df


def get_bidding_details(id_list):
    items_df = pd.DataFrame()
    for id in id_list:
        try:
            r = requests.get(
                'https://www.catawiki.com/buyer/api/v3/lots/' + str(id) + '/bidding_block?currency_code=EUR')
            c = r.content
            # We convert json to dictionary
            result = json.loads(c)
            # we extract the lot
            lots = pd.DataFrame.from_dict(result["bidding_block"]['lot'], orient='index').T
            items_df = pd.concat([items_df, lots], ignore_index=True)
            print(id)
        except:
            pass
    return items_df


# Setting some parameters
n_pages = 2
category = 333


# Getting Lots info
lots = get_lots(n_pages, category)
# Extract list of ids
list_of_ids = extract_ids(lots)
# Get Auction Details
auction_details = get_item_auction_details(list_of_ids)
# Get bidding Details
bidding_details = get_bidding_details(list_of_ids)

# enrich info
dfs = [lots, auction_details, bidding_details]
df_final = reduce(lambda left,right: pd.merge(left,right,on='id'), dfs)




# TENTATIVO SCRAPING STIMA DELL'ESPERTO
# Make the request
r = requests.get('https://www.catawiki.com/it/l/51249171')
# Extract content
c = r.content
soup = BeautifulSoup(c)
min_expert_estimate = json.loads(soup.findAll("div",{"class":"lot-details-page-wrapper"})[0].attrs['data-props'])['expertsEstimate']['min']
max_expert_estimate = json.loads(soup.findAll("div",{"class":"lot-details-page-wrapper"})[0].attrs['data-props'])['expertsEstimate']['max']

print('ciao')