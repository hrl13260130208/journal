import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
from journal.common import Row_Name,common_website,common_journals,common_article
import logging



logger=logging.getLogger("logger")

def wait():
    # time.sleep(random.random() * 4+3)
    pass
class website(common_website):

    def get(self,section,url):

        wait()

        data=requests.get(url,verify=False)
        soup=BeautifulSoup(data.text,"html.parser")

        h1 = soup.find("h1")
        title = h1.get_text().replace("Open Access", " ").replace("\n", " ").strip()

        for a in soup.find_all("a"):
            if a.get_text().lower() == "archive":
                issn_url=a["href"]
                self.set_list(title, issn_url)



class journals(common_journals):

    def get(self,website,journal,url):
        infos=[]
        journal_common_info=self.get_common(journal,url)

        journal_common_info[Row_Name.JOURNAL_TITLE] = journal
        journal_common_info[Row_Name.PUBLISHER] = "OMICS International"
        wait()
        data = requests.get(url.strip())

        soup = BeautifulSoup(data.text, "html.parser")
        if "www.longdom.org" in url:
            ul=soup.find("ul",class_="list-group list-group-flush mb-3")
            if ul!=None:
                for div in ul.find_all("div", class_="card mb-3 rounded-0 border-0"):
                    year = div.find("h6").get_text().strip()
                    for a in div.find_all("a", class_="nav-link col-md-4 green-800-before"):
                        a_text = a.get_text()
                        if "Volume" in a_text:
                            issue_info = dict(journal_common_info)
                            vi = a_text.split(",")
                            volume = vi[0].replace("Volume", "").strip()
                            issue = vi[1].replace("Issue", "").strip()

                            issue_info[Row_Name.YEAR] = year
                            issue_info[Row_Name.VOLUME] = volume
                            issue_info[Row_Name.ISSUE] = issue
                            issue_info[Row_Name.TEMP_URL] = a["href"]
                            issue_info[Row_Name.TEMP_AURL]="1"

                            infos.append(issue_info)
                    for index,a in enumerate(div.find_all("a", class_="nav-link col-md-10 red-500-before")):
                        a_text = a.get_text()

                        issue_info = dict(journal_common_info)
                        issue_info[Row_Name.YEAR] = year
                        issue_info[Row_Name.VOLUME] = year
                        issue_info[Row_Name.ATTACH] = "Suppl."
                        issue_info[Row_Name.ISSUE_TITLE]=a_text
                        issue_info[Row_Name.TEMP_URL] = a["href"]
                        issue_info[Row_Name.TEMP_AURL]="1"
                        issue_info[Row_Name.ISSUE]="s"+str(index+1)
                        infos.append(issue_info)
        else:
            for div in soup.find_all("div", class_="card mb-3"):
                year = div.find("h6").get_text().strip()
                for a in div.find_all("a"):
                    a_text = a.get_text()
                    index=1
                    if "Volume" in a_text:
                        issue_info = dict(journal_common_info)
                        vi = a_text.split(",")
                        volume = vi[0].replace("Volume", "").strip()
                        issue = vi[1].replace("Issue", "").strip()

                        issue_info[Row_Name.YEAR]=year
                        issue_info[Row_Name.VOLUME]=volume
                        issue_info[Row_Name.ISSUE]=issue
                        issue_info[Row_Name.TEMP_URL]=a["href"]
                        # print(issue_info)
                        infos.append(issue_info)
                    elif  "Special Issue" in a_text:
                        issue_info = dict(journal_common_info)

                        issue_info[Row_Name.YEAR] = year
                        issue_info[Row_Name.VOLUME] = year
                        issue_info[Row_Name.ATTACH] = "Suppl."
                        issue_info[Row_Name.TEMP_URL] = a["href"]
                        issue_info[Row_Name.ISSUE] = "s" + str(index)
                        index+=1
                        issue_info[Row_Name.ISSUE_TITLE] = a.get_text().replace("Special Issue:", "").strip()
                        infos.append(issue_info)
        return infos

    def get_common(self,journal,url):
        info={}
        common=self.nm.get_journal_common_info(journal)

        if common ==None:
            wait()
            data = requests.get(url)
            soup = BeautifulSoup(data.text, "html.parser")
            if "www.longdom.org" in url:
                p = soup.find("p", class_="lead")
                if p!=None:
                    info[Row_Name.ISSN]=p.get_text().replace("ISSN:", "").strip()
                    return info
            div = soup.find("div", class_="issn")
            if div==None or div.get_text()=="" :
                return info
            try:
                issn = div.get_text().split(":")[1].strip()
                info[Row_Name.ISSN]=issn
            except:
                return info

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
        soup = BeautifulSoup(data.text, "html.parser")

        if Row_Name.TEMP_AURL in journal_temp:
            soup = BeautifulSoup(data.text, "html.parser")
            for div in soup.find_all("div", class_="mb-4"):

                article_info = dict(journal_temp)
                article_info[Row_Name.ABS_URL]=journal_temp[Row_Name.TEMP_URL]
                at = div.find("div", class_="d-flex w-100 justify-content-between border-bottom-1 mb-1")
                if at != None:
                    span = at.find("span")
                    if span != None:
                        pages = span.get_text().replace("Pages:", "").split("-")
                        try:
                            article_info[Row_Name.START_PAGE] = pages[0]
                            article_info[Row_Name.END_PAGE] = pages[1]
                            article_info[Row_Name.PAGE_TOTAL] = int(pages[1]) - int(pages[0]) + 1
                        except:
                            pass

                    span.extract()
                article_info[Row_Name.ARTICLE_TYPE] = at.get_text()
                h3 = div.find("h3")
                article_info[Row_Name.TITLE] = h3.get_text()
                try:
                    pdf_url = h3.find("a")["href"]
                    article_info[Row_Name.FULLTEXT_URL] = pdf_url
                    # pdf_path = self.download_pdf(pdf_url, "N-OMICS")
                    # if pdf_path != None:
                    #     article_info[Row_Name.FULLTEXT_PDF] = pdf_path.replace(self.DOWNLOAD_DIR, "")
                except:
                    pass
                for p in div.find_all("p", class_="mb-1 font-size-3 text-muted"):
                    text = p.get_text()
                    if "DOI" in text:
                        if p.find("a")!=None:
                            article_info[Row_Name.DOI] = p.find("a").get_text()
                        else:
                            article_info[Row_Name.DOI]=text.replace("DOI:","")
                    else:
                        article_info[Row_Name.AUTHOR_NAME] = text.replace(",", "##").replace(" and ", "##").strip()
                abs_url = div.find("a", {"title": "Abstract"})
                if abs_url != None:
                    article_info[Row_Name.ABS_URL] = abs_url["href"]
                    article_info[Row_Name.PAGEURL] = abs_url["href"]
                    data2 = requests.get(abs_url["href"])
                    # print(data.text)
                    soup2 = BeautifulSoup(data2.text, "html.parser")
                    abs = soup2.find("meta", {"name": "citation_abstract"})
                    if abs != None:
                        article_info[Row_Name.ABSTRACT] = abs["content"]
                    c_doi = soup2.find("meta", {"name": "citation_doi"})
                    if c_doi != None:
                        article_info[Row_Name.DOI] = c_doi["content"]

                article_info[Row_Name.TEMP_AURL]=None
                urls.append(article_info)
        else:
            for div in soup.find_all("div", class_="row current-issue text-left"):
                article_info = dict(journal_temp)
                article_type = div.find("font", class_="issue_type")
                a = div.find("strong").find("a")
                article_info[Row_Name.TEMP_AURL]=a["href"]
                article_info[Row_Name.ARTICLE_TYPE]=article_type.get_text().replace(":", "")
                urls.append(article_info)
        return urls

    def second(self,info,text,soup=None):
        article_info=info

        if article_info[Row_Name.TEMP_AURL]=="1":
            return article_info
        wait()
        # data_s = requests.get(article_info[Row_Name.TEMP_AURL])
        # bs_c = BeautifulSoup(data_s.text, "html.parser")
        bs_c=soup

        article_info[Row_Name.LANGUAGE] = "en"

        article_pdfurl = bs_c.find("meta", {"name": "citation_pdf_url"})
        if article_pdfurl != None:
            article_info[Row_Name.FULLTEXT_URL] = article_pdfurl["content"]
            # data_2 = requests.get(article_pdfurl["content"])
            # bs_2 = BeautifulSoup(data_2.text, "html.parser")
            # iframe=bs_2.find("iframe")
            # if iframe !=None:
            #     pdfurl=iframe["src"]
            # else:
            #     pdfurl=article_pdfurl["content"]
            # pdf_path = self.download_pdf(pdfurl, "N-OMICS")
            # if pdf_path != None:
            #     article_info[Row_Name.FULLTEXT_PDF] = pdf_path.replace(self.DOWNLOAD_DIR, "")


        aus = bs_c.find("dt")
        if aus != None:
            aff_dict = {}
            for aff in bs_c.find_all("dd"):
                sup = aff.find("sup")
                if sup == None:
                    if "0" in aff_dict:
                        aff_dict["0"] += ";" + aff.get_text()
                    else:
                        aff_dict["0"] = aff.get_text()
                else:
                    num = sup.get_text().strip()
                    sup.extract()
                    aff_dict[num] = aff.get_text()

            # print(aff_dict)

            email ={}
            try:
                div = bs_c.find("div", class_="mb-1")
                for a in div.find_all("a"):
                    if "email" in a.get_text():
                        email["*"] = a["title"]
            except:
                pass

            # print(email)
            article_authors = ""
            article_affs = ""
            emails = ""
            lines = aus.get_text()
            lines = clear_lines(lines)
            for line in lines.split(","):
                print(line)
                if " and " in line:
                    for au in line.split(" and "):
                        # print(au)
                        # print(pipe(au.strip(),aff_dict,"",email,"$$"))
                        au1, af, em = pipe(au, aff_dict, "", email, "$$")
                        if af == "" and "0" in aff_dict:
                            article_affs += aff_dict["0"] + "##"
                        else:
                            article_affs += af + "##"
                        article_authors += au1 + "##"
                        emails += em + "##"
                else:
                    au1, af, em = pipe(line, aff_dict, "", email, "$$")
                    if af == "" and "0" in aff_dict:
                        article_affs += aff_dict["0"] + "##"
                    else:
                        article_affs += af + "##"
                    article_authors += au1 + "##"
                    emails += em + "##"

            article_info[Row_Name.AUTHOR_NAME] = article_authors[:-2]
            article_info[Row_Name.AFFILIATION] = article_affs[:-2]
            if email!="":
                article_info[Row_Name.EMAIL] = emails[:-2]

        return article_info


