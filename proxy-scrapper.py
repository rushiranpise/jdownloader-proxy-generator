import requests
from bs4 import BeautifulSoup
import json

filename = 'proxylist.jdproxies'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
             '(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'


def create_proxy_record(address, port, type, enabled):
    proxy_record = dict()
    proxy_preferences = dict()
    proxy_preferences["username"] = None
    proxy_preferences["password"] = None
    proxy_preferences["port"] = port
    proxy_preferences["address"] = address
    proxy_preferences["type"] = type
    proxy_preferences['preferNativeImplementation'] = False
    proxy_preferences['resolveHostName'] = False
    proxy_preferences['connectMethodPreferred'] = False
    proxy_record['proxy'] = proxy_preferences
    proxy_record['rangeRequestsSupported'] = True
    proxy_record['filter'] = None
    proxy_record['pac'] = False
    proxy_record['reconnectSupported'] = True
    proxy_record['enabled'] = enabled
    json_data = proxy_record
    return json_data


def create_json_structure(proxies):
    proxylist_json_structure = dict()
    proxylist_json_structure["customProxyList"] = proxies
    return proxylist_json_structure

def get_proxies_from_proxyscan_io():
    proxy_site_url = 'https://www.proxyscan.io/api/proxy?ping=100&limit=1000'
    res = requests.get(proxy_site_url, headers={'User-Agent': user_agent})
    proxies = json.loads(res.text)
    proxy_list = list()
    for item in proxies:
        if len(item["Type"]) > 1:
            if "SOCKS5" in item["Type"]:
                item["Type"] = "SOCKS5"
            else:
                item["Type"] = "HTTPS" 
        else:
            item["Type"] = item["Type"][0].upper()
        proxy_list.append(
            create_proxy_record(
                type=item["Type"], address=item["Ip"], port=item["Port"], enabled=True
            )
        )
    return proxy_list

proxy_list = list([create_proxy_record(type="NONE", address=None, port=80, enabled=True)])
proxy_list = proxy_list + get_proxies_from_proxyscan_io()
json_output = create_json_structure(proxy_list)
with open(filename, 'w') as f:
    json.dump(json_output, f, indent=2)
