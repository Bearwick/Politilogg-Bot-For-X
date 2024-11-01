from PolitiloggAPI import fetch_politilogg_feed
from Storage import getTweet, write_json
from XAPI import post_tweet
import time

politilogg_feed_url = "https://api.politiet.no/politiloggen/v1/atom?districts="


def fetch_police_feed():
    try:
        return fetch_politilogg_feed(politilogg_feed_url)

    except Exception as e:
        print(f"Error fetching feed: {e}")

def create_tweet(entry):
    category = entry.category.replace(" ", "_") if " " in entry.category else entry.category

    tweet_content = f"#{entry.municipality} #{category}\n{entry.content}\n\n{entry.link}"
    
    # Truncate if tweet exceeds 280 characters
    if len(tweet_content) > 280:
        available_length = 280 - len(f"#{entry.municipality} #{category}\n\n{entry.link}") - 3  # 3 for "..."
        truncated_text = entry.content[:available_length] + "..."
        tweet_content = f"#{entry.municipality} #{category}\n{truncated_text}\n\n{entry.link}"
    
    return {"text": tweet_content}

def post_feed(police_feed):
    for entry in police_feed:
        tweet_data = getTweet(entry.entry_id)
        if tweet_data == None:
            tweet = create_tweet(entry)
            tweet_id, sleep_duration = post_tweet(tweet)
            if tweet_id == False:
                return sleep_duration
            write_json(entry.entry_id, tweet_id)
            return sleep_duration
        
        else:
            # Not implemented since paid higher API level was required for GET requests
            # Implement logic for comparing tweet text (and its comments) and police message text
            # if equal do nothing
            # else post comment on original tweet
            continue


if __name__ == "__main__":
    while True:
        police_feed = fetch_police_feed()
        sleep_duration = post_feed(police_feed)
        print("sleeping for {} minutes".format(sleep_duration//60))
        time.sleep(sleep_duration)