def pipe(au,aff_dict,aff,email_dict,email):
    '''
    匹配作者机构
    :param au:
    :param aff_dict:
    :param aff:
    :param email_dict:
    :param email:
    :return:
    '''
    au=au.strip()
    key_set=set()
    for key in aff_dict.keys():
        key_set.add(key)
    for key in email_dict.keys():
        key_set.add(key)
    if au[-1] in key_set:
        if au[-1] in aff_dict:
            aff+= aff_dict[au[-1]] + ";"
            return pipe(au[:-1], aff_dict, aff, email_dict,email)
        elif au[-1] in email_dict:
            email=email_dict[au[-1]]+";"
            return pipe(au[:-1],aff_dict,aff,email_dict,email)
    elif au[-1].isalpha():
        if aff.__len__()>1 and aff[-1]==";":
            aff=aff[:-1]
        if email.__len__()>1 and email[-1]==";":
            email=email[:-1]
        return au,aff,email
    else:
        return pipe(au[:-1],aff_dict,aff,email_dict,email)

def clear_lines(line):
    tn = re.search("\d,\d", line)
    if tn != None:
        num = tn.start() + tn.group().index(",")
        # print(line[:num]+line[num+1:])
        return clear_lines(line[:num]+line[num+1:])
    else:
        return line

