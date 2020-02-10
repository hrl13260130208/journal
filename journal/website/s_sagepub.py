
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
from journal.common import Row_Name,common_website,common_journals,common_article



class journals(common_journals):
    #期刊：Journal of Histochemistry & Cytochemistry
    # def get(self,website,journal,url):
    #     infos=[]
    #     journal_common_info={}
    #     journal_common_info[Row_Name.JOURNAL_TITLE] = journal
    #     journal_common_info[Row_Name.PUBLISHER] = website
    #     journal_common_info[Row_Name.ISSN]="0022-1554"
    #     journal_common_info[Row_Name.EISSN]="1551-5044"
    #     journal_common_info[Row_Name.JID]="48527"
    #
    #
    #     info = dict(journal_common_info)
    #     info[Row_Name.VOLUME] = "63"
    #     info[Row_Name.YEAR] = "2015"
    #     info[Row_Name.ISSUE] = "7"
    #     info[Row_Name.STRING_COVER_DATE] = "July 2015"
    #     info[Row_Name.TEMP_URL] = "https://journals.sagepub.com/toc/jhca/63/7"
    #     infos.append(info)
    #
    #     info = dict(journal_common_info)
    #     info[Row_Name.VOLUME] = "62"
    #     info[Row_Name.YEAR] = "2014"
    #     info[Row_Name.ISSUE] = "8"
    #     info[Row_Name.STRING_COVER_DATE] = "August 2014"
    #     info[Row_Name.TEMP_URL] = "https://journals.sagepub.com/toc/jhca/62/8"
    #     infos.append(info)
    #
    #     info = dict(journal_common_info)
    #     info[Row_Name.VOLUME] = "62"
    #     info[Row_Name.YEAR] = "2014"
    #     info[Row_Name.ISSUE] = "9"
    #     info[Row_Name.STRING_COVER_DATE] = "September 2014"
    #     info[Row_Name.TEMP_URL] = "https://journals.sagepub.com/toc/jhca/62/9"
    #     infos.append(info)
    #
    #     return infos

    #期刊：
    def get(self,website,journal,url):
        infos=[]
        journal_common_info={}
        journal_common_info[Row_Name.JOURNAL_TITLE] = journal
        journal_common_info[Row_Name.PUBLISHER] = website
        journal_common_info[Row_Name.ISSN]="0300-0605"
        journal_common_info[Row_Name.EISSN]="1473-2300"
        journal_common_info[Row_Name.JID]="61844"


        # info = dict(journal_common_info)
        # info[Row_Name.VOLUME] = "43"
        # info[Row_Name.YEAR] = "2015"
        # info[Row_Name.ISSUE] = "6"
        # info[Row_Name.STRING_COVER_DATE] = "December 2015"
        # info[Row_Name.TEMP_URL] = "https://journals.sagepub.com/toc/imra/43/6"
        # infos.append(info)

        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "40"
        info[Row_Name.YEAR] = "2012"
        info[Row_Name.ISSUE] = "1"
        info[Row_Name.STRING_COVER_DATE] = "February 2012"
        info[Row_Name.TEMP_URL] = "https://journals.sagepub.com/toc/imra/40/1"
        infos.append(info)



        return infos

class article(common_article):

    # def first(self,journal_temp):
    #     urls = []
    #     url_set=set()
    #     data = requests.get(journal_temp[Row_Name.TEMP_URL])
    #     soup = BeautifulSoup(data.text, "html.parser")
    #
    #     for div in soup.find_all("div", class_="art_title linkable"):
    #         a = div.find("a")
    #         aurl="https://journals.sagepub.com" + a["href"]
    #
    #         article_info = dict(journal_temp)
    #
    #
    #         article_info[Row_Name.TEMP_AURL] = aurl
    #         # article_info[Row_Name.TITLE] = title
    #
    #         urls.append(article_info)
    #     return urls

    #没有文章页
    def first(self,journal_temp):
        urls = []
        url_set=set()
        data = requests.get(journal_temp[Row_Name.TEMP_URL])
        soup = BeautifulSoup(data.text, "html.parser")

        for a in soup.find_all("a", class_="abstract-link"):

            aurl="https://journals.sagepub.com" + a["href"]

            article_info = dict(journal_temp)


            article_info[Row_Name.TEMP_AURL] = aurl
            # article_info[Row_Name.TITLE] = title

            urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        au = ""
        for m_au in soup.find_all("meta", {"name": "dc.Creator"}):

            au += m_au["content"] + "##"
        if au != "":
            info[Row_Name.AUTHOR_NAME] = au[:-2]

        abs = soup.find("div", class_="hlFld-Abstract")
        if abs != None:
            info[Row_Name.ABSTRACT] = abs.get_text().replace("Abstract.","").replace("Abstract","").replace("\n", "").strip()

        tag_a=soup.find("a",{"data-item-name":"download-PDF"})

        if tag_a!=None:
            pdf_url="https://journals.sagepub.com"+tag_a["href"]
            pdf_path=self.download_pdf(pdf_url,"sagepub")
            if pdf_path!=None:
                info[Row_Name.FULLTEXT_URL]=pdf_url
                info[Row_Name.FULLTEXT_PDF]=pdf_path


        return info

if __name__ == '__main__':
    urls=[]
    url_set=set()
    info={}

    com = common_article(None)
    # url = "https://journals.sagepub.com/doi/abs/10.1177/147323001204000139"
    url = "https://journals.sagepub.com/doi/abs/10.1177/147323001204000110"
    # url = "https://journals.sagepub.com/doi/full/10.1177/0300060514566649"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    aff_dict={}
    for sage_aff in soup.find_all("div",class_="artice-info-affiliation"):
        sage_sup = sage_aff.find("sup")
        if sage_sup != None:
            key = sage_sup.get_text().strip()
            sage_sup.extract()
            aff_dict[key] = sage_aff.get_text().strip()
        else:
            aff_dict["0"] = sage_aff.get_text().strip()

        sage_aff.extract()
    au=""

    span=soup.find("span",class_="NLM_contrib-group")
    print(span.get_text())
    au_dict=com.clear_authors(span.get_text(),aff_dict.keys())
    print(au_dict,aff_dict)
    print(com.get_author_email_aff(au_dict,{},aff_dict))

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






