
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
from journal.common import Row_Name,common_website,common_journals,common_article



class journals(common_journals):

    #期刊：Journal of Medical Microbiology: An Official Journal of the Pathological Society of Great Britain and Ireland
    def get(self,website,journal,url):
        infos=[]
        journal_common_info={}
        journal_common_info[Row_Name.JOURNAL_TITLE] = journal
        journal_common_info[Row_Name.PUBLISHER] = website
        journal_common_info[Row_Name.ISSN]="0022-2615"
        journal_common_info[Row_Name.EISSN]="1473-5644"
        journal_common_info[Row_Name.JID]="61399"

        # url = "https://www.microbiologyresearch.org/content/journal/jmm/browse?page=previous-issues"
        # data = requests.get(url,verify=False)
        # soup = BeautifulSoup(data.text, "html.parser")
        # ul = soup.find("ul", class_="list-unstyled issue-list expandable")
        # for li in ul.find_all("li", class_="volume-item"):
        #     h5 = li.find("h5")
        #     line = h5.get_text().strip().split(" ")
        #     volume = line[1]
        #     year = line[2][2:-1]
        #     if int(year) >= 2010 and int(year) <= 2015:
        #
        #         issue_url = "https://www.microbiologyresearch.org//content/journal/jmm/issueslist?volume=" + str(
        #             volume) + "&showDates=false"
        #
        #         issue_data = requests.get(issue_url)
        #         issue_soup = BeautifulSoup(issue_data.text, "html.parser")
        #         for issue_li in issue_soup.find_all("li", class_="issue"):
        #             info=dict(journal_common_info)
        #             # info = dict()
        #             a = issue_li.find("a")
        #             iurl = "https://www.microbiologyresearch.org" + a["href"]
        #
        #             span1 = a.find("span", class_="issuenumber")
        #             span2 = a.find("span", class_="issueyear").get_text().replace(",", " ").replace("\n", " ").strip()
        #             issue = span1.get_text().split(" ")[1]
        #             # print(issue, span2, iurl)
        #             info[Row_Name.VOLUME] = volume
        #             info[Row_Name.YEAR] = year
        #             info[Row_Name.ISSUE] = issue
        #             info[Row_Name.STRING_COVER_DATE] = span2
        #             info[Row_Name.TEMP_URL] = iurl
        #
        #             infos.append(info)
        #
        #     if int(year) == 2017:
        #
        #         issue_url = "https://www.microbiologyresearch.org//content/journal/jmm/issueslist?volume=" + str(
        #             volume) + "&showDates=false"
        #
        #         issue_data = requests.get(issue_url)
        #         issue_soup = BeautifulSoup(issue_data.text, "html.parser")
        #         for issue_li in issue_soup.find_all("li", class_="issue"):
        #             info=dict(journal_common_info)
        #             # info = dict()
        #             a = issue_li.find("a")
        #             iurl = "https://www.microbiologyresearch.org" + a["href"]
        #
        #             span1 = a.find("span", class_="issuenumber")
        #             span2 = a.find("span", class_="issueyear").get_text().replace(",", " ").replace("\n", " ").strip()
        #             issue = span1.get_text().split(" ")[1]
        #             # print(issue, span2, iurl)
        #             if issue=="9":
        #                 info[Row_Name.VOLUME] = volume
        #                 info[Row_Name.YEAR] = year
        #                 info[Row_Name.ISSUE] = issue
        #                 info[Row_Name.STRING_COVER_DATE] = span2
        #                 info[Row_Name.TEMP_URL] = iurl
        #
        #                 infos.append(info)
        #     if int(year) == 2018:
        #
        #         issue_url = "https://www.microbiologyresearch.org//content/journal/jmm/issueslist?volume=" + str(
        #             volume) + "&showDates=false"
        #
        #         issue_data = requests.get(issue_url)
        #         issue_soup = BeautifulSoup(issue_data.text, "html.parser")
        #         for issue_li in issue_soup.find_all("li", class_="issue"):
        #             info=dict(journal_common_info)
        #             # info = dict()
        #             a = issue_li.find("a")
        #             iurl = "https://www.microbiologyresearch.org" + a["href"]
        #
        #             span1 = a.find("span", class_="issuenumber")
        #             span2 = a.find("span", class_="issueyear").get_text().replace(",", " ").replace("\n", " ").strip()
        #             issue = span1.get_text().split(" ")[1]
        #             # print(issue, span2, iurl)
        #             if issue == "2" or issue=="4":
        #                 info[Row_Name.VOLUME] = volume
        #                 info[Row_Name.YEAR] = year
        #                 info[Row_Name.ISSUE] = issue
        #                 info[Row_Name.STRING_COVER_DATE] = span2
        #                 info[Row_Name.TEMP_URL] = iurl
        #
        #                 infos.append(info)

        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "62"
        info[Row_Name.YEAR] = "2013"
        info[Row_Name.ISSUE] ="1"
        # info[Row_Name.STRING_COVER_DATE] = span2
        info[Row_Name.TEMP_URL] = "https://www.microbiologyresearch.org/content/journal/jmm/62/1"
        infos.append(info)
        info = dict(journal_common_info)
        info[Row_Name.VOLUME] = "61"
        info[Row_Name.YEAR] = "2012"
        info[Row_Name.ISSUE] ="12"
        # info[Row_Name.STRING_COVER_DATE] = span2
        info[Row_Name.TEMP_URL] = "https://www.microbiologyresearch.org/content/journal/jmm/61/12"
        infos.append(info)
        return infos

    #期刊：Microbiology
    # def get(self,website,journal,url):
    #     infos=[]
    #     journal_common_info={}
    #     journal_common_info[Row_Name.JOURNAL_TITLE] = journal
    #     journal_common_info[Row_Name.PUBLISHER] = website
    #     journal_common_info[Row_Name.ISSN]="1350-0872"
    #     journal_common_info[Row_Name.EISSN]="1465-2080"
    #     journal_common_info[Row_Name.JID]="61398"
    #
    #     url = "https://www.microbiologyresearch.org/content/journal/micro/browse?page=previous-issues"
    #     data = requests.get(url,verify=False)
    #     soup = BeautifulSoup(data.text, "html.parser")
    #     ul = soup.find("ul", class_="list-unstyled issue-list expandable")
    #     for li in ul.find_all("li", class_="volume-item"):
    #         h5 = li.find("h5")
    #         line = h5.get_text().strip().split(" ")
    #         volume = line[1]
    #         year = line[2][2:-1]
    #         # if int(year) == 2016 or int(year) == 2015 or int(year)==2013:
    #         #
    #         #     issue_url = "https://www.microbiologyresearch.org/content/journal/micro/issueslist?volume=" + str(
    #         #         volume) + "&showDates=false"
    #         #
    #         #     issue_data = requests.get(issue_url)
    #         #     issue_soup = BeautifulSoup(issue_data.text, "html.parser")
    #         #     for issue_li in issue_soup.find_all("li", class_="issue"):
    #         #         info=dict(journal_common_info)
    #         #         # info = dict()
    #         #         a = issue_li.find("a")
    #         #         iurl = "https://www.microbiologyresearch.org" + a["href"]
    #         #
    #         #         span1 = a.find("span", class_="issuenumber")
    #         #         span2 = a.find("span", class_="issueyear").get_text().replace(",", " ").replace("\n", " ").strip()
    #         #         issue = span1.get_text().split(" ")[1]
    #         #         # print(issue, span2, iurl)
    #         #         info[Row_Name.VOLUME] = volume
    #         #         info[Row_Name.YEAR] = year
    #         #         info[Row_Name.ISSUE] = issue
    #         #         info[Row_Name.STRING_COVER_DATE] = span2
    #         #         info[Row_Name.TEMP_URL] = iurl
    #         #
    #         #         infos.append(info)
    #
    #         if int(year) == 2012:
    #             print("------------")
    #
    #             issue_url = "https://www.microbiologyresearch.org/content/journal/micro/issueslist?volume=" + str(
    #                 volume) + "&showDates=false"
    #             # print(issue_url)
    #             issue_data = requests.get(issue_url)
    #
    #             issue_soup = BeautifulSoup(issue_data.text, "html.parser")
    #             print(issue_soup)
    #             for issue_li in issue_soup.find_all("li", class_="issue"):
    #                 info=dict(journal_common_info)
    #                 # info = dict()
    #                 a = issue_li.find("a")
    #                 iurl = "https://www.microbiologyresearch.org" + a["href"]
    #
    #                 span1 = a.find("span", class_="issuenumber")
    #                 span2 = a.find("span", class_="issueyear").get_text().replace(",", " ").replace("\n", " ").strip()
    #                 issue = span1.get_text().split(" ")[1]
    #                 print(issue, span2, iurl)
    #                 if issue=="9" or issue=="8":
    #                     info[Row_Name.VOLUME] = volume
    #                     info[Row_Name.YEAR] = year
    #                     info[Row_Name.ISSUE] = issue
    #                     info[Row_Name.STRING_COVER_DATE] = span2
    #                     info[Row_Name.TEMP_URL] = iurl
    #
    #                     infos.append(info)
    #     return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []
        url_set=set()
        data = requests.get(journal_temp[Row_Name.TEMP_URL],verify=False)
        soup = BeautifulSoup(data.text, "html.parser")
        div = soup.find("div", class_="issueToc")
        for ul in div.find_all("ul", class_="list-unstyled"):

            li1 = ul.find("li", class_="issueTocShowhide")
            if li1 != None:
                at = li1.get_text().strip()
                # print(at)
            else:
                at = ""
            for h5 in ul.find_all("h4"):
                a = h5.find("a")
                aurl = "https://www.microbiologyresearch.org" + a["href"].replace("\n", "")
                title = a.get_text().replace("\n", "")
                if not aurl in url_set:
                    url_set.add(aurl)
                    # article_info = dict()
                    article_info = dict(journal_temp)
                    # print(aurl)
                    article_info[Row_Name.TEMP_AURL] = aurl
                    article_info[Row_Name.TITLE] = title
                    article_info[Row_Name.ARTICLE_TYPE] = at
                    urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        div = soup.find("div", class_="download-pdf")
        if div!=None:
            fr = div.find("form")
            pdf_url = "https://www.microbiologyresearch.org" + fr["action"]
            pdf_path=self.download_pdf(pdf_url,dir_name="microbiologyresearch")
            if pdf_path!=None:
                info[Row_Name.FULLTEXT_URL]=pdf_url
                info[Row_Name.FULLTEXT_PDF]=pdf_path


        aff_dict = {}
        for v in soup.find_all("span", class_="meta-value affiliations"):
            sup = v.find("sup")
            if sup == None:
                sup_key = 0
            else:
                sup_key = sup.get_text().replace("\u200b","").strip()
            a = v.find("a")
            if a != None:
                aff_dict[sup_key] = a.get_text().strip()

        au_dict = None
        for li in soup.find_all("li"):
            au_line = li.find("span", class_="meta-value authors")
            if au_line != None:
                a = au_line.get_text().replace("\n", "").strip()
                au_dict = self.clear_authors(a,aff_dict.keys())
                break

        au,em,aff=self.get_author_email_aff(au_dict,{},aff_dict)
        info[Row_Name.AUTHOR_NAME]=au
        info[Row_Name.AFFILIATION]=aff

        return info

