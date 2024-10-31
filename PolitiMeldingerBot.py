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
            tweet_id = post_tweet(tweet)
            if tweet_id == False:
                return True
            write_json(entry.entry_id, tweet_id)
        
        else:
            # Not implemented since paid higher API level was required for GET requests
            # Implement logic for comparing tweet text (and its comments) and police message text
            # if equal do nothing
            # else post comment on original tweet
            continue


def getSleepTime():
        # Get current time
    current_time = time.localtime()
    
    # Calculate sleep duration to 6 am next day if current time is after 6 am
    if current_time.tm_hour >= 6:
        hours_until_midnight = 24 - current_time.tm_hour  # Remaining hours today
        minutes_until_next_hour = 60 - current_time.tm_min if current_time.tm_min > 0 else 0
        sleep_duration = (hours_until_midnight + 6) * 3600 + minutes_until_next_hour * 60
    else:
        # If before 6 am, calculate sleep to reach 6 am the same day
        sleep_duration = (6 - current_time.tm_hour) * 3600 - current_time.tm_min * 60
    
    # Ensure sleep duration is positive
    if sleep_duration > 0:
        print("Sleeping for " + str(sleep_duration // 60) + " minutes...")
        return sleep_duration
    else:
        return 0


if __name__ == "__main__":
    while True:
        police_feed = fetch_police_feed()
        rate_limit_reached = post_feed(police_feed)

        if rate_limit_reached:
            time.sleep(getSleepTime())
        else:
            time.sleep(60)

