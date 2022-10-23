from numpy import number
import requests
import re
import csv 
import json
import demoji

import pandas as pd

#region Functions and Data Cleaning
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

def cleanup_twitter_comment(comment):
    # conversation_text = conversation['text'].replace('\n','\\n').replace('\t','\\t')
    print(f"before : {comment}")
    allowed_char = 'A-Za-z0-9_?! '

    comment = demoji.replace_with_desc(comment," ")
    comment = emoji_pattern.sub(r'', comment) #remove emoji
    comment = re.sub("@[A-Za-z0-9_]+","", comment) #remove mentions
    comment = re.sub("#[A-Za-z0-9_]+","", comment) #remove hashtags
    comment = re.sub("http.*","", comment) #remove hashtags

    comment = re.sub(f"[^{allowed_char}]+","", comment)
    #TODO remove duplicated characters. example : sayaaaa, bagus miiiinnnnn

    print(f"after : {comment}")
    return comment

def print_curl(url):
    # curl -H "Authorization: OAuth <ACCESS_TOKEN>" http://www.example.com
    print(f"curl -H 'Authorization: Bearer {bearer}' '{url}'")

#endregion

#region Config
with open("config.json") as json_data_file:
    config = json.load(json_data_file)

twitter_config = config['twitter_api']
twitter_api_host = twitter_config['host']
max_result = twitter_config['max_result']
bearer = twitter_config['bearer']
start_time = twitter_config['start_time']
end_time = twitter_config['end_time']
tweet_fields = twitter_config['tweet_fields']
expansions = twitter_config['expansions']
user_fields = twitter_config['user_fields']
user_id = twitter_config['user_id']
#endregion

#region API Setup
# setup url to get tweets of tokopedia.
# this request will return conversation id which will be used to get conversation details
api_tweets = (
                f"{twitter_api_host}/2/users/{user_id}/tweets?"
                f"max_results={max_result}"
                f"&start_time={start_time}"
                f"&end_time={end_time}"
                f"&tweet.fields={tweet_fields}"
                f"&expansions={expansions}"
                f"&user.fields={user_fields}"
            )

# setup url to get conversation for each tweet based on conversation id
api_conversation = (
                        f"{twitter_api_host}/2/tweets/search/recent?"
                        f"&tweet.fields=referenced_tweets"
                        f"&query=conversation_id:"
                    )

# setup authorization header
headers = {'Authorization' : f'Bearer {bearer}'}
#endregion

print('start retrieving data...')
loop = True
page = 1
api_tweets_loop = api_tweets
comments_array = []
tweets_array = []

while loop == True:
    print(f"page {page}")

    print(f"Retrieving timeline from {api_tweets_loop} ...")
    #get tweet list from timeline
    response = requests.get(api_tweets_loop, headers=headers)

    result_tweets = response.json()
    # header = ['no', 'comment', 'tweet']
    i = 0;

    for data in result_tweets['data'] :
        tweet = data['text'];

        #append url with conversation id to get conversation details
        url_conversation = api_conversation+data['conversation_id']

        #get conversation details
        print(f"Retrieving conversation from {url_conversation} ...")
        response = requests.get(url_conversation, headers=headers)
        print_curl(url_conversation)
        result_conversation = response.json()
        
        if response.status_code != 200 :
            print("Error")
            print(result_conversation)
            loop = False
            break
        
        #TODO separate this process so that there is layer for retrieving data 
        # and data cleaning layer
        if result_conversation['meta']['result_count'] > 0 :
            for conversation in result_conversation['data'] :
                i=i+1
                conversation_text = conversation['text']
                conversation_text = cleanup_twitter_comment(conversation['text'])
                #Pengen handphone #OPPOReno7Series5G karena mau kasih ibu handphone baru yang keren dan kece abis.
                
                if conversation_text not in comments_array and conversation_text is not None and conversation_text.strip():
                    comments_array.append(conversation_text.strip())
                    tweets_array.append(tweet)
    
    if 'next_token' in result_tweets['meta'] and result_tweets['meta']['next_token'] is not None :
        page = page+1
        next_token = result_tweets['meta']['next_token']
        api_tweets_loop = f"{api_tweets}&pagination_token={next_token}"
    else:
        loop = False

print('end retrieving data')

print('start writing file...')

comments_data = pd.DataFrame({'comments':comments_array,'tweet':tweets_array})

datatoexcel = pd.ExcelWriter('october_2022.xlsx')
comments_data.to_excel(datatoexcel)
datatoexcel.save()

print('end writing file')
