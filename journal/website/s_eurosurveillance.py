
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
        journal_common_info[Row_Name.ISSN]="1025-496X"
        journal_common_info[Row_Name.JID]="60581"

        url = "https://www.eurosurveillance.org/content/eurosurveillance/browse?page=previous-issues"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")
        ul = soup.find("ul", class_="list-unstyled issue-list expandable")
        for li in ul.find_all("li", class_="volume-item"):
            h5 = li.find("h5")
            line = h5.get_text().strip().split(" ")
            volume = line[1]
            year = line[2][2:-1]
            if int(year) >= 2012 and int(year) <= 2014:
            # if int(year) >= 2015:

                issue_url = "https://www.eurosurveillance.org/content/eurosurveillance/issueslist?volume=" + str(
                    volume) + "&showDates=true"
                issue_data = requests.get(issue_url)
                issue_soup = BeautifulSoup(issue_data.text, "html.parser")
                for issue_li in issue_soup.find_all("li", class_="issue"):
                    info=dict(journal_common_info)
                    a = issue_li.find("a")
                    iurl = "https://www.eurosurveillance.org" + a["href"]

                    span1 = a.find("span", class_="issuenumber")
                    span2 = a.find("span", class_="issueyear").get_text().replace(",", " ").replace("\n", " ").strip()
                    issue = span1.get_text().split(" ")[1]
                    # print(issue, span2, iurl)
                    # if volume=="19"and issue=="13"  :
                    #     info[Row_Name.VOLUME]=volume
                    #     info[Row_Name.YEAR]=year
                    #     info[Row_Name.ISSUE]=issue
                    #     info[Row_Name.STRING_COVER_DATE]=span2
                    #     info[Row_Name.TEMP_URL]=iurl
                    #
                    #     infos.append(info)
                    # elif volume=="19"and issue=="14"  :
                    #     info[Row_Name.VOLUME]=volume
                    #     info[Row_Name.YEAR]=year
                    #     info[Row_Name.ISSUE]=issue
                    #     info[Row_Name.STRING_COVER_DATE]=span2
                    #     info[Row_Name.TEMP_URL]=iurl
                    #
                    #     infos.append(info)
                    # elif volume=="18"and issue=="49"  :
                    #     info[Row_Name.VOLUME]=volume
                    #     info[Row_Name.YEAR]=year
                    #     info[Row_Name.ISSUE]=issue
                    #     info[Row_Name.STRING_COVER_DATE]=span2
                    #     info[Row_Name.TEMP_URL]=iurl
                    #
                    #     infos.append(info)
                    if volume=="18"and issue=="41"  :
                        info[Row_Name.VOLUME]=volume
                        info[Row_Name.YEAR]=year
                        info[Row_Name.ISSUE]=issue
                        info[Row_Name.STRING_COVER_DATE]=span2
                        info[Row_Name.TEMP_URL]=iurl

                        infos.append(info)
                    elif volume=="18"and issue=="40"  :
                        info[Row_Name.VOLUME]=volume
                        info[Row_Name.YEAR]=year
                        info[Row_Name.ISSUE]=issue
                        info[Row_Name.STRING_COVER_DATE]=span2
                        info[Row_Name.TEMP_URL]=iurl

                        infos.append(info)
                    # elif volume=="17"and issue=="36"  :
                    #     info[Row_Name.VOLUME]=volume
                    #     info[Row_Name.YEAR]=year
                    #     info[Row_Name.ISSUE]=issue
                    #     info[Row_Name.STRING_COVER_DATE]=span2
                    #     info[Row_Name.TEMP_URL]=iurl
                    #
                    #     infos.append(info)
                    # elif volume=="17"and issue=="19"  :
                    #     info[Row_Name.VOLUME]=volume
                    #     info[Row_Name.YEAR]=year
                    #     info[Row_Name.ISSUE]=issue
                    #     info[Row_Name.STRING_COVER_DATE]=span2
                    #     info[Row_Name.TEMP_URL]=iurl
                    #
                    #     infos.append(info)
        return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []
        url_set=set()
        data = requests.get(journal_temp[Row_Name.TEMP_URL])
        soup = BeautifulSoup(data.text, "html.parser")
        div = soup.find("div", class_="issueToc")
        for ul in div.find_all("ul", class_="list-unstyled"):

            li1 = ul.find("li", class_="issueTocShowhide")
            if li1 != None:
                at = li1.get_text().strip()
                print(at)
            else:
                at = ""
            for h5 in ul.find_all("h5"):
                a = h5.find("a")
                aurl = "https://www.eurosurveillance.org" + a["href"]
                title = a.get_text().replace("\n", "")
                if not aurl in url_set:
                    url_set.add(aurl)
                    article_info = dict(journal_temp)
                    article_info[Row_Name.TEMP_AURL] = aurl
                    article_info[Row_Name.TITLE] = title
                    article_info[Row_Name.ARTICLE_TYPE] = at
                    urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        div = soup.find("div", class_="pdfItem")
        if div!=None:
            a = div.find("a")
            pdf_url = "https://www.eurosurveillance.org" + a["href"]
            pdf_path=self.download_pdf(pdf_url,dir_name="eurosurveillance")
            if pdf_path!=None:
                info[Row_Name.FULLTEXT_URL]=pdf_url
                info[Row_Name.FULLTEXT_PDF]=pdf_path


        aff_dict = {}
        for v in soup.find_all("span", class_="meta-value affiliations"):
            sup = v.find("sup")
            if sup == None:
                sup_key = 0
            else:
                sup_key = sup.get_text().strip()
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
    url = "https://www.eurosurveillance.org/content/10.2807/1560-7917.ES2013.18.40.20603"
    url_set=set()
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    for li in soup.find_all("li"):
        au_line=li.find("span",class_="meta-value authors")
        if au_line!=None:
            print(repr(au_line.get_text().replace("\n","").strip()))
            break

    aff_dict={}
    for v in soup.find_all("span",class_="meta-value affiliations"):
        sup=v.find("sup")
        if sup==None:
            sup_key=0
        else:
            sup_key=sup.get_text().strip()
        a=v.find("a")
        if a!=None:
            aff_dict[sup_key]=a.get_text().strip()

    print("aff:",aff_dict)
    # eb=soup.find("div",class_="")
    # em=soup.find("div",class_="hidden js-correspondance_email")
    # if em!=None:
    #     s1=em.find("span", class_="js-em1")
    #     s2=em.find("span", class_="js-em2")
    #     em






    # div=soup.find("div",class_="pdfItem")
    # a=div.find("a")
    # pdf_url="https://www.eurosurveillance.org"+a["href"]
    # print(pdf_url)
    # for ul in div.find_all("ul",class_="list-unstyled"):
    #
    #     li1=ul.find("li",class_="issueTocShowhide")
    #     if li1!=None:
    #         at=li1.get_text().strip()
    #     else:
    #         at=""
    #     for h5 in ul.find_all("h5"):
    #         a=h5.find("a")
    #         aurl="https://www.eurosurveillance.org"+a["href"]
    #         title=a.get_text().replace("\n","")
    #         if not aurl in url_set:
    #             url_set.add(aurl)
    #             print(aurl,title)


    # ul=soup.find("ul",class_="list-unstyled issue-list expandable")
    # for li in ul.find_all("li",class_="volume-item"):
    #     h5=li.find("h5")
    #     line=h5.get_text().strip().split(" ")
    #     volume=line[1]
    #     year=line[2][2:-1]
    #     if int(year)>=2010 and int(year)<=2015:
    #         print(volume,year)
    #         issue_url="https://www.eurosurveillance.org/content/eurosurveillance/issueslist?volume="+str(volume)+"&showDates=true"
    #         issue_data=requests.get(issue_url)
    #         issue_soup=BeautifulSoup(issue_data.text, "html.parser")
    #         for issue_li in issue_soup.find_all("li",class_="issue"):
    #             a=issue_li.find("a")
    #             iurl="https://www.eurosurveillance.org"+a["href"]
    #
    #             span1=a.find("span",class_="issuenumber")
    #             span2=a.find("span",class_="issueyear").get_text().replace(","," ").replace("\n"," ").strip()
    #             issue=span1.get_text().split(" ")[1]
    #             print(issue,span2,iurl)
    #             urls.append(iurl)