def pipe_author_email_aff(author_line,email_dict,aff_dict):
    author_line = author_line.strip()
    key_set = set()
    for key in aff_dict.keys():
        key_set.add(key.strip())
        aff_dict[key.strip()]=aff_dict[key]
    for key in email_dict.keys():
        key_set.add(key.strip())
        email_dict[key.strip()]=email_dict[key]

    author_dict=clear_authors(author_line,key_set)
    return get_author_email_aff(author_dict,email_dict,aff_dict)

def get_author_email_aff(author_dict,email_dict,aff_dict):
    print("++++++++",author_dict)
    authors=""
    emails=""
    affs=""
    has_aff=False
    has_email=False
    for key in author_dict.keys():
        find_email=False
        find_aff=False
        authors+=key+"##"
        for sup in author_dict[key]:
            if sup in email_dict:
                emails+=email_dict[sup]+";"
                find_email=True
                has_email=True
            if sup in aff_dict:
                affs+=aff_dict[sup]+";"
                find_aff=True
                has_aff=True
        if find_email:
            emails=emails[:-1]+"##"
        else:
            emails+="$$##"
        if find_aff:
            affs=affs[:-1]+"##"
        else:
            affs+="$$##"
    if not has_email:
        emails=""
    if not has_aff:
        affs=""
    return authors[:-2],emails[:-2],affs[:-2]

