from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import functools
import xlwt

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

# Getting list of full name, party and number
def getNamePartyNumber(url_list):
    result_list = []
    for url in url_list:
        try:
            html = urlopen(url)
        except HTTPError as e:
            return None
        try:
            soup = BeautifulSoup(html, features="lxml")
            # Getting names
            name_list = [tuple(name.get_text().split(maxsplit=2)) for name in soup.findAll("a", {"href": re.compile("^wp407.*")})]
            for index, val in enumerate(name_list):
                if len(val) < 3:
                    name_list[index] = val + ('',)
            # Getting party and number
            temp = soup.findAll("td")
            temp = [t.find("b") for t in temp]
            party_and_number = [tuple(i.get_text().split(", ")) for i in temp if i != None]
            # Aggregate
            result_list.extend(functools.reduce(lambda a,b: a+b, i) for i in zip(name_list, party_and_number))
        except AttributeError as e:
            return None
    return result_list

# Writing in excel-file
def writeExcel(info_list):
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("Candidates")
    # Column titles
    title_list = ["Прізвище", "Ім'я", "По-батькові", "Партія", "Номер у списку"]
    for c in range(len(title_list)):
        sheet.write(0, c, title_list[c])
    # Fill in information
    for r in range(1, len(info_list)+1):
        for c in range(len(info_list[0])):
            sheet.write(r, c, info_list[r-1][c])
    wb.save("Candidates.xls")

def main():
    url_list = getAllLinks("https://www.cvk.gov.ua/pls/vnd2019/wp401pt001f01=919lit=192current_row=1.html")
    writeExcel(getNamePartyNumber(url_list))

if __name__ == "__main__":
    main()
