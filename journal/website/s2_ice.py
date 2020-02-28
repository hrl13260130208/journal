

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
        journal_common_info[Row_Name.EISSN]="2045-2543"
        journal_common_info[Row_Name.JID]="52669"

        url = "https://www.icevirtuallibrary.com/loi/jgele?expanded=v9&expanded=v8&expanded=v7&expanded=v1"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")

        for div in soup.find_all("div", class_="js_issue"):
            a = div.find("a")
            span = div.find("span", class_="coverDateText")
            line = a.get_text().strip()
            s = span.get_text().strip()
            v = re.search("Volume \d*", line)
            i = re.search("Issue \d*", line)
            vol = v.group().split(" ")[1]
            issue = i.group().split(" ")[1]
            s = s.replace("(", "").replace(",", "")
            year=re.search("\d{4}",s).group()
            print(vol, issue, s)
            if int(vol)==7 and int(issue)==4:
                info = dict(journal_common_info)
                info[Row_Name.VOLUME] = vol
                info[Row_Name.YEAR] = year
                info[Row_Name.STRING_COVER_DATE] = s
                info[Row_Name.ISSUE] = issue
                info[Row_Name.TEMP_URL] = "https://www.icevirtuallibrary.com"+a["href"]
                infos.append(info)
            if int(vol)<=5:
                info = dict(journal_common_info)
                info[Row_Name.VOLUME] = vol
                info[Row_Name.YEAR] = year
                info[Row_Name.STRING_COVER_DATE] = s
                info[Row_Name.ISSUE] = issue
                info[Row_Name.TEMP_URL] = "https://www.icevirtuallibrary.com" + a["href"]
                infos.append(info)



        return infos


class article(common_article):

    def first(self,journal_temp):
        urls = []

        data = requests.get(journal_temp[Row_Name.TEMP_URL],verify=False)
        soup = BeautifulSoup(data.text, "html.parser")
        # print(soup)

        for table in soup.find_all("table", class_="articleEntry"):
            article_info = dict(journal_temp)
            t = table.find("div", class_="art_title linkable")
            ta = t.find("a")
            title = ta.get_text()

            div1 = table.find("div", class_="tocAuthors afterTitle")
            au = ""
            for a in div1.find_all("a"):
                au += a.get_text().strip() + "##"
            print(au[:-2])

            pages = table.find("span", class_="articlePageRange issueInProgress")
            if pages == None:
                pages = table.find("span", class_="articlePageRange")

            line = pages.get_text().replace(",", "").replace("pp.", "").strip()
            if "–" in line:
                ps = line.split("–")
                article_info[Row_Name.START_PAGE]=ps[0]
                article_info[Row_Name.END_PAGE]= ps[1]
            else:
                article_info[Row_Name.START_PAGE] = line
                article_info[Row_Name.END_PAGE] = line

            pa = table.find("a", class_="ref nowrap pdf")

            article_info[Row_Name.TITLE] = title
            article_info[Row_Name.TEMP_AURL] = "https://www.icevirtuallibrary.com" + ta["href"]
            article_info[Row_Name.FULLTEXT_URL] = "https://www.icevirtuallibrary.com" + pa["href"]
            article_info[Row_Name.AUTHOR_NAME] = au

            urls.append(article_info)

        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        div = soup.find("div", class_="abstractSection abstractInFull")
        if div != None:
            info[Row_Name.ABSTRACT]=div.get_text()

        # aff={}
        # for div in soup.find_all("div",class_="authorAffiliationEnt"):
        #     sup=div.find("sup")
        #     if sup!=None:
        #         key=sup.get_text().strip()
        #         sup.extract()
        #         aff[key]=div.get_text()
        #     else:
        #         sup,text=self.find_first(div.get_text())
        #         if sup==None:
        #             aff["0"]+=text
        #         else:
        #             aff[sup]=text
        # div1=soup.find("div", class_="hlFld-ContribAuthor")
        # authors=self.clear_authors(div1.get_text(),aff.keys())
        # au,em,aff=self.get_author_email_aff(author_dict=authors,email_dict={},aff_dict=aff)
        # info[Row_Name.AUTHOR_NAME]=au
        # info[Row_Name.AFFILIATION]=aff
        if Row_Name.FULLTEXT_URL in info.keys():
            pdf_path = self.download_pdf(info[Row_Name.FULLTEXT_URL], dir_name="bci")
            if pdf_path != None:
                info[Row_Name.FULLTEXT_PDF] = pdf_path

        return info


if __name__ == '__main__':

    url = "https://www.icevirtuallibrary.com/doi/full/10.1680/geolett.14.00061"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")
    div1 = soup.find("span", class_="NLM_contrib-group")
    print(div1)

    #
    # # print(soup)
    #
    # for table in soup.find_all("table",class_="articleEntry"):
    #     t=table.find("div", class_="art_title linkable")
    #     ta=t.find("a")
    #     title=ta.get_text()
    #     # print(title,"https://www.icevirtuallibrary.com"+ta["href"])
    #
    #     div1 = table.find("div", class_="tocAuthors afterTitle")
    #     au = ""
    #     for a in div1.find_all("a"):
    #         au += a.get_text().strip() + "##"
    #     print(au[:-2])
    #
    #     pages = table.find("span", class_="articlePageRange issueInProgress")
    #     if pages == None:
    #         pages = table.find("span", class_="articlePageRange")
    #
    #     line=pages.get_text().replace(",","").replace("pp.","").strip()
    #     if "–" in line:
    #         ps=line.split("–")
    #         print(ps[0],ps[1])
    #     else:
    #         print(line)
    #
    #     pa=table.find("a",class_="ref nowrap pdf")
    #     print("https://www.icevirtuallibrary.com"+pa["href"])




