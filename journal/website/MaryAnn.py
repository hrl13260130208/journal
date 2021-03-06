import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
from journal.redis_manager import name_manager
from journal.common import Row_Name,common_website,common_journals,common_article
from journal.job import jobs
import logging


logger=logging.getLogger("logger")

def wait():
    time.sleep(random.random() * 4+3)
class website(common_website):

    def get(self,section,url):

        wait()
        data=requests.get(url)
        soup=BeautifulSoup(data.text,"html.parser")
        for div_row in soup.find_all("div",class_="row"):
            for div_tag in div_row.find_all("div",class_="col-sm-6 col-md-3 my-2"):
                a=div_tag.find("a")["href"]
                url="https://home.liebertpub.com"+a
                wait()
                logger.info("解析MaryAnn的期刊："+url)
                try:
                    data2 = requests.get(url)
                except:
                    time.sleep(10)
                    data2 = requests.get(url)
                bs = BeautifulSoup(data2.text, "html.parser")
                issn_url=""
                for a in bs.find_all("a", class_="nav-link px-3"):
                    if a.get_text().strip() == "All Issues":
                        issn_url=a["href"]

                if issn_url == "":
                    for li in bs.find_all("li", class_="nav-item dropdown btn-group"):
                        if li.get_text().find("All Issues") != -1:
                            for a_tag in li.find_all("a", class_="dropdown-item"):
                                journal_title = a_tag.get_text()
                                issn_url = a_tag["href"]
                                self.set_list(journal_title, issn_url)
                    continue
                journal_title = bs.find("h1", class_="journal-title").get_text().strip().replace("\n"," ").replace("\r"," ")

                self.set_list(journal_title, issn_url)



class journals(common_journals):

    def get(self,website,journal,url):
        journals_list=[]
        journal_common_info=self.get_common(journal,url)

        if journal.find("  ")!=-1:
            journal_common_info[Row_Name.JOURNAL_TITLE] = journal[:journal.find("  ")]
        else:
            journal_common_info[Row_Name.JOURNAL_TITLE] = journal
        journal_common_info[Row_Name.PUBLISHER] = website

        wait()
        data = requests.get(url)
        bs = BeautifulSoup(data.text, "html.parser")
        div = bs.find("div", class_="loi tab loi-tab-2")

        ul = div.find("ul", class_="rlist tab__content")
        for li in ul.find_all("li", class_="col-md-4"):
            issue_info = dict(journal_common_info)

            cdate = li.find("span", class_="coverDate").get_text().strip()
            issue_info[Row_Name.STRING_COVER_DATE] = cdate
            issue_info[Row_Name.YEAR] = cdate[-4:]
            for a in li.find_all("a"):
                a_text = a.get_text().strip()
                vol_num = a_text.find("Vol")
                if vol_num != -1:
                    issue_num = a_text.find("Issue")
                    issue_info[Row_Name.VOLUME] = a_text[vol_num + 4:issue_num].strip()
                    issue_info[Row_Name.ISSUE] = a_text[issue_num + 6:].strip()
                    issue_info[Row_Name.TEMP_URL]="https://www.liebertpub.com"+a["href"]
                    journals_list.append(issue_info)
        return journals_list


    def get_common(self,journal,url):
        info={}
        common=self.nm.get_journal_common_info(journal)

        if common ==None:
            wait()
            ha={
            "authority": "www.liebertpub.com",
            "method": "GET",
            "path": "/loi/VOR",
            "scheme": "https",
            "upgrade - insecure - requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
            }
            cookie=" I2KBRCK=1; MAID=bTY2/0pIlThlENHcxBGyPQ==; _ga=GA1.2.2018801126.1543481100; gdprCookie=Cookies policy accepted; seerid=86715.61259763717; seerid=86715.61259763717; PathforaImpressions_95ee3ae4ffcc3bcb7ff6ee6329a77114=2%7C1553048980739; PathforaClosed_95ee3ae4ffcc3bcb7ff6ee6329a77114=2%7C1553048982823; __atuvc=40%7C9%2C11%7C10%2C4%7C11%2C5%7C12%2C3%7C13; __attag=%22lio%3Aly_unknown_email%2Clio%3Aly_frequent_user%2Clio%3Asmt_power%2Clio%3Aall%2Clio%3A95ee3ae4ffcc3bcb7ff6ee6329a77114_reach%2Clio%3Aaudhighlyengaged%2Clio%3Aaud_unknown_users%22%2Clio%3Aly_unknown_email%2Clio%3Aaud_unknown_users; _gid=GA1.2.1969530633.1553669761; SERVER=WZ6myaEXBLGexQVnui0xrg==; MACHINE_LAST_SEEN=2019-03-27T23%3A54%3A27.951-07%3A00; JSESSIONID=aaaT0kUlxcj7G7WTwxwMw; seerses=e; seerses=e; ly_segs=%7B%22ly_unknown_email%22%3A%22ly_unknown_email%22%2C%22ly_frequent_user%22%3A%22ly_frequent_user%22%2C%22smt_power%22%3A%22smt_power%22%2C%22all%22%3A%22all%22%2C%2295ee3ae4ffcc3bcb7ff6ee6329a77114_reach%22%3A%2295ee3ae4ffcc3bcb7ff6ee6329a77114_reach%22%2C%22audhighlyengaged%22%3A%22audhighlyengaged%22%2C%22aud_unknown_users%22%3A%22aud_unknown_users%22%7D; cookiePolicy=iaccept; _gat__gaenor=1; PathforaPageView=191"
            c = {}
            for a in cookie.split(";"):
                a = a.split("=")
                c[a[0]] = a[1]
            data = requests.get(url,headers=ha)

            bs = BeautifulSoup(data.text, "html.parser")
            # print(bs)
            div = bs.find("div", class_="text-minute margin-bottom--small")
            div_str = div.get_text().strip()
            for s in div_str.split("|"):
                if s.find("Online ISSN:") != -1:
                    info[Row_Name.EISSN] = s[13:].strip()
                elif s.find("ISSN:") != -1:
                    info[Row_Name.ISSN] = s[5:].strip()

            if Row_Name.ISSN not in info and Row_Name.EISSN not in info:
                raise ValueError("issn与eissn为空！")
            self.nm.save_journal_common_info(journal,json.dumps(info))
            return info
        else:
            return json.loads(common)


