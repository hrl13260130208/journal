
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
import PyPDF2
from journal.common import Row_Name,common_website,common_journals,common_article



class journals(common_journals):

    def get(self,website,journal,url):
        infos=[]
        journal_common_info={}
        journal_common_info[Row_Name.JOURNAL_TITLE] = journal
        journal_common_info[Row_Name.PUBLISHER] = website
        # journal_common_info[Row_Name.ISSN]="0891-2017"
        journal_common_info[Row_Name.EISSN]="1941-5923"
        journal_common_info[Row_Name.JID]="60967"



        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "11"
        info[Row_Name.YEAR] = "2010"
        info[Row_Name.ISSUE] = "null"
        info[Row_Name.TEMP_URL] = "https://www.amjcaserep.com/archives/issue/idIssue/834890"
        infos.append(info)
        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "12"
        info[Row_Name.YEAR] = "2011"
        info[Row_Name.ISSUE] = "null"
        info[Row_Name.TEMP_URL] = "https://www.amjcaserep.com/archives/issue/idIssue/834980"
        infos.append(info)
        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "13"
        info[Row_Name.YEAR] = "2012"
        info[Row_Name.ISSUE] = "null"
        info[Row_Name.TEMP_URL] = "https://www.amjcaserep.com/archives/issue/idIssue/835039"
        infos.append(info)
        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "14"
        info[Row_Name.YEAR] = "2013"
        info[Row_Name.ISSUE] = "null"
        info[Row_Name.TEMP_URL] = "https://www.amjcaserep.com/archives/issue/idIssue/835152"
        infos.append(info)

        return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []
        url_set=set()
        data = requests.get(journal_temp[Row_Name.TEMP_URL],verify=False)
        soup = BeautifulSoup(data.text, "html.parser")

        for a in soup.find_all("a", class_="title"):

            article_info = dict(journal_temp)

            article_info[Row_Name.TEMP_AURL] = a["href"]
            article_info[Row_Name.TITLE] = a.get_text()

            urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        if Row_Name.FULLTEXT_URL in info.keys():
            # print(info[Row_Name.FULLTEXT_URL])
            data=requests.get(info[Row_Name.FULLTEXT_URL],verify=False)

            soup=BeautifulSoup(data.text,"html.parser")
            # print(soup)
            in1=soup.find("input",{"name":"ID_JOUR"})
            in2=soup.find("input",{"name":"idArt"})
            # print("=================",in1,in2)
            pdf_path = self.download_pdf("https://www.amjcaserep.com/download/getFreePdf/l/EN",
                                         dir_name="amjcaserep",post=True,
                                         post_data={"ID_JOUR": int(in1["value"]),"idArt": int(in2["value"])},check_pdf=False)
            if pdf_path != None:
                info[Row_Name.FULLTEXT_PDF] = pdf_path


        return info


def checkpdf(file):
    pdf = PyPDF2.PdfFileReader(file,strict=False)
    pages=pdf.getNumPages()
    return pages



if __name__ == '__main__':
    urls=[]
    url_set=set()
    info={}
    file=r"C:\temp\other\test.pdf"

    # url = "https://www.amjcaserep.com/abstract/index/idArt/889353"
    # data = requests.get(url,verify=False)
    # soup = BeautifulSoup(data.text, "html.parser")
    url="https://www.amjcaserep.com/download/getFreePdf/l/EN"
    data=requests.post(url,data={"ID_JOUR": 2669,"idArt": 882208},verify=False)
    # data.encoding = 'utf-8'
    file = open(file, "wb+")
    file.write(data.content)

    checkpdf(file)
    file.close()

    # print(get_author_and_aff_from_head(soup))

    # for a in soup.find_all("a",class_="title"):
    #     print(a["href"],a.get_text())
    #







