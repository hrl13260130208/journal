
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
        journal_common_info[Row_Name.ISSN]="0892-6638"
        journal_common_info[Row_Name.EISSN]="1530-6860"
        journal_common_info[Row_Name.JID]="62251"

        url = "https://www.fasebj.org/loi/fasebj/group/d2010.y2017"
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")
        print(url)
        for div in soup.find_all("div", class_="issue__details"):
            a = div.find("a")
            sd = a.find("span", class_='issue-details__date').get_text().strip()
            vi = a.find("span", class_='issue-details__vol').get_text().strip()
            vis = vi.split(" ")

            volume = vis[0].replace("Vol.", "").strip()
            issue = vis[2].strip()
            year = sd.split(" ")[1]

            if int(year) == 2010 and issue == "1_supplement":
                iurl = "https://www.fasebj.org" + a["href"]
                info = dict(journal_common_info)
                info[Row_Name.VOLUME] = volume
                info[Row_Name.YEAR] = year
                info[Row_Name.ISSUE] = issue
                info[Row_Name.ATTACH] = "Suppl."
                info[Row_Name.STRING_COVER_DATE] = sd
                info[Row_Name.TEMP_URL] = iurl
                infos.append(info)
            if int(year) == 2011 and issue == "1_supplement":
                iurl = "https://www.fasebj.org" + a["href"]
                info = dict(journal_common_info)
                info[Row_Name.VOLUME] = volume
                info[Row_Name.YEAR] = year
                info[Row_Name.ISSUE] = issue
                info[Row_Name.ATTACH] = "Suppl."
                info[Row_Name.STRING_COVER_DATE] = sd
                info[Row_Name.TEMP_URL] = iurl
                infos.append(info)
            if int(year) == 2012 and issue == "1_supplement":
                iurl = "https://www.fasebj.org" + a["href"]
                info = dict(journal_common_info)
                info[Row_Name.VOLUME] = volume
                info[Row_Name.YEAR] = year
                info[Row_Name.ISSUE] = issue
                info[Row_Name.ATTACH] = "Suppl."
                info[Row_Name.STRING_COVER_DATE] = sd
                info[Row_Name.TEMP_URL] = iurl
                infos.append(info)
            if int(year) == 2013 and issue == "1_supplement":
                iurl = "https://www.fasebj.org" + a["href"]
                info = dict(journal_common_info)
                info[Row_Name.VOLUME] = volume
                info[Row_Name.YEAR] = year
                info[Row_Name.ISSUE] = issue
                info[Row_Name.ATTACH] = "Suppl."
                info[Row_Name.STRING_COVER_DATE] = sd
                info[Row_Name.TEMP_URL] = iurl
                infos.append(info)
            if int(year) == 2015 and issue == "1_supplement":
                iurl = "https://www.fasebj.org" + a["href"]
                info = dict(journal_common_info)
                info[Row_Name.VOLUME] = volume
                info[Row_Name.YEAR] = year
                info[Row_Name.ISSUE] = issue
                info[Row_Name.ATTACH] = "Suppl."
                info[Row_Name.STRING_COVER_DATE] = sd
                info[Row_Name.TEMP_URL] = iurl
                infos.append(info)
            if int(year) == 2016 and issue == "1_supplement":
                iurl = "https://www.fasebj.org" + a["href"]
                info = dict(journal_common_info)
                info[Row_Name.VOLUME] = volume
                info[Row_Name.YEAR] = year
                info[Row_Name.ISSUE] = issue
                info[Row_Name.ATTACH] = "Suppl."
                info[Row_Name.STRING_COVER_DATE] = sd
                info[Row_Name.TEMP_URL] = iurl
                infos.append(info)
            if int(year) == 2018 and issue == "1_supplement":
                iurl = "https://www.fasebj.org" + a["href"]
                info = dict(journal_common_info)
                info[Row_Name.VOLUME] = volume
                info[Row_Name.YEAR] = year
                info[Row_Name.ISSUE] = issue
                info[Row_Name.ATTACH] = "Suppl."
                info[Row_Name.STRING_COVER_DATE] = sd
                info[Row_Name.TEMP_URL] = iurl
                infos.append(info)

        return infos

