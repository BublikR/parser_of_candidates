from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

# Getting links to number pages
def getPagesLinks(url):
    link_list = [url]
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        soup = BeautifulSoup(html, features="lxml")
        soup_list = soup.findAll("a", {"href": re.compile(url.split("/")[-1].split(".")[0][:-1]+"\d+.html")})
        link_list.extend(["/".join(url.split("/")[:-1]) + "/" + i.attrs["href"] for i in soup_list])
    except AttributeError as e:
        return None
    return link_list

# Getting all links
def getAllLinks(url):
    link_list = [url]
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        soup = BeautifulSoup(html, features="lxml")
        soup_list = soup.findAll("a", {"href": re.compile(url.split("/")[-1].split("=")[0]+".*row=1.html")})
        link_list.extend(["/".join(url.split("/")[:-1]) + "/" + i.attrs["href"] for i in soup_list])
        all_link_list = []
        [all_link_list.extend(getPagesLinks(url)) for url in link_list]
    except AttributeError as e:
        return None
    return all_link_list

def main():
    print(getAllLinks("https://www.cvk.gov.ua/pls/vnd2019/wp401pt001f01=919lit=192current_row=1.html"))


if __name__ == "__main__":
    main()
