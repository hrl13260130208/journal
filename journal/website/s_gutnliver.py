
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
        journal_common_info[Row_Name.ISSN]="1976-2283"
        journal_common_info[Row_Name.EISSN]="2005-1212"
        journal_common_info[Row_Name.JID]="62586"



        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "12"
        info[Row_Name.YEAR] = "2018"
        info[Row_Name.ISSUE] = "1"
        info[Row_Name.STRING_COVER_DATE] = "Jan 2018"
        info[Row_Name.TEMP_URL] = "http://www.gutnliver.org/journal/list.html?pn=vol&TG=vol&sm=&s_v=12&s_n=1&year=2018"
        infos.append(info)

        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "7"
        info[Row_Name.YEAR] = "2013"
        info[Row_Name.ISSUE] = "1"
        info[Row_Name.STRING_COVER_DATE] = "Jan 2013"
        info[Row_Name.TEMP_URL] = "http://www.gutnliver.org/journal/list.html?pn=vol&TG=vol&sm=&s_v=7&s_n=1&year=2013"
        infos.append(info)

        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "7"
        info[Row_Name.YEAR] = "2013"
        info[Row_Name.ISSUE] = "2"
        info[Row_Name.STRING_COVER_DATE] = "Mar 2013"
        info[Row_Name.TEMP_URL] = "http://www.gutnliver.org/journal/list.html?pn=vol&TG=vol&s_v=7&s_n=2&year=2013"
        infos.append(info)

        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "7"
        info[Row_Name.YEAR] = "2013"
        info[Row_Name.ISSUE] = "3"
        info[Row_Name.STRING_COVER_DATE] = "May 2013"
        info[Row_Name.TEMP_URL] = "http://www.gutnliver.org/journal/list.html?pn=vol&TG=vol&s_v=7&s_n=3&year=2013"
        infos.append(info)

        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "7"
        info[Row_Name.YEAR] = "2013"
        info[Row_Name.ISSUE] = "4"
        info[Row_Name.STRING_COVER_DATE] = "Jul 2013"
        info[Row_Name.TEMP_URL] = "http://www.gutnliver.org/journal/list.html?pn=vol&TG=vol&s_v=7&s_n=4&year=2013"
        infos.append(info)

        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "7"
        info[Row_Name.YEAR] = "2013"
        info[Row_Name.ISSUE] = "5"
        info[Row_Name.STRING_COVER_DATE] = "Sep 2013"
        info[Row_Name.TEMP_URL] = "http://www.gutnliver.org/journal/list.html?pn=vol&TG=vol&s_v=7&s_n=5&year=2013"
        infos.append(info)

        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "7"
        info[Row_Name.YEAR] = "2013"
        info[Row_Name.ISSUE] = "6"
        info[Row_Name.STRING_COVER_DATE] = "Nov 2013"
        info[Row_Name.TEMP_URL] = "http://www.gutnliver.org/journal/list.html?pn=vol&TG=vol&s_v=7&s_n=6&year=2013"
        infos.append(info)

        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "4"
        info[Row_Name.YEAR] = "2010"
        info[Row_Name.ISSUE] = "Suppl"
        info[Row_Name.STRING_COVER_DATE] = "Sep 2010"
        info[Row_Name.TEMP_URL] = "http://www.gutnliver.org/journal/list.html?pn=vol&TG=vol&sm=sp&s_v=4&s_n=4&year=2010"
        infos.append(info)

        return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []
        url_set=set()
        data = requests.get(journal_temp[Row_Name.TEMP_URL])
        soup = BeautifulSoup(data.text, "html.parser")

        for div in soup.find_all("div", class_="basic_list"):
            a = div.find("a", class_='j_text_size')
            aurl="http://www.gutnliver.org" + a["href"]

            article_info = dict(journal_temp)
            article_info[Row_Name.TEMP_AURL] = aurl

            urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        abs = soup.find("div", class_="Abstract")
        if abs != None:
            info[Row_Name.ABSTRACT] = abs.get_text().replace("\n", "").replace("Abstract", "").strip()

        if Row_Name.FULLTEXT_URL in info.keys():
            pdf_path = self.download_pdf(info[Row_Name.FULLTEXT_URL], dir_name="gutnliver")
            if pdf_path != None:
                info[Row_Name.FULLTEXT_PDF] = pdf_path

        au=soup.find("meta",{ "name":"citation_authors"})
        if au!=None:
            info[Row_Name.AUTHOR_NAME]=au["content"].replace(",","##")

        return info

if __name__ == '__main__':
    urls=[]
    url_set=set()
    info={}

    com = common_article(None)
    # url = "http://www.gutnliver.org/journal/view.html?uid=496#"
    # url = "http://www.gutnliver.org/journal/view.html?uid=499#"
    # data = requests.get(url)
    # soup = BeautifulSoup(data.text, "html.parser")
    #
    # aff_dict={}
    # div =soup.find("div", {"id":"conBox"})
    # for p in div.find_all("p"):
    #     sup=p.find("sup")
    #     if sup != None:
    #         key = sup.get_text().strip()
    #         sup.extract()
    #         aff_dict[key] = p.get_text().strip()
    #     else:
    #         aff_dict["0"] = p.get_text().strip()
    #
    #     p.extract()
    # print(aff_dict)
    # line=div.get_text()
    # line=line[:line.find("Correspondence")].strip()
    # print(line)
    # au_dict=com.clear_authors(line,aff_dict.keys())
    # print(au_dict)
    # au,em,af=com.get_author_email_aff(au_dict,{},aff_dict)
    #
    # print(au,em,af)

    # print(com.get_sup("name111",["1","11"],0))








