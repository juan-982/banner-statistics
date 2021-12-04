import requests

def get(url):
    print("GET: " + url)
    response = requests.get(url)
    return response
