
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
        journal_common_info[Row_Name.ISSN]="0003-9438"
        journal_common_info[Row_Name.EISSN]="2363-9822"
        journal_common_info[Row_Name.JID]="37796"

        url = "https://www.arch-anim-breed.net/about/contact.html"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")

        for div in soup.find_all("div", class_="grid-100 volumes"):
            sp = div.find("span", class_="triangle")
            text = sp.get_text().replace("\n", "").strip()
            if "|" in text:
                text = text[:text.find("|")]
            vols = text.split(",")
            volume=vols[0][-2:]
            year=vols[1].strip()
            for li in div.find_all("li"):
                a = li.find("a")
                iurl=a["href"]
                issue=a.get_text().replace("Issue","").strip()
                if int(year)>=2010 and int(year)<=2012:
                    info = dict(journal_common_info)
                    info[Row_Name.VOLUME] = volume
                    info[Row_Name.YEAR] = year
                    info[Row_Name.ISSUE] = issue
                    info[Row_Name.TEMP_URL] = iurl
                    infos.append(info)
                if  int(year)==2017 and issue=="4":
                    info = dict(journal_common_info)
                    info[Row_Name.VOLUME] = volume
                    info[Row_Name.YEAR] = year
                    info[Row_Name.ISSUE] = issue
                    info[Row_Name.TEMP_URL] = iurl
                    infos.append(info)

        return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []
        url_set=set()
        data = requests.get(journal_temp[Row_Name.TEMP_URL])
        soup = BeautifulSoup(data.text, "html.parser")

        for div in soup.find_all("div", class_="grid-85 tablet-grid-85"):
            a = div.find("a")

            title=a.get_text()
            aurl= a["href"]

            article_info = dict(journal_temp)

            article_info[Row_Name.TEMP_AURL] = aurl
            article_info[Row_Name.TITLE] = title

            urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        if Row_Name.ABSTRACT in info.keys():
            info[Row_Name.ABSTRACT]=BeautifulSoup(info[Row_Name.ABSTRACT],"html.parser").get_text().replace("Abstract.","").replace("Abstract","")


        if Row_Name.FULLTEXT_URL in info.keys():
            pdf_path=self.download_pdf(info[Row_Name.FULLTEXT_URL],dir_name="archanimbreed")
            if pdf_path!=None:
                info[Row_Name.FULLTEXT_PDF]=pdf_path

        aff_dict={}
        ul=soup.find("ul",class_="affiliation-list hide-on-mobile")

        for li in ul.find_all("li"):
            sup=li.find("sup")
            if sup!=None:
                key=sup.get_text().strip()
                sup.extract()
                aff_dict[key]=li.get_text().strip()
            else:
                aff_dict["0"] = li.get_text().strip()

        # print(aff_dict)
        # au_dict=None
        for strong in soup.find_all("strong",class_="hide-on-mobile"):
            print(len(strong["class"]),strong)
            if len(strong["class"])>1:
                continue

            au_dict = self.clear_authors(strong.get_text(), aff_dict.keys())
            # print(au_dict)
            au, em, aff = self.get_author_email_aff(au_dict, {}, aff_dict)
            info[Row_Name.AUTHOR_NAME] = au
            info[Row_Name.AFFILIATION] = aff

        return info

if __name__ == '__main__':
    urls=[]
    url_set=set()
    info={}

    url = "https://www.arch-anim-breed.net/55/562/2012/"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    com = common_article(None)
    print(com.get_author_and_aff_from_head(soup))

    # for div in soup.find_all("div",class_="grid-85 tablet-grid-85"):
    #     a=div.find("a")
    #     print(a["href"],a.get_text())

    # for div in  soup.find_all("div",class_="grid-100 volumes"):
    #     sp=div.find("span", class_="triangle")
    #     text=sp.get_text().replace("\n","").strip()
    #     if "|" in text:
    #         text=text[:text.find("|")]
    #     vols=text.split(",")
    #     print(vols[0][-2:])
    #     print(vols[1].strip())
    #     for li in div.find_all("li"):
    #         a = li.find("a")
    #         print(a["href"],a.get_text())







