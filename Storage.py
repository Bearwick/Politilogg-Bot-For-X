import json
import os
from collections import OrderedDict

def read_json(filename="police_tweet_map.json"):
    """
    Reads a JSON file and returns the data as a dictionary.
    If the file does not exist, creates an empty JSON file and returns an empty dictionary.
    """
    if not os.path.exists(filename):
        # Create an empty JSON file
        with open(filename, "w") as file:
            json.dump({}, file)
        return {}

    with open(filename, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}

    return data

def write_json(police_message_id, tweet_id, comment_ids=None, filename="police_tweet_map.json"):
    """
    Writes or updates a dictionary entry with a new police_message_id. 
    The entry consists of a tweet_id and an optional list of comment tweet IDs.
    """
    # Load existing data
    data = read_json(filename)
    
    # Define the structure for the police message
    data[police_message_id] = {
        "tweet": tweet_id,
        "comments": comment_ids if comment_ids else []
    }

    # Check the file size and update with trimmed data if needed
    data = check_file_size(data, filename)

    # Write the updated dictionary back to the JSON file
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def getTweet(police_message_id, filename="police_tweet_map.json"):
    """
    Retrieves the tweet information associated with a given police_message_id from the JSON file.
    If the file does not exist, it creates an empty JSON file.
    Returns a dictionary with 'tweet_id', 'comments', and 'has_comments' fields.
    """
    # Load data from the JSON file
    data = read_json(filename)

    # Retrieve entry if it exists
    entry = data.get(police_message_id)
    if entry:
        tweet_id = entry.get("tweet")
        comments = entry.get("comments", [])
        has_comments = len(comments) > 0  # True if there are comments, False otherwise

        return {
            "tweet_id": tweet_id,
            "comments": comments,
            "has_comments": has_comments
        }
    return None  # Return None if the police_message_id does not exist

def check_file_size(data, filename="police_tweet_map.json", max_records=100000, records_to_remove=40000):
    """
    Checks if the JSON file has more than max_records. If so, removes the oldest
    records_to_remove records from the data and returns the updated data.
    """
    # Only proceed if the data exceeds max_records
    if len(data) > max_records:
        print(f"File has {len(data)} records, trimming to {max_records - records_to_remove}.")

        # Convert to an OrderedDict to maintain insertion order (Python 3.7+ dicts preserve order)
        ordered_data = OrderedDict(data)

        # Remove the oldest records
        for _ in range(records_to_remove):
            ordered_data.popitem(last=False)

        return ordered_data  # Return the trimmed data

    return data  # Return data as-is if no trimming was needed
