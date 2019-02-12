import sys

# pip install git+https://github.com/abenassi/Google-Search-API
try:
    from google import google
except ImportError:
    sys.exit(
        'Error: Google-Search-API missing\n'
        'Do: pip install git+https://github.com/abenassi/Google-Search-API')


def search_results(search_string: str, num_pages: int=1):
    return google.search(search_string, num_pages)


def print_search_results(search_string: str, num_pages: int=1):
    for search_result in search_results(search_string, num_pages):
        print(search_result.description)
