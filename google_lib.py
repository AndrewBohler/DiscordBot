# pip install git+https://github.com/abenassi/Google-Search-API
from google import google


def search_results(search_string: str, num_pages: int=1):
    return google.search(search_string, num_pages)


def print_search_results(search_string: str, num_pages: int=1):
    for search_result in search_results(search_string, num_pages):
        print(search_result.description)
