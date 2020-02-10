
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
        # journal_common_info[Row_Name.ISSN]="0022-1554"
        journal_common_info[Row_Name.EISSN]="1559-4122"
        journal_common_info[Row_Name.JID]="59598"


        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "Spring"
        info[Row_Name.YEAR] = "2018"
        info[Row_Name.ISSUE] = "null"
        # info[Row_Name.STRING_COVER_DATE] = "July 2015"
        info[Row_Name.TEMP_URL] = "null"
        infos.append(info)

        return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []
        url_set=set()
        url = "http://perspectives.ahima.org/series/2018-spring/"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")

        for h3 in soup.find_all("h3"):
            a = h3.find("a")
            if a != None:
                aurl=a["href"]

                article_info = dict(journal_temp)


                article_info[Row_Name.TEMP_AURL] = aurl
                # article_info[Row_Name.TITLE] = title

                urls.append(article_info)

        url = "http://perspectives.ahima.org/series/2018-spring/page/2/"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")

        for h3 in soup.find_all("h3"):
            a = h3.find("a")
            if a != None:
                aurl = a["href"]

                article_info = dict(journal_temp)

                article_info[Row_Name.TEMP_AURL] = aurl
                article_info[Row_Name.TITLE] = a.get_text()

                urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        # au = ""
        # for m_au in soup.find_all("meta", {"name": "dc.Creator"}):
        #
        #     au += m_au["content"] + "##"
        # if au != "":
        #     info[Row_Name.AUTHOR_NAME] = au[:-2]
        #
        # abs = soup.find("div", class_="hlFld-Abstract")
        # if abs != None:
        #     info[Row_Name.ABSTRACT] = abs.get_text().replace("Abstract.","").replace("Abstract","").replace("\n", "").strip()
        #
        # tag_a=soup.find("a",{"data-item-name":"download-PDF"})
        #
        # if tag_a!=None:
        #     pdf_url="https://journals.sagepub.com"+tag_a["href"]
        #     pdf_path=self.download_pdf(pdf_url,"sagepub")
        #     if pdf_path!=None:
        #         info[Row_Name.FULLTEXT_URL]=pdf_url
        #         info[Row_Name.FULLTEXT_PDF]=pdf_path


        return info

if __name__ == '__main__':
    urls=[]
    url_set=set()
    info={}

    url = "http://perspectives.ahima.org/series/2018-spring/"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    for h3 in soup.find_all("h3"):
        a=h3.find("a")
        if a!=None:
            print(a["href"])

    # for div in soup.find_all("div",class_="issueGroup"):
    #     va=div.find("a",class_="title expander open")
    #     volume=va.get_text().strip().split(" ")[1]
    #     if int(volume)>=36 and int(volume)<=42:
    #         for div_issue in div.find_all("div",class_="js_issue"):
    #             a=div_issue.find("a")
    #             args=a.get_text().replace("\n","").split("-")
    #             issue=args[0].strip().split(" ")[1]
    #             sd=args[1].strip()
    #             year=re.search("\d{4}",sd)
    #             if year!=None:
    #                 year=year.group()
    #
    #             iurl="https://www.mitpressjournals.org"+a["href"]
    #             print(iurl)






