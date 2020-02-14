

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
        journal_common_info[Row_Name.EISSN]="1939-2389"
        journal_common_info[Row_Name.JID]="52429"

        url = "http://blogs.shu.edu/ghg/"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")
        # print(soup)

        ul = soup.find("ul", id="widget-collapsarch-2-top")
        for li in ul.find_all("li"):
            year = re.search("\d{4}", li.get_text())
            if year != None:
                if year.group() == "2015" or year.group() == "2014":
                    for li1 in li.find_all("li", class_='collapsing archives expand'):
                        span = li1.find("span", title='click to expand')
                        a = span.find("a")

                        info = dict(journal_common_info)
                        info[Row_Name.VOLUME] = year.group()
                        info[Row_Name.YEAR] = year.group()
                        info[Row_Name.ISSUE] = a.get_text()
                        info[Row_Name.TEMP_URL] = a["href"]
                        infos.append(info)

        return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []

        data = requests.get(journal_temp[Row_Name.TEMP_URL],verify=False)
        soup = BeautifulSoup(data.text, "html.parser")
        # print(soup)
        for h2 in soup.find_all("h2"):
            a = h2.find("a")
            # print(a.get_text(), a["href"])

            article_info = dict(journal_temp)

            article_info[Row_Name.TEMP_AURL] = a["href"]
            article_info[Row_Name.TITLE] = a.get_text()

            urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        # if Row_Name.FULLTEXT_URL in info.keys():
            # print(info[Row_Name.FULLTEXT_URL])
            # data=requests.get(info[Row_Name.FULLTEXT_URL],verify=False)
            #
            # soup=BeautifulSoup(data.text,"html.parser")
            # # print(soup)
            # in1=soup.find("input",{"name":"ID_JOUR"})
            # in2=soup.find("input",{"name":"idArt"})
            # # print("=================",in1,in2)
            # pdf_path = self.download_pdf("https://www.amjcaserep.com/download/getFreePdf/l/EN",
            #                              dir_name="amjcaserep",post=True,
            #                              post_data={"ID_JOUR": int(in1["value"]),"idArt": int(in2["value"])},check_pdf=False)
            # if pdf_path != None:
            #     info[Row_Name.FULLTEXT_PDF] = pdf_path


        return info





if __name__ == '__main__':
    url = "http://blogs.shu.edu/ghg/2015/10/"
    data = requests.get(url)
    soup=BeautifulSoup(data.text,"html.parser")
    # print(soup)
    for h2 in soup.find_all("h2"):
        a=h2.find("a")
        print(a.get_text(),a["href"])

    # for li in soup.find_all("li",class_="collapsing archives expand"):
    #





