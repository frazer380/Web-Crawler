import urllib3
from bs4 import BeautifulSoup
import json
import sys
import re

http = urllib3.PoolManager()


def crawl(url):

    soup = getUrlData(url)

    # FIND DATA

    values = getPageData(soup)
    updateJSON(values[0], values[1], values[2], url)

    # FIND ANCHOR TAGS
    surfLink(soup, url)
    #with open("sites.json", "a") as file:
    #    json.dump([{"Title": title, "Description": description, "Keywords": keywords, "URL": url}], file)

def surfLink(data, url):
    for link in data.find_all("a"):
        link = link.get("href")
        if link.startswith("/"):
            link = url + link
            soup = getUrlData(link)
            values = getPageData(soup)
            updateJSON(values[0], values[1], values[2], link)
            #surfLink(soup, link)
        elif link.startswith("./"):
            link = link.replace(".", url)
            soup = getUrlData(soup)
            values = getPageData(soup)
            updateJSON(values[0], values[1], values[2], link)
            #surfLink(soup, link)
        else:
            soup = getUrlData(link)
            values = getPageData(soup)
            updateJSON(values[0], values[1], values[2], link)
            #surfLink(soup, link)

def getUrlData(link):
    response = http.request("GET", link)
    html = response.data
    soup = BeautifulSoup(html, "html.parser")
    return soup
    
def getPageData(data):
    desc = ""
    words = ""
    for meta in data.find_all("meta", {"name": "description"}):
        if meta:
            desc = meta["content"]
    for meta in data.find_all("meta", {"name": "keywords"}):
        if meta:
            words = meta["content"]
    title = data.title.string
    return [desc, words, title]
    
def updateJSON(title, description, keywords, url):
    if title == "":
        title = description
        if description == "":
            title = keywords
    jsonData = {"Title": title, "Description": description, "Keywords": keywords, "URL": url}
    with open("sites.json", "r") as file:
        data = json.load(file)
        file.close()
    strData = str(data)
    if not strData.find(str(jsonData)) >= 0:
        data.append(jsonData)

        with open("sites.json", "w") as file:
            json.dump(data, file, indent=4, separators=(',', ': '))
            file.close()

crawl(sys.argv[1])