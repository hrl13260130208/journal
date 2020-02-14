

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
        journal_common_info[Row_Name.ISSN]="0219-8126"
        # journal_common_info[Row_Name.EISSN]="1941-5923"
        journal_common_info[Row_Name.JID]="52932"


        url="https://www.nlb.gov.sg/Browse/BiblioAsia.aspx"
        data=requests.get(url)


        # info = dict(journal_common_info)
        # info[Row_Name.VOLUME] = "11"
        # info[Row_Name.YEAR] = "2010"
        # info[Row_Name.ISSUE] = "null"
        # info[Row_Name.TEMP_URL] = "https://www.amjcaserep.com/archives/issue/idIssue/834890"
        # infos.append(info)
        # info = dict(journal_common_info)
        # info[Row_Name.VOLUME] = "12"
        # info[Row_Name.YEAR] = "2011"
        # info[Row_Name.ISSUE] = "null"
        # info[Row_Name.TEMP_URL] = "https://www.amjcaserep.com/archives/issue/idIssue/834980"
        # infos.append(info)
        # info = dict(journal_common_info)
        # info[Row_Name.VOLUME] = "13"
        # info[Row_Name.YEAR] = "2012"
        # info[Row_Name.ISSUE] = "null"
        # info[Row_Name.TEMP_URL] = "https://www.amjcaserep.com/archives/issue/idIssue/835039"
        # infos.append(info)
        # info = dict(journal_common_info)
        # info[Row_Name.VOLUME] = "14"
        # info[Row_Name.YEAR] = "2013"
        # info[Row_Name.ISSUE] = "null"
        # info[Row_Name.TEMP_URL] = "https://www.amjcaserep.com/archives/issue/idIssue/835152"
        # infos.append(info)

        return infos

if __name__ == '__main__':
    url = "https://www.nlb.gov.sg/Browse/BiblioAsia.aspx"
    data = requests.get(url)
    soup=BeautifulSoup(data.text,"html.parser")
    # print(soup)
    for div in soup.find_all("div",class_="row-fluid"):
        for a in div.find_all("a"):

            text=a.get_text().strip()
            # print(text)
            y=re.search("\d{4}",text)
            if y==None:
                continue
            year=y.group()
            if int(year)>=2010 and int(year)<2016:
                temp_i = text.split(",")
                ti2=temp_i[0].split(" ")
                vol=ti2[1]
                issue=ti2[3]
                scd=temp_i[1]
                print(vol,issue,scd,a["href"])






