from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

# Geting links to number pages
def getPagesLink(url):
    link_list = [url]
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        soup = BeautifulSoup(html, features="lxml")
        soup_list = soup.findAll("a", {"href": re.compile(url.split("/")[-1].split(".")[0][:-1]+"\d+.html")})
        link_list.extend(['/'.join(url.split("/")[:-1]) + "/" + i.attrs['href'] for i in soup_list])
    except AttributeError as e:
        return None
    return link_list

def main():
    print(getPagesLink("https://www.cvk.gov.ua/pls/vnd2019/wp401pt001f01=919lit=192current_row=1.html"))


if __name__ == "__main__":
    main()
