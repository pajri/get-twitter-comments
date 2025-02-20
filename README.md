# Twitter Data Retrieval and Cleaning Script

## Description
This script retrieves tweets from the Twitter API, extracts conversations, cleans the data by removing unwanted characters, and stores the results in an Excel file.

## Requirements
- Python 3.x
- The following Python libraries:
  - `requests`
  - `re`
  - `csv`
  - `json`
  - `demoji`
  - `pandas`

## Setup
1. Install the required dependencies using:
   ```bash
   pip install requests pandas demoji
   ```
2. Create a `config.json` file with the following structure:
   ```json
   {
       "twitter_api": {
           "host": "https://api.twitter.com",
           "max_result": 100,
           "bearer": "YOUR_BEARER_TOKEN",
           "start_time": "YYYY-MM-DDTHH:mm:ssZ",
           "end_time": "YYYY-MM-DDTHH:mm:ssZ",
           "tweet_fields": "text,author_id",
           "expansions": "author_id",
           "user_fields": "name,username",
           "user_id": "YOUR_USER_ID"
       }
   }
   ```

## Usage
1. Run the script using:
   ```bash
   python twitter_data.py
   ```
2. The script retrieves tweets, processes conversations, and cleans up comments.
3. The cleaned data is saved in an Excel file named `october_2022.xlsx`.

## Features
- Retrieves tweets and their associated conversations
- Cleans comments by removing emojis, mentions, hashtags, and URLs
- Saves the cleaned data in an Excel file for further analysis

## Notes
- Ensure you have a valid Twitter API bearer token in the `config.json` file.
- Modify the `config.json` parameters as needed for different date ranges and tweet fields.

## License
This script is for personal and educational use. Modify and distribute as needed.

