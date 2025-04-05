import sys
import requests
from collections import Counter
import re
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend URL
    # allow_origins=["*"], # set this to frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to load cache
def load_cache():
    if os.path.exists("cache.json"):
        with open("cache.json", "r") as file:
            return json.load(file)
    return {}

# Function to save cache
def save_cache(cache):
    with open("cache.json", "w") as file:
        json.dump(cache, file)

# Function to get pages in a category
def get_pages_in_category(category):
    cache = load_cache()
    if category in cache and 'pages' in cache[category]:
        return cache[category]['pages']
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
    pages = [member['title'] for member in data['query']['categorymembers']]
    cache[category] = {
        'pages': pages
    }
    save_cache(cache)
    return pages

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
    return Counter(word for word in words if word not in common_words and not word.isdigit() and not word.isnumeric())

def process_category(category):
    cache = load_cache()
    if category in cache and 'word_counts' in cache[category]:
        cumulative_counter = Counter(cache[category]['word_counts'])
    else:
        pages = get_pages_in_category(category)
        cumulative_counter = Counter()

        for page in pages:
            text = get_page_text(page)
            words = clean_and_split_text(text)
            cumulative_counter.update(count_non_common_words(words))
    
    return cumulative_counter

@app.get("/word-frequencies/{category}")
async def get_word_frequencies(category: str):
    cache = load_cache()
    if category in cache and 'word_counts' in cache[category]:
        cumulative_counter = Counter(cache[category]['word_counts'])
    else:
        pages = get_pages_in_category(category)
        cumulative_counter = Counter()

        for page in pages:
            text = get_page_text(page)
            words = clean_and_split_text(text)
            cumulative_counter.update(count_non_common_words(words))
    
    if not cumulative_counter:
        raise HTTPException(status_code=404, detail="No data found for the given category")

    return JSONResponse(content=dict(cumulative_counter))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    
#     if len(sys.argv) != 2:
#         print("Usage: python wiki_category_analysis.py <Wikipedia_Category>")
#         sys.exit(1)

#     category = sys.argv[1]
#     cumulative_counter = process_category(category)

#     for word, count in cumulative_counter.most_common():
#         print(f"{word}: {count}")

# else:
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
