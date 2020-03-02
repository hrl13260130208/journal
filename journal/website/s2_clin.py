

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

        url = "https://www.clinicalneuropsychiatry.org/past-issues/"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")

        for h4 in soup.find_all("h4"):
            a = h4.find("a")
            items = a.get_text().split(",")
            vol = items[0].replace("Clinical Neuropsychiatry Volume", "")
            i = items[1].split("–")
            if len(i) != 2:
                i = items[1].split("-")
            issue = i[0].replace("issue", "")
            year=re.search("\d{4}",i[1]).group()
            # print(vol, issue, i[1], a["href"])

            if int(year)<=2018:
                info = dict(journal_common_info)
                info[Row_Name.VOLUME]=vol
                info[Row_Name.YEAR]=year
                info[Row_Name.ISSUE]=issue
                info[Row_Name.STRING_COVER_DATE]=i[1]
                info[Row_Name.TEMP_URL]=a["href"]
                infos.append(info)
        return infos


class article(common_article):

    def first(self,journal_temp):
        urls = []

        data = requests.get(journal_temp[Row_Name.TEMP_URL],verify=False)
        soup = BeautifulSoup(data.text, "html.parser")
        # print(soup)

        for div in soup.find_all("div", class_="media"):
            div_p = div.find("div", class_="pull-right")
            a = div_p.find("a")
            pdf_url = a["onclick"].replace("location.href='", "").replace("';return false;", "")
            div_b = div.find("div", class_="media-body")
            h3 = div_b.find("h3")
            ha = h3.find("a")
            span = div_b.find("span", class_="autori")

            # print(ha.get_text(), ha["href"], span.get_text().replace("...", "").replace(",", "##"), pdf_url)

            article_info = dict(journal_temp)

            article_info[Row_Name.TITLE]=a.get_text()
            if span!=None:
                article_info[Row_Name.AUTHOR_NAME]=span.get_text().replace("...", "").replace(",", "##")
            article_info[Row_Name.TEMP_AURL]=ha["href"]
            article_info[Row_Name.FULLTEXT_URL]=pdf_url
            urls.append(article_info)


        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        # if Row_Name.FULLTEXT_URL in info.keys():
        #
        #     pdf_path = self.download_pdf(info[Row_Name.FULLTEXT_URL],
        #                                  dir_name="bci")
        #     if pdf_path != None:
        #         info[Row_Name.FULLTEXT_PDF] = pdf_path


        return info


if __name__ == '__main__':


    url="https://www.clinicalneuropsychiatry.org/clinical-neuropsychiatry-volume-15-issue-1-february-2018/"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    for div in soup.find_all("div", class_="media"):
        div_p=div.find("div",class_="pull-right")
        a=div_p.find("a")
        pdf_url=a["onclick"].replace("location.href='","").replace("';return false;","")
        div_b=div.find("div", class_="media-body")
        h3=div_b.find("h3")
        ha=h3.find("a")
        span=div_b.find("span", class_="autori")

        # print(ha.get_text(),ha["href"],span.get_text().replace("...","").replace(",","##"),pdf_url)
        # print(ha.get_text().strip(),span.get_text().replace("...","").replace(",","##").strip())

    # for h4 in soup.find_all("h4"):
    #     a=h4.find("a")
    #     items=a.get_text().split(",")
    #     vol=items[0].replace("Clinical Neuropsychiatry Volume","")
    #     i=items[1].split("–")
    #     if len(i)!=2:
    #         i=items[1].split("-")
    #     issue=i[0].replace("issue","")
    #     print(vol,issue,i[1],a["href"])
    #


