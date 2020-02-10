
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
        journal_common_info[Row_Name.EISSN]="1452-8266"
        journal_common_info[Row_Name.JID]="60352"


        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "33"
        info[Row_Name.YEAR] = "2014"
        info[Row_Name.ISSUE] = "2"
        info[Row_Name.STRING_COVER_DATE] = "Apr 2014"
        info[Row_Name.TEMP_URL] = "https://content.sciendo.com/configurable/contentpage/journals$002fjomb$002f33$002f2$002fjomb.33.issue-2.xml"
        infos.append(info)

        return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []
        url_set=set()
        url = "https://content.sciendo.com/configurable/contentpage/journals$002fjomb$002f33$002f2$002fjomb.33.issue-2.xml"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

        data = requests.get(url, headers=header,verify=False)

        soup = BeautifulSoup(data.text, "html.parser")
        # print(soup)
        ul = soup.find("ul", class_="tree collapsible-tree expand-all m-4 toc-large-display")

        for li in ul.find_all("li"):
            a = li.find("a", class_="c-Typography c-Typography--title c-Button--link c-Button--primary")
            aurl="https://content.sciendo.com" + a["href"]
            title=a.get_text().replace("\n","").strip()

            article_info = dict(journal_temp)


            article_info[Row_Name.TEMP_AURL] = aurl
            article_info[Row_Name.TITLE] = title

            urls.append(article_info)

        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"
        section=soup.find("section",class_="abstract")
        if section!=None:
            h2=section.find("h2")
            if h2!=None:
                h2.extract()
            info[Row_Name.ABSTRACT]=section.get_text().replace("\n","").strip()

        aff_dict = {}
        ul=soup.find("ul",class_="affiliation-list list-style-none")
        for li in ul.find_all("li"):
            sup = li.find("sup")
            if sup == None:
                sup_key = 0
            else:
                sup_key = sup.get_text().strip()
                sup.extract()

            aff_dict[sup_key] = li.get_text().strip()

        au_div=soup.find("div",class_="contributor-line text-subheading")
        em=au_div.find("a",class_="email c-Button--link c-Button--primary ico-email")
        if em!=None:
            # print("==================",em.get_text())
            em.extract()

        # print(au_div.get_text())
        au_dict = self.clear_authors(au_div.get_text().replace("\n","").strip(), aff_dict.keys())
        au, em, aff = self.get_author_email_aff(au_dict, {}, aff_dict)
        info[Row_Name.AUTHOR_NAME] = au
        info[Row_Name.AFFILIATION] = aff

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
        if Row_Name.FULLTEXT_URL in info.keys():
            pdf_path = self.download_pdf(info[Row_Name.FULLTEXT_URL], dir_name="sciendo")
            if pdf_path != None:
                info[Row_Name.FULLTEXT_PDF] = pdf_path


        return info

if __name__ == '__main__':
    urls=[]
    url_set=set()
    info={}

    url = "https://content.sciendo.com/configurable/contentpage/journals$002fjomb$002f33$002f2$002fjomb.33.issue-2.xml"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

    data = requests.get(url,headers=header)

    soup = BeautifulSoup(data.text, "html.parser")
    # print(soup)
    ul = soup.find("ul",class_="tree collapsible-tree expand-all m-4 toc-large-display")

    for li in ul.find_all("li"):
        a=li.find("a",class_="c-Typography c-Typography--title c-Button--link c-Button--primary")
        print("https://content.sciendo.com"+a["href"],a.get_text())

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