class article(common_article):

    def first(self,journal_temp):
        urls=[]
        wait()
        data = requests.get(journal_temp[Row_Name.TEMP_URL])
        bs = BeautifulSoup(data.text, "html.parser")

        div = bs.find("div", class_="table-of-content")
        for i in div.find_all("div", class_="issue-item"):
            article_info = dict(journal_temp)
            # i=div.find("div",class_="issue-item")
            title = i.find("h5")
            article_url = title.find("a")["href"]
            article_info[Row_Name.TEMP_AURL]="https://www.liebertpub.com" + article_url

            article_start_page = i.find("ul", class_="rlist--inline separator toc-item__detail")
            for li in article_start_page.find_all("li"):
                if li.get_text().find("Page") != -1:
                    [s.extract() for s in li.find("span")]
                    strs = li.get_text().split("–")
                    try:
                        start_p = int(strs[0])
                        if strs.__len__() < 2:
                            end_p = int(strs[0])
                        else:
                            end_p = int(strs[1])
                        p_t = end_p - start_p + 1
                    except:
                        start_p = strs[0]
                        end_p = strs[1]
                        num_0 = re.search("\d+", strs[0])
                        num_1 = re.search("\d+", strs[1])
                        try:
                            p_t = int(strs[1][num_1.span()[0]:num_1.span()[1]]) - int(
                                strs[0][num_0.span()[0]:num_0.span()[1]])
                        except:
                            pass

                    article_info[Row_Name.START_PAGE] = start_p
                    article_info[Row_Name.END_PAGE] = end_p
                    article_info[Row_Name.PAGE_TOTAL] = p_t
                elif li.get_text().find("Published Online:") != -1:
                    [s.extract() for s in li.find("span")]
                    self.set_possible_none_item(article_info, Row_Name.STRING_PUB_DATE, li)

            urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):


        bs_c = BeautifulSoup(text, "html.parser")

        info[Row_Name.LANGUAGE]="en"

        for section in bs_c.find_all("section", class_="section"):
            if section.find("strong").get_text() == "Information":
                string = section.find("div").get_text().strip()
                info[Row_Name.COPYRIGHT_STATEMENT] = string
                re_s = re.search("[0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3}", string)
                if re_s != None:
                    info[Row_Name.COPYRIGHT_YEAR] = string[re_s.span()[0]:re_s.span()[1]]
                if string.find("Mary Ann") != -1:
                    info[Row_Name.COPYRIGHT_HOLDER] = "Mary Ann Liebert, Inc"
                else:
                    info[Row_Name.COPYRIGHT_HOLDER]=string.replace("©","").replace("Copyright","").strip()



        an_string = ""
        em_string = ""
        af_string = ""
        co_string = ""
        ans = {}

        has_af = False
        has_em = False
        div_a = bs_c.find("div", class_="accordion-tabbed loa-accordion")
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
                    co_string += p
                elif p.find("E-mail Address:") != -1:
                    has_em = True
                    # print(p)
                    if em.find("$$") != -1:
                        em = p.split(":")[1].strip()
                    else:
                        em += ";" + p.split(":")[1].strip()
                    if p.find(em) == -1:
                        co_string += p
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

    def set_not_none_item(self,a_info,key,value):
        if value == None:
            raise ValueError(key+"的值为空！")
        a_info[key]=value

    def set_possible_none_item(self,a_info,key,value):
        if value!=None:
            a_info[key]=value.get_text().strip()



