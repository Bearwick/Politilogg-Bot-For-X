import feedparser

# Define a class to represent an Atom feed entry
class MessageEntry:
    def __init__(self, entry_id, title, published, updated, link, district, municipality, category, content):
        self.entry_id = entry_id
        self.title = title
        self.published = published
        self.updated = updated
        self.link = link
        self.district = district
        self.municipality = municipality
        self.category = category
        self.content = content

    # Optional: Method to display entry information
    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Published: {self.published}\n"
                f"Link: {self.link}\n"
                f"District: {self.district}\n"
                f"Municipality: {self.municipality}\n"
                f"Category: {self.category}\n"
                f"Content: {self.content}\n")

# Function to fetch and parse the Atom feed and store entries as objects
def fetch_politilogg_feed(feed_url):
    # Parse the Atom feed
    feed = feedparser.parse(feed_url)

    # List to store AtomEntry objects
    entries_list = []
    
    # Check if the feed was parsed correctly
    if feed.bozo == 1:
        print("Failed to parse feed.")
        return entries_list

    # Loop through the feed entries and create AtomEntry objects
    for entry in feed.entries:
        # Extract category values (district, municipality, category)
        district = municipality = category = None
        for tag in entry.get('tags', []):
            if tag.label == "district":
                district = tag.term
            elif tag.label == "municipality":
                municipality = tag.term
            elif tag.label == "category":
                category = tag.term

        # Create an AtomEntry object for each entry
        entry_obj = MessageEntry(
            entry_id=entry.id,
            title=entry.title,
            published=entry.published,
            updated=entry.updated,
            link=entry.link,
            district=district,
            municipality=municipality,
            category=category,
            content=entry.content[0].value if entry.content else None
        )

        # Append the object to the list
        entries_list.append(entry_obj)

    return entries_list