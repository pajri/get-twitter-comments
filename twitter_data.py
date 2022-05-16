from numpy import number
import requests
import re
import csv 
import json

import pandas as pd

#region Functions

def cleanup_twitter_comment(comment):
    comment = re.sub("@[A-Za-z0-9_]+","", comment) #remove mentions
    comment = re.sub("#[A-Za-z0-9_]+","", comment) #remove hashtags
    return comment

def print_curl(url):
    # curl -H "Authorization: OAuth <ACCESS_TOKEN>" http://www.example.com
    print(f"curl -H 'Authorization: Bearer {bearer}' '{url}'")

#endregion

#region Config
with open("config.json") as json_data_file:
    config = json.load(json_data_file)

twitter_config = config['twitter_api']
#endregion

twitter_api_host = "https://api.twitter.com"
max_result = 20
start_time = "2022-01-01T00:00:00Z"
end_time = "2022-05-16T00:00:00Z"
tweet_fields = "author_id,conversation_id,created_at,in_reply_to_user_id,referenced_tweets"
expansions = "author_id,in_reply_to_user_id,referenced_tweets.id"
user_fields = "name,username"

api_tweets = (
                f"{twitter_api_host}/2/users/72293042/tweets?"
                f"max_results={max_result}"
                f"&start_time={start_time}"
                f"&end_time={end_time}"
                f"&tweet.fields={tweet_fields}"
                f"&expansions={expansions}"
                f"&user.fields={user_fields}"
            )

api_conversation = (
                        f"{twitter_api_host}/2/tweets/search/recent?"
                        f"&tweet.fields=referenced_tweets"
                        f"&query=-from:tokopedia conversation_id:"
                    )
bearer = twitter_config['bearer']
headers = {'Authorization' : f'Bearer {bearer}'}

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)


print('start retrieving data...')
loop = True
page = 1
api_tweets_loop = api_tweets
comments_array = []


while loop == True:
    print(f"page {page}")
    response = requests.get(api_tweets_loop, headers=headers)

    result_tweets = response.json()
    header = ['no', 'comment']
    i = 0;

    for data in result_tweets['data'] :
        url_conversation = api_conversation+data['conversation_id']
        response = requests.get(url_conversation, headers=headers)
        print_curl(url_conversation)
        
        result_conversation = response.json()
        
        if response.status_code != 200 :
            print("Error")
            print(result_conversation)
            loop = False
            break

        if result_conversation['meta']['result_count'] > 0 :
            for conversation in result_conversation['data'] :
                i=i+1
                # conversation_text = conversation['text'].replace('\n','\\n').replace('\t','\\t')
                # conversation_text = emoji_pattern.sub(r'', conversation_text)
                conversation_text = conversation['text']
                conversation_text = cleanup_twitter_comment(conversation['text'])
                #Pengen handphone #OPPOReno7Series5G karena mau kasih ibu handphone baru yang keren dan kece abis.

                if conversation_text not in comments_array :
                    comments_array.append(conversation_text)
    
    if 'next_token' in result_tweets['meta'] and result_tweets['meta']['next_token'] is not None :
        page = page+1
        next_token = result_tweets['meta']['next_token']
        api_tweets_loop = f"{api_tweets}&pagination_token={next_token}"
    else:
        loop = False



print('end retrieving data')

print('start writing file...')

comments_data = pd.DataFrame({'comments':comments_array})

datatoexcel = pd.ExcelWriter('comments_2022.xlsx')
comments_data.to_excel(datatoexcel)
datatoexcel.save()

print('end writing file')