def clear_authors(author_line,key_set,split_char=","):
    author_line=author_line.replace(" and ",split_char)
    # and_num=author_line.find("and")
    # if and_num !=-1:
    #     author_line[and_num-1] in
    last_author=None
    author_dict={}
    for au in author_line.split(split_char):
        if au=="":
            continue
        if au in key_set:
            #拆出的是脚标
            if last_author==None:
                raise ValueError("解析出错！")
            else:
                if last_author in author_dict:
                    author_dict[last_author].append(au)
                else:
                    author_dict[last_author]=[au]
        else:
            #拆出的非脚标（可能是脚标的混合、作者、作者脚标混合）
            author_name,sup_list=split_author_sup(au,key_set,[])
            if author_name==None:
                if last_author == None:
                    raise ValueError("解析出错！")
            else:
                last_author=author_name

            if last_author in author_dict:
                author_dict[last_author].extend(sup_list)
            else:
                author_dict[last_author] = sup_list
    return author_dict



def split_author_sup(text,key_set,sup_list):
    num=get_sup(text,key_set,0)
    if num==0:
        for key in key_set:
            if key in text:
                raise ValueError("脚标位置有误或有未知的脚标！")
        return text,sup_list
    else:
        sup_list.append(text[-num:])
        if num==len(text):
            return None,sup_list
        else:
            return split_author_sup(text[:-num],key_set,sup_list)


def get_sup(text,key_set,num):
    new_num=num+1
    if text[-new_num:] in key_set:
        return get_sup(text,key_set,new_num)
    else:
        return num


if __name__ == '__main__':
    url = "https://www.longdom.org/archive/jnfs-volume-5-issue-3-year-2015.html"
    # url = "https://www.omicsonline.org/open-access/closedform-inverse-kinematic-solution-for-anthropomorphic-motion-in-redundant-robot-arms-2168-9695.1000110.php?aid=21589"
    data = requests.get(url)
    # print(data.text)
    soup = BeautifulSoup(data.text, "html.parser")
    for div in soup.find_all("div", class_="mb-4"):

        article_info = dict()

        at = div.find("div", class_="d-flex w-100 justify-content-between border-bottom-1 mb-1")
        if at != None:
            span = at.find("span")
            if span != None:
                pages = span.get_text().replace("Pages:", "").split("-")
                try:
                    article_info[Row_Name.START_PAGE] = pages[0]
                    article_info[Row_Name.END_PAGE] = pages[1]
                    article_info[Row_Name.PAGE_TOTAL] = int(pages[1]) - int(pages[0]) + 1
                except:
                    pass

            span.extract()
        article_info[Row_Name.ARTICLE_TYPE] = at.get_text()
        h3 = div.find("h3")
        article_info[Row_Name.TITLE] = h3.get_text()
        try:
            pdf_url = h3.find("a")["href"]
            article_info[Row_Name.FULLTEXT_URL] = pdf_url
            # pdf_path = self.download_pdf(pdf_url, "N-OMICS")
            # if pdf_path != None:
            #     article_info[Row_Name.FULLTEXT_PDF] = pdf_path.replace(self.DOWNLOAD_DIR, "")
        except:
            pass
        for p in div.find_all("p", class_="mb-1 font-size-3 text-muted"):
            text = p.get_text()
            if "DOI" in text:
                if p.find("a") != None:
                    article_info[Row_Name.DOI] = p.find("a").get_text()
                else:
                    article_info[Row_Name.DOI] = text.replace("DOI:", "")
            else:
                article_info[Row_Name.AUTHOR_NAME] = text.replace(",", "##").replace(" and ", "##").strip()
        abs_url=div.find("a",{"title":"Abstract"})
        if abs_url!=None:
            print(abs_url["href"])
            article_info[Row_Name.ABS_URL]=abs_url["href"]
            article_info[Row_Name.PAGEURL]=abs_url["href"]
            data2 = requests.get(abs_url["href"])
            # print(data.text)
            soup2 = BeautifulSoup(data2.text, "html.parser")
            abs=soup2.find("meta",{"name":"citation_abstract"})
            print(abs)
            if abs!=None:
                article_info[Row_Name.ABSTRACT]=abs["content"]
















