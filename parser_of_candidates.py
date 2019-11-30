from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import functools

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

def getNamePartyNumber(url_list):
    result_list = []
    for url in url_list:
        try:
            html = urlopen(url)
        except HTTPError as e:
            return None
        try:
            soup = BeautifulSoup(html, features="lxml")
            name_list = [tuple(name.get_text().split()) for name in soup.findAll("a", {"href": re.compile("^wp407.*")})]
            party_and_number = [tuple(i.get_text().split(", ")) for i in soup.findAll("b")]
            result_list.extend(functools.reduce(lambda a,b: a+b, i) for i in zip(name_list, party_and_number))
        except AttributeError as e:
            return None
    return result_list

def main():
    url_list = getAllLinks("https://www.cvk.gov.ua/pls/vnd2019/wp401pt001f01=919lit=192current_row=1.html")
    print(getNamePartyNumber(url_list))


if __name__ == "__main__":
    main()
