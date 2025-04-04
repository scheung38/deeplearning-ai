import sys
import requests
from collections import Counter
import re

# Function to get pages in a category
def get_pages_in_category(category):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": "max",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return [member['title'] for member in data['query']['categorymembers']]

# Function to get the text of a Wikipedia page
def get_page_text(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
        "format": "json"
    }
    response = requests.get(url, params=params)
    pages = response.json()['query']['pages']
    page = next(iter(pages.values()))
    return page.get('extract', '')

# Function to clean and split text into words
def clean_and_split_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    words = text.lower().split()
    return words

# Function to count non-common words
def count_non_common_words(words):
    common_words = set(['the', 'is', 'in', 'and', 'to', 'of', 'a', 'for', 'on', 'with', 'as', 'by', 'at', 'an'])
    return Counter(word for word in words if word not in common_words)

# Main function
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python wiki_category_analysis.py <Wikipedia_Category>")
        sys.exit(1)

    category = sys.argv[1]
    pages = get_pages_in_category(category)
    cumulative_counter = Counter()

    for page in pages:
        text = get_page_text(page)
        words = clean_and_split_text(text)
        cumulative_counter.update(count_non_common_words(words))

    for word, count in cumulative_counter.most_common():
        print(f"{word}: {count}")