class article(common_article):

    def first(self,journal_temp):
        urls = []
        url_set=set()
        data = requests.get(journal_temp[Row_Name.TEMP_URL],verify=False)
        soup = BeautifulSoup(data.text, "html.parser")

        #增刊
        ul = soup.find("ul", class_="expandable-list__body")
        print(ul)
        for li in ul.find_all("li"):
            try:
                a = li.find("a")
                url="https://www.fasebj.org" + a["href"]
                print(url)
                time.sleep(5)
                data1 = requests.get(url,verify=False)
                soup1 = BeautifulSoup(data1.text, "html.parser")

                for div in soup1.find_all("div", class_="item__body"):
                    # at = div.find("span", class_="badge-type")
                    # if at != None:
                    #     at = at.get_text()
                    h4=div.find("h4")
                    a = h4.find("a")
                    if a != None:
                        aurl = "https://www.fasebj.org" + a["href"]


                        article_info = dict(journal_temp)

                        article_info[Row_Name.TEMP_AURL] = aurl
                        article_info[Row_Name.TITLE] = a.get_text()
                        # article_info[Row_Name.ARTICLE_TYPE] = at
                        urls.append(article_info)
                        if urls.__len__()>100:
                            return urls
            except:
                time.sleep(10)

        print("__________",urls)

        #正常卷期
        # for div in soup1.find_all("div", class_="issue-item"):
        #     at = div.find("span", class_="badge-type")
        #     if at != None:
        #         at = at.get_text()
        #
        #     a = div.find("a")
        #     if a != None:
        #         aurl = "https://www.fasebj.org" + a["href"]
        #
        #         article_info = dict(journal_temp)
        #         for pageline in div.find_all("ul", class_="rlist--inline separator toc-item__detail"):
        #             pageline = pageline.get_text()
        #             pages = re.search("\d+–\d+", pageline)
        #             if pages != None:
        #                 pages = pages.group().split("–")
        #                 article_info[Row_Name.START_PAGE] = pages[0]
        #                 article_info[Row_Name.END_PAGE] = pages[1]
        #                 break
        #
        #         article_info[Row_Name.TEMP_AURL] = aurl
        #         article_info[Row_Name.TITLE] = a.get_text()
        #         article_info[Row_Name.ARTICLE_TYPE] = at
        #         urls.append(article_info)

        return urls

    def second(self,info,text,soup=None):
        info[Row_Name.LANGUAGE]="en"

        abs = soup.find("div", class_="abstractSection abstractInFull")
        if abs != None:
            info[Row_Name.ABSTRACT]=abs.get_text().replace("\n", "").strip()

        li = soup.find("li", class_="coolBar__section coolBar--pdf")
        if li != None:
            a = li.find("a")
            pdf_url = "https://www.fasebj.org" + a["href"]
            pdf_path=self.download_pdf(pdf_url,"fasebj")
            if pdf_path!=None:
                info[Row_Name.FULLTEXT_URL]=pdf_url
                info[Row_Name.FULLTEXT_PDF]=pdf_path



        an_string = ""
        em_string = ""
        af_string = ""
        co_string = ""
        ans = {}

        has_af = False
        has_em = False
        div_a = soup.find("div", class_="accordion-tabbed loa-accordion")
        # print(div_a)
        for div_tag in div_a.find_all("div", {"class": "accordion-tabbed__tab-mobile accordion__closed"}) \
                       + div_a.find_all("div", {"class": "accordion-tabbed__tab-mobile"}):
            a = div_tag.find("a", href="#")
            if a["title"].strip() in ans:
                continue
            else:
                ans[a["title"].strip()] = 1
            an_string += a["title"].strip() + "##"
            div_s = div_tag.find("div", class_="author-info accordion-tabbed__content")
            [s.extract() for s in div_s.find("div", class_="bottom-info")]
            af = ""
            aa = ""
            em = "$$"
            # print(div_tag)
            # print("================", a["title"].strip())
            for p in div_s.find_all("p"):
                # print(p)
                [s.extract() for s in p.find_all("p")]
                p = p.get_text().strip().replace("\n", " ").replace("\r", " ")

                if p.lower().find("correspondence") != -1:
                    pass
                    # co_string += p
                elif p.find("E-mail Address:") != -1:
                    pass
                    # has_em = True
                    # # print(p)
                    # if em.find("$$") != -1:
                    #     em = p.split(":")[1].strip()
                    # else:
                    #     em += ";" + p.split(":")[1].strip()
                    # if p.find(em) == -1:
                    #     co_string += p
                elif p != "":
                    af += p + ";"
                    # print("+++++++++++++++", af)
            em_string += em + "##"
            if af == "":
                af_string += "$$##"
            else:
                af_string += af[:-1] + "##"
                has_af = True

        info[Row_Name.AUTHOR_NAME] = an_string[:-2]
        if has_em:
            info[Row_Name.EMAIL] = em_string[:-2]
        if has_af:
            info[Row_Name.AFFILIATION] = af_string[:-2]

        info[Row_Name.CORRESPONDING] = co_string

        return info

