import requests
import re
import csv  

api_tweets = "https://api.twitter.com/2/users/72293042/tweets?tweet.fields=author_id,conversation_id,created_at,in_reply_to_user_id,referenced_tweets&expansions=author_id,in_reply_to_user_id,referenced_tweets.id&user.fields=name,username"
api_conversation = "https://api.twitter.com/2/tweets/search/recent?query=conversation_id:"
bearer "" #YOUR BEARER TOKEN
headers = {'Authorization' : 'Bearer {}'.format(bearer)}

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)


print('start retrieving data...')

response = requests.get(api_tweets, headers=headers)
result_tweets = response.json()
header = ['no', 'comment']
comments_data = []
i = 0;
for data in result_tweets['data'] :
    response = requests.get(api_conversation+data['conversation_id'], headers=headers)
    result_conversation = response.json()

    if result_conversation['meta']['result_count'] > 0 :
        for conversation in result_conversation['data'] :
            i=i+1
            conversation_text = conversation['text']
            conversation_text = emoji_pattern.sub(r'', conversation_text)
            row = [i,conversation_text]
            comments_data.append(row)

print('end retrieving data')

print('start writing file...')

with open('comments.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(comments_data)

print('end writing file')
