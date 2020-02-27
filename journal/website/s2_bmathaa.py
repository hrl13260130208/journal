

import requests
from bs4 import BeautifulSoup
import PyPDF2
import re
from journal.common import Row_Name,common_website,common_journals,common_article

class journals(common_journals):

    def get(self,website,journal,url):
        infos=[]
        journal_common_info={}
        journal_common_info[Row_Name.JOURNAL_TITLE] = journal
        journal_common_info[Row_Name.PUBLISHER] = website
        # journal_common_info[Row_Name.ISSN]="0219-8126"
        journal_common_info[Row_Name.EISSN]="1821-1291"
        journal_common_info[Row_Name.JID]="52429"

        url = "http://bmathaa.org/online.html"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")

        for a in soup.find_all("a"):
            text = a.get_text()
            r = re.search("V\.\d* Issue \d*", text)
            if r != None:
                items = r.group().split(" ")
                vol = items[0].replace("V.", "")
                issue = items[2]
                print(vol, issue)
                print("http://bmathaa.org/" + a["href"])
                if int(vol)>=2 and int(vol)<=8:
                    info = dict(journal_common_info)
                    info[Row_Name.VOLUME]=vol
                    info[Row_Name.ISSUE]=issue
                    info[Row_Name.TEMP_URL]="http://bmathaa.org/" + a["href"]
                    infos.append(info)
        return infos


class article(common_article):

    def first(self,journal_temp):
        urls = []

        data = requests.get(journal_temp[Row_Name.TEMP_URL],verify=False)
        soup = BeautifulSoup(data.text, "html.parser")
        # print(soup)

        div = soup.find("div", id="primarycontent")
        h4 = div.find_all("h4")
        p = div.find_all("p")
        soup.extract()
        if len(h4) == len(p):
            for title, i in zip(h4, p):
                article_info = dict(journal_temp)
                a = i.find("a")
                # print("http://bmathaa.org/" + a["href"])
                title = title.get_text()
                t = re.match("\d*\.", title)
                if t != None:
                    title = title.replace(t.group(), "").strip()
                # print(title)
                a.extract()
                au=i.get_text().replace("Author:", "").replace("Authors: ", "").replace(" and ", "##").replace(",","##")
                article_info[Row_Name.TITLE]=title
                article_info[Row_Name.AUTHOR_NAME]=au
                article_info[Row_Name.FULLTEXT_URL]="http://bmathaa.org/" + a["href"]
                urls.append(article_info)


        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        if Row_Name.FULLTEXT_URL in info.keys():

            pdf_path = self.download_pdf(info[Row_Name.FULLTEXT_URL],
                                         dir_name="bci")
            if pdf_path != None:
                info[Row_Name.FULLTEXT_PDF] = pdf_path


        return info


if __name__ == '__main__':
    # url = "http://bmathaa.org/online.html"
    # data = requests.get(url)
    # soup = BeautifulSoup(data.text, "html.parser")
    #
    # for a in soup.find_all("a"):
    #     text=a.get_text()
    #     r=re.search("V\.\d* Issue \d*",text)
    #     if r!=None:
    #         items=r.group().split(" ")
    #         vol=items[0].replace("V.","")
    #         issue=items[2]
    #         if int(vol) >= 2 and int(vol) <= 8:
    #             print(vol,issue)
    #             print("http://bmathaa.org/"+a["href"])

    url="http://bmathaa.org/vol_5_issue_2.html"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    div=soup.find("div",id="primarycontent")
    h4=div.find_all("h4")
    p=div.find_all("p")
    soup.extract()
    if len(h4)==len(p):
        for title,i in zip(h4,p):
            a=i.find("a")
            print("http://bmathaa.org/"+a["href"])
            title=title.get_text()
            t=re.match("\d*\.",title)
            if t!=None:
                title=title.replace(t.group(),"").strip()
            print(title)
            a.extract()
            print(i.get_text().replace("Author:","").replace("Authors: ","").replace(" and ","##").replace(",","##"))



