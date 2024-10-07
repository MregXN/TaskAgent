import os 
import requests
from getpass import getpass
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import env

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
BING_SEARCH_V7_SUBSCRIPTION_KEY = env.BING_SEARCH_V7_SUBSCRIPTION_KEY
if not BING_SEARCH_V7_SUBSCRIPTION_KEY:
    BING_SEARCH_V7_SUBSCRIPTION_KEY = getpass("Bing Search V7 Subscription Key: ")
    os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY'] = BING_SEARCH_V7_SUBSCRIPTION_KEY

endpoint = env.BING_ENDPOINT

def bing_web_search(search_query):
    '''
    This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
    Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
    '''
    # Construct a request
    mkt = 'en-US'
    params = { 'q': search_query, 'mkt': mkt, "textDecorations": True}
    headers = { 'Ocp-Apim-Subscription-Key': BING_SEARCH_V7_SUBSCRIPTION_KEY }

    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        json_content = response.json()
        contexts = json_content["webPages"]["value"][:1]
        # result = [con["name"] + "\n" + con['url'] for con in contexts]
        all_webtext = []
        for item in contexts:
            print("- [Bing web search] visiting {} via {}".format(item["name"], item["url"]))
            url = item['url']
            try:
                page = urlopen(url)
                html = page.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                webtext = soup.get_text()
            except Exception as ex:
                print(ex)
                continue
            webtext = re.sub(r'\s+', ' ', webtext).strip()
            all_webtext.append(webtext)
        return "\n\n".join(all_webtext)
    except Exception as ex:
        raise ex
    
