import requests
import urllib.parse
from typing import List, Dict, Any

base_url = 'https://www.googleapis.com/books/v1/volumes'
api_key = 'AIzaSyCrHfJF9K9osb60UM7yWzTwYDnBZ97t5U4'

def search_books(title=None, author=None, genre=None) -> List[Dict[str, Any]]:

    uri = f'{base_url}?key={api_key}'

    # No query was given, return empty
    if not any([title, author, genre]):
        return []

    # Whether or not we have yet added the 'q=' str
    search_param_added = False
    
    # Add the title to the query
    if title:
        if not search_param_added:
            uri = f'{uri}&q='
            search_param_added = True
        uri = f'{uri}intitle:{title}'

    # Add the author to the query
    if author:
        if not search_param_added:
            uri = f'{uri}&q='
            search_param_added = True
        else:
            uri = f'{uri}+'
        uri = f'{uri}inauthor:{author}'
    
    # Add the genre to the query
    if genre:
        if not search_param_added:
            uri = f'{uri}&q='
            search_param_added = True
        else:
            uri = f'{uri}+'
        uri = f'{uri}subject:{genre}'

    # Make the request
    r = requests.get(uri)

    # Bad request occurred
    if r.status_code not in [200, 201]:
        return []
    
    # Get the json data from the response
    json = r.json()

    # No results or bad response
    if 'items' not in json:
        return []

    # Create a dictionary of the book containing relevant data from the response
    books = []
    skipped_books = 0

    for book in json['items']:
        info = book['volumeInfo']
        if 'title' not in info or 'authors' not in info or 'categories' not in info:
            skipped_books = skipped_books+1
            continue

        books.append(
            {
                'title': book['volumeInfo']['title'],
                'author': book['volumeInfo']['authors'][0],

                'genre': book['volumeInfo']['categories'][0] if 'categories' in book['volumeInfo'] else None,

                'cover_img': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else None,
            }
        )
    print(f'skipped {skipped_books} books')
    # Return the books    
    return books