if __name__ == '__main__':
    cookie=" I2KBRCK=1; MAID=bTY2/0pIlThlENHcxBGyPQ==; _ga=GA1.2.2018801126.1543481100; gdprCookie=Cookies policy accepted; seerid=86715.61259763717; seerid=86715.61259763717; PathforaImpressions_95ee3ae4ffcc3bcb7ff6ee6329a77114=2%7C1553048980739; PathforaClosed_95ee3ae4ffcc3bcb7ff6ee6329a77114=2%7C1553048982823; __atuvc=40%7C9%2C11%7C10%2C4%7C11%2C5%7C12%2C3%7C13; __attag=%22lio%3Aly_unknown_email%2Clio%3Aly_frequent_user%2Clio%3Asmt_power%2Clio%3Aall%2Clio%3A95ee3ae4ffcc3bcb7ff6ee6329a77114_reach%2Clio%3Aaudhighlyengaged%2Clio%3Aaud_unknown_users%22%2Clio%3Aly_unknown_email%2Clio%3Aaud_unknown_users; _gid=GA1.2.1969530633.1553669761; SERVER=WZ6myaEXBLGexQVnui0xrg==; MACHINE_LAST_SEEN=2019-03-27T23%3A54%3A27.951-07%3A00; JSESSIONID=aaaT0kUlxcj7G7WTwxwMw; seerses=e; seerses=e; ly_segs=%7B%22ly_unknown_email%22%3A%22ly_unknown_email%22%2C%22ly_frequent_user%22%3A%22ly_frequent_user%22%2C%22smt_power%22%3A%22smt_power%22%2C%22all%22%3A%22all%22%2C%2295ee3ae4ffcc3bcb7ff6ee6329a77114_reach%22%3A%2295ee3ae4ffcc3bcb7ff6ee6329a77114_reach%22%2C%22audhighlyengaged%22%3A%22audhighlyengaged%22%2C%22aud_unknown_users%22%3A%22aud_unknown_users%22%7D; cookiePolicy=iaccept; _gat__gaenor=1; PathforaPageView=191"
    c={}
    for a in cookie.split(";"):
        a= a.split("=")
        c[a[0]]=a[1]

    print(c)



    pass
    # job=jobs()
    # job.run_single_website("MaryAnn")
    #
    # article_info={}
    # url="https://www.liebertpub.com/doi/10.1089/wound.2018.0824"
    #
    # data_s = requests.get(url)
    # bs_c = BeautifulSoup(data_s.text, "html.parser")
    # an_string = ""
    # em_string = ""
    # af_string = ""
    # co_string = ""
    # ans={}
    #
    # has_af = False
    # has_em = False
    # div_a = bs_c.find("div", class_="accordion-tabbed loa-accordion")
    # # print(div_a)
    # for div_tag in div_a.find_all("div", {"class": "accordion-tabbed__tab-mobile accordion__closed"}) \
    #                + div_a.find_all("div", {"class": "accordion-tabbed__tab-mobile"}):
    #     a = div_tag.find("a", href="#")
    #     if a["title"].strip() in ans:
    #         continue
    #     else:
    #         ans[a["title"].strip()]=1
    #     an_string += a["title"].strip() + "##"
    #     div_s = div_tag.find("div", class_="author-info accordion-tabbed__content")
    #     [s.extract() for s in div_s.find("div", class_="bottom-info")]
    #     af = ""
    #     aa = ""
    #     em = "$$"
    #     # print(div_tag)
    #     # print("================", a["title"].strip())
    #     for p in div_s.find_all("p"):
    #         print(p)
    #         [s.extract() for s in p.find_all("p")]
    #         p = p.get_text().strip().replace("\n", " ").replace("\r", " ")
    #
    #         if p.lower().find("correspondence") != -1:
    #             co_string += p
    #         elif p.find("E-mail Address:") != -1:
    #             has_em = True
    #             print(p)
    #             if em.find("$$") != -1:
    #                 em = p.split(":")[1].strip()
    #             else:
    #                 em += ";" + p.split(":")[1].strip()
    #             if p.find(em) == -1:
    #                 co_string += p
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
    # article_info[Row_Name.AUTHOR_NAME] = an_string[:-2]
    # if has_em:
    #     article_info[Row_Name.EMAIL] = em_string[:-2]
    # if has_af:
    #     article_info[Row_Name.AFFILIATION] = af_string[:-2]
    #
    # article_info[Row_Name.CORRESPONDING] = co_string
    # print(article_info)




