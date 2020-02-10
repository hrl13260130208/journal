
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
from journal.common import Row_Name,common_website,common_journals,common_article



class journals(common_journals):

    def get(self,website,journal,url):
        infos=[]
        journal_common_info={}
        journal_common_info[Row_Name.JOURNAL_TITLE] = journal
        journal_common_info[Row_Name.PUBLISHER] = website
        journal_common_info[Row_Name.ISSN]="1476-5586"
        journal_common_info[Row_Name.EISSN]="1522-8002"
        journal_common_info[Row_Name.JID]="61523"


        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "16"
        info[Row_Name.YEAR] = "2014"
        info[Row_Name.ISSUE] = "11"
        info[Row_Name.STRING_COVER_DATE] = "Apr 2014"
        info[Row_Name.TEMP_URL] = "https://www.sciencedirect.com/journal/neoplasia/vol/16/issue/11"
        infos.append(info)

        return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []
        url_set=set()
        url = "https://www.sciencedirect.com/journal/neoplasia/vol/16/issue/11"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

        data = requests.get(url, headers=header)
        soup = BeautifulSoup(data.text, "html.parser")
        # print(soup)
        ol = soup.find("ol", class_="js-jl-aip-list article-list-items")

        for li in ol.find_all("li"):
            h3 = li.find("h3")
            if h3 != None:
                a = h3.find("a")
                aurl="https://www.sciencedirect.com"+a["href"]
                title= a.get_text()

                article_info = dict(journal_temp)

                article_info[Row_Name.TEMP_AURL] = aurl
                article_info[Row_Name.TITLE] = title

                urls.append(article_info)

        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"
        abs = soup.find("div", {"id": "abstracts"})
        if abs != None:
            h2 = abs.find("h2")
            if h2 != None:
                h2.extract()
            info[Row_Name.ABSTRACT] = abs.get_text().replace("\n", "").strip()

        au = ""
        for a in soup.find_all("a", class_="author size-m workspace-trigger"):
            # print(a)
            f = a.find("span", class_="text given-name")
            s = a.find("span", class_="text surname")
            # print(f,s)
            au += f.get_text() + " " + s.get_text() + "##"
        # print(au)
        info[Row_Name.AUTHOR_NAME]=au[:-2]

        if Row_Name.FULLTEXT_URL in info.keys():
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

            data = requests.get(info[Row_Name.FULLTEXT_URL],headers=header)
            soup = BeautifulSoup(data.text, "html.parser")

            div = soup.find("div", {"id": "redirect-message"})
            # print(div)
            if div != None:
                a = div.find("a")
                pdf_path = self.download_pdf(a["href"], dir_name="sciencedirect")
                if pdf_path != None:
                    info[Row_Name.FULLTEXT_PDF] = pdf_path


        return info

if __name__ == '__main__':
    urls=[]
    url_set=set()
    info={}

    url = "https://www.sciencedirect.com/science/article/pii/S147655861400116X/pdfft?md5=2959c3a08d95ff6b9a95dd450801d3f9&pid=1-s2.0-S147655861400116X-main.pdf"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

    data = requests.get(url,headers=header)
    soup = BeautifulSoup(data.text, "html.parser")
    # print(soup)

    au=""
    for a in soup.find_all("a", class_="author size-m workspace-trigger"):
        f=a.find("span", class_="text given-name")
        s=a.find("span", class_="ext surname")
        au+=f.get_text()+" "+s.get_text()+"##"

    print(au[:-2])


    # ol = soup.find("ol", class_="js-jl-aip-list article-list-items")
    #
    # for li in ol.find_all("li"):
    #     h3=li.find("h3")
    #     if h3!=None:
    #         a=h3.find("a")
    #         print("https://www.sciencedirect.com"+a["href"],a.get_text())