if __name__ == '__main__':
    urls=[]
    url_set=set()
    info={}
    # url = "https://www.fasebj.org/doi/10.1096/fj.201802786RR"
    url = "https://www.fasebj.org/toc/fasebj/24/1_supplement"
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    for ul in soup.find_all("ul",class_="expandable-list__body"):
        for li in ul.find_all("li"):
            a=li.find("a")
            print("https://www.fasebj.org"+a["href"])

    # an_string = ""
    # em_string = ""
    # af_string = ""
    # co_string = ""
    # ans = {}
    #
    # has_af = False
    # has_em = False
    # div_a = soup.find("div", class_="accordion-tabbed loa-accordion")
    # # print(div_a)
    # for div_tag in div_a.find_all("div", {"class": "accordion-tabbed__tab-mobile accordion__closed"}) \
    #                + div_a.find_all("div", {"class": "accordion-tabbed__tab-mobile"}):
    #     a = div_tag.find("a", href="#")
    #     if a["title"].strip() in ans:
    #         continue
    #     else:
    #         ans[a["title"].strip()] = 1
    #     an_string += a["title"].strip() + "##"
    #     div_s = div_tag.find("div", class_="author-info accordion-tabbed__content")
    #     # div_s.find("div", class_="bottom-info")
    #     [s.extract() for s in div_s.find("div", class_="bottom-info")]
    #     af = ""
    #     aa = ""
    #     em = "$$"
    #     print("___________________",div_s)
    #     # print("================", a["title"].strip())
    #     for p in div_s.find_all("p"):
    #         # print(p)
    #         [s.extract() for s in p.find_all("p")]
    #         p = p.get_text().strip().replace("\n", " ").replace("\r", " ")
    #
    #         if p.lower().find("correspondence") != -1:
    #             pass
    #         elif p.find("E-mail Address:") != -1:
    #             pass
    #         elif p != "":
    #             af += p + ";"
    #             print("+++++++++++++++", af)
    #     em_string += em + "##"
    #     if af == "":
    #         af_string += "$$##"
    #     else:
    #         af_string += af[:-1] + "##"
    #         has_af = True
    #
    # info[Row_Name.AUTHOR_NAME] = an_string[:-2]
    # if has_em:
    #     info[Row_Name.EMAIL] = em_string[:-2]
    # if has_af:
    #     info[Row_Name.AFFILIATION] = af_string[:-2]
    #
    # info[Row_Name.CORRESPONDING] = co_string
    #
    # print(info)
    # li=soup.find("li",class_="coolBar__section coolBar--pdf")
    # if li!=None:
    #     a=li.find("a")
    #     pdf_url="https://www.fasebj.org"+a["href"]
    #     print(pdf_url)

    # for div in soup.find_all("div", class_="issue-item"):
    #     at=div.find("span", class_="badge-type")
    #     if at!=None:
    #         at=at.get_text()
    #
    #     a=div.find("a")
    #     if a!=None:
    #         aurl="https://www.fasebj.org"+a["href"]
    #         print(aurl,a.get_text())
    #         for pageline in div.find_all("ul", class_="rlist--inline separator toc-item__detail"):
    #             pageline=pageline.get_text()
    #             pages=re.search("\d+–\d+",pageline)
    #             if pages!=None:
    #                 pages=pages.group().split("–")
    #                 print(pages)




