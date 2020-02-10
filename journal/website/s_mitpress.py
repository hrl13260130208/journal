
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
        journal_common_info[Row_Name.ISSN]="0891-2017"
        journal_common_info[Row_Name.EISSN]="1530-9312"
        journal_common_info[Row_Name.JID]="45524"

        url = "https://www.mitpressjournals.org/compling"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")

        for div in soup.find_all("div", class_="issueGroup"):
            va = div.find("a", class_="title expander open")
            volume = va.get_text().strip().split(" ")[1]
            if int(volume) >= 36 and int(volume) <= 42:
                for div_issue in div.find_all("div", class_="js_issue"):
                    a = div_issue.find("a")
                    args = a.get_text().replace("\n", "").split("-")
                    issue = args[0].strip().split(" ")[1]
                    sd = args[1].strip()
                    year = re.search("\d{4}", sd)
                    if year != None:
                        year = year.group()

                    iurl = "https://www.mitpressjournals.org" + a["href"]
                    info = dict(journal_common_info)
                    info[Row_Name.VOLUME] = volume
                    info[Row_Name.YEAR] = year
                    info[Row_Name.ISSUE] = issue
                    info[Row_Name.STRING_COVER_DATE] = sd
                    info[Row_Name.TEMP_URL] = iurl
                    infos.append(info)

        return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []
        url_set=set()
        data = requests.get(journal_temp[Row_Name.TEMP_URL])
        soup = BeautifulSoup(data.text, "html.parser")

        div = soup.find("div", class_="tocContent")
        for table in div.find_all("table"):
            t_div = table.find("div", class_="art_title linkable")
            a = t_div.find("a")
            title=a.get_text()
            aurl="https://www.mitpressjournals.org" + a["href"]

            article_info = dict(journal_temp)


            article_info[Row_Name.TEMP_AURL] = aurl
            article_info[Row_Name.TITLE] = title

            urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        abs = soup.find("div", class_="abstractSection abstractInFull")
        if abs != None:
            info[Row_Name.ABSTRACT] = abs.get_text().replace("\n", "").strip()

        pageline=soup.find("span", class_="pageRange")

        if pageline!=None:
            pageline = pageline.get_text()
            pages = re.search("\d+-\d+", pageline)
            if pages != None:
                pages = pages.group().split("-")
                info[Row_Name.START_PAGE] = pages[0]
                info[Row_Name.END_PAGE] = pages[1]

        au=""
        for m_au in soup.find_all("meta",{"name":"dc.Creator"}):
            print(m_au)
            au+=m_au["content"]+"##"
        if au!="":
            info[Row_Name.AUTHOR_NAME]=au[:-2]

        pdf_a=soup.find("a",class_="show-pdf")
        if pdf_a!=None:
            pdf_url=pdf_a["href"]
            pdf_path=self.download_pdf(pdf_url,"mitpress")
            if pdf_path!=None:
                info[Row_Name.FULLTEXT_URL]=pdf_url
                info[Row_Name.FULLTEXT_PDF]=pdf_path

        return info

if __name__ == '__main__':
    urls=[]
    url_set=set()
    info={}

    com=common_article(None)
    url = "https://www.mitpressjournals.org/doi/abs/10.1162/coli.2010.36.2.09054"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")


    au_div=soup.find_all("div", class_="authorName")
    aff_div=soup.find_all("div", class_="authorAffiliation")
    aus=""
    affs=""
    aset=set()
    for au in au_div:
        au=au.get_text()
        if not au in aset:
            aus += au + "##"
            aset.add(au)

    print(aus)
    # print(au_div)
    # print(aff_div)
    # if len(au_div) ==len(aff_div):
    #     for a_index in range(len(au_div)):
    #         print(au_div[a_index].get_text())
    #         au=com.find_last(au_div[a_index].get_text())
    #         if not au in aset:
    #             aff=aff_div[a_index].get_text()
    #             aus+=au+"##"
    #             affs+=aff+"##"
    #             aset.add(au)
    # print(aus,affs)


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






