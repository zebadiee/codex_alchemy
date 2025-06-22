import requests

def watts0n_search(query):
    # Example with DuckDuckGo Instant Answer API
    url = 'https://api.duckduckgo.com/'
    params = {'q': query, 'format': 'json'}
    resp = requests.get(url, params=params)
    data = resp.json()
    hits = []
    for topic in ['Heading', 'AbstractURL']:
        if topic in data and data[topic]:
            hits.append({'source': 'DuckDuckGo', 'title': data[topic], 'url': data.get('AbstractURL')})
    return hits[:5] 