if __name__ == '__main__':
    urls=[]
    url_set=set()
    url = "https://www.microbiologyresearch.org/content/journal/micro/10.1099/mic.0.000082"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")


    sa=article(None)
    aff_dict = {}
    for v in soup.find_all("span", class_="meta-value affiliations"):
        sup = v.find("sup")
        if sup == None:
            sup_key = 0
        else:
            sup_key = sup.get_text().replace("\u200b","").strip()
            print(sup_key)
        a = v.find("a")
        if a != None:
            aff_dict[sup_key] = a.get_text().strip()

    au_dict = None
    for li in soup.find_all("li"):
        au_line = li.find("span", class_="meta-value authors")
        if au_line != None:
            a = au_line.get_text().replace("\n", "").strip()
            print(a)
            au_dict = sa.clear_authors(a, aff_dict.keys())
            break

    print(sa.get_author_email_aff(au_dict, {}, aff_dict))



    # div = soup.find("div", class_="issueToc")
    # for ul in div.find_all("ul", class_="list-unstyled"):
    #
    #     li1 = ul.find("li", class_="issueTocShowhide")
    #     if li1 != None:
    #         at = li1.get_text().strip()
    #         print(at)
    #     else:
    #         at = ""
    #     for h5 in ul.find_all("h4"):
    #         a = h5.find("a")
    #         aurl = "https://www.microbiologyresearch.org" + a["href"].replace("\n","")
    #         title = a.get_text().replace("\n", "")
    #         if not aurl in url_set:
    #             url_set.add(aurl)
    #             article_info = dict()
    #             # article_info = dict(journal_temp)
    #             print(aurl)
    #             article_info[Row_Name.TEMP_AURL] = aurl
    #             article_info[Row_Name.TITLE] = title
    #             article_info[Row_Name.ARTICLE_TYPE] = at
    #             urls.append(article_info)
    #
    # print(urls)
    # ul = soup.find("ul", class_="list-unstyled issue-list expandable")
    # for li in ul.find_all("li", class_="volume-item"):
    #     h5 = li.find("h5")
    #     line = h5.get_text().strip().split(" ")
    #     volume = line[1]
    #     year = line[2][2:-1]
    #     if int(year) >= 2010 and int(year) <= 2015:
    #
    #         issue_url = "https://www.microbiologyresearch.org//content/journal/jmm/issueslist?volume=" + str(
    #             volume) + "&showDates=false"
    #
    #         print(issue_url)
    #         issue_data = requests.get(issue_url)
    #         issue_soup = BeautifulSoup(issue_data.text, "html.parser")
    #         for issue_li in issue_soup.find_all("li", class_="issue"):
    #             # info=dict(journal_common_info)
    #             info=dict()
    #             a = issue_li.find("a")
    #             iurl = "https://www.microbiologyresearch.org" + a["href"]
    #
    #             span1 = a.find("span", class_="issuenumber")
    #             span2 = a.find("span", class_="issueyear").get_text().replace(",", " ").replace("\n", " ").strip()
    #             issue = span1.get_text().split(" ")[1]
    #             # print(issue, span2, iurl)
    #             info[Row_Name.VOLUME]=volume
    #             info[Row_Name.YEAR]=year
    #             info[Row_Name.ISSUE]=issue
    #             info[Row_Name.STRING_COVER_DATE]=span2
    #             info[Row_Name.TEMP_URL]=iurl
    #
    #             infos.append(info)
    # print(infos)


