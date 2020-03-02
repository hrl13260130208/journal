import logging
from journal.redis_manager import name_manager

import json
import requests
import PyPDF2
import uuid
import os
import time
import re
import random
from bs4 import BeautifulSoup
import urllib3
from urllib3.exceptions import InsecureRequestWarning

#关闭安全请求警告
urllib3.disable_warnings(InsecureRequestWarning)

author_node_name = "au"
aff_node_name = "aff"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}


def wait():
    time.sleep(random.random() * 5 + 5)
    # pass

def get_html(url):
    time.sleep(random.random()*3+1)

    data = requests.get(url,headers=header,verify=False,timeout=60)
    # print(data.text)
    data.encoding = 'utf-8'
    datatext = data.text
    data.close()
    return datatext,data.url
logger=logging.getLogger("logger")
class common_website:
    def __init__(self):
        self.nm=name_manager()
        self.list=[]

    def get(self,section,url):
        '''
        从所给的url中爬取所有的期刊，要求爬取期刊名称和期刊内卷期列表的url

        :param section:
        :param url:
        :return:
        '''
        pass

    def run(self,section,url):
        '''
        执行get方法，并将list中的数据存到redis中

        当get方法出错时，退出程序
        :param section:
        :param url:
        :return:
        '''
        try:
            logger.info("解析url:"+url+"...")
            self.get(section,url)
            logger.info("解析完成！")
        except:
            logger.error("网站爬取出错！",exc_info = True)
            exit(0)

        for item in self.list:
            self.nm.seve_website_journal_set(section, json.dumps(item))

    def set_list(self,title,url):
        self.list.append((title,url))


class common_journals:
    def __init__(self):
        self.nm=name_manager()
        self.method = []

    def get(self,website,journal,url):
        '''
        需要子类实现
            实现内容：
                必需项：YEAR、VOLUME、ISSUE
                期刊层可以爬取的信息（）

        :param website:
        :param journal:
        :param url:
        :return:  要求是一个子元素是字典的list。例：[{'a':"d"},{'a':"d"}]

        '''
        pass

    def run(self,website,journal,url):

        '''
        执行get方法，将需要采集的期刊信息存储到redis中

        当get方法执行出错时，会执行method中配置的其他方法，当所有方法都执行失败的时候，会将错误信息存储到redis中

        :param website:
        :param journal:
        :param url:
        :return:
        '''

        try:
            logger.info("解析url:"+url)
            if not self.nm.is_discontinue_journal(url):
                wait()
                journals=self.get(website,journal,url.strip())
                for journal_info in journals:
                    if not isinstance(journal_info,dict):
                        raise ValueError("list中的item不是字典！")
                    if not Row_Name.JOURNAL_TITLE in journal_info:
                        raise ValueError("期刊标题为空！")
                    if not Row_Name.YEAR in journal_info:
                        raise ValueError("期刊年份为空！")
                    if not Row_Name.VOLUME in journal_info:
                        raise ValueError("volume为空！")
                    if not Row_Name.ISSUE in journal_info:
                        raise ValueError("issue为空！")

                    if self.nm.is_increment(journal, journal_info[Row_Name.YEAR],
                                            journal_info[Row_Name.VOLUME], journal_info[Row_Name.ISSUE]):
                        self.nm.save_journal_temp_data(journal, json.dumps(journal_info))
        except:
            logger.info("爬取"+journal+"失败!", exc_info=True)
            self.nm.save_journal_error_message(website+"_"+journal+"_"+url)



class common_article:
    DOWNLOAD_DIR = "D:/pdfs/"

    def __init__(self,website):
        self.nm = name_manager()
        self.website=website

    def run(self,journal):
        '''
        执行first与second方法，爬取文章的具体信息

         当get方法执行出错时，会执行method中配置的其他方法（方法名为journals中配置的方法名+_first(或_second)）
        :param journal:
        :param method_j:
        :return:
        '''
        while (True):
            temp_data = self.nm.get_journal_temp_data(journal)
            if temp_data == None:
                break
            journal_temp = json.loads(temp_data)
            self.do_run(journal_temp)



    def do_run(self,journal_temp):
        '''

        :param journal_temp:
        :return:
        '''
        infos = []
        len=-1
        try:
            m_first = getattr(self, "first")

            logger.info("爬取"+journal_temp[Row_Name.JOURNAL_TITLE]+"文章列表："+journal_temp[Row_Name.TEMP_URL])
            wait()
            infos = m_first(journal_temp)
        except:
            logger.error("爬取文章列表出错。错误信息：", exc_info=True)
            message = ["first", json.dumps(journal_temp)]
            self.nm.save_article_error_message(json.dumps(message))

        for info in infos:
            try:
                if not Row_Name.TEMP_AURL in info or info[Row_Name.TEMP_AURL]==None:
                    ainfo=info
                else:
                    logger.info("爬取"+journal_temp[Row_Name.JOURNAL_TITLE]+"具体文章："+info[Row_Name.TEMP_AURL])
                    wait()
                    ainfo = self.get_article(info)
                self.nm.save_article_data(self.website, json.dumps(ainfo))
                self.nm.save_download_article_data(ainfo[Row_Name.JOURNAL_TITLE],ainfo[Row_Name.VOLUME],ainfo[Row_Name.ISSUE],json.dumps(ainfo))
            except:
                logger.error("爬取文章出错：" + info[Row_Name.TEMP_AURL] + " 。错误信息：", exc_info=True)
                message = ["second", json.dumps(info)]
                self.nm.save_article_error_message(json.dumps(message))
                continue
        self.nm.save_download_schedule(journal_temp[Row_Name.JOURNAL_TITLE], journal_temp[Row_Name.VOLUME],
                                               journal_temp[Row_Name.ISSUE])

    def get_article(self,info):
        if Row_Name.TEMP_AURL in info.keys():


            data = requests.get(info[Row_Name.TEMP_AURL],headers=header,verify=False)
            bs_c = BeautifulSoup(data.text, "html.parser")
            info=self.head_parser(info,bs_c,data)
            try:
                info=self.second(info,data.text,soup=bs_c)
            except:
                logger.error("second方法执行出错！", exc_info=True)
        else:
            try:
                info = self.second(info, None, soup=None)
            except:
                logger.error("second方法执行出错！", exc_info=True)



        return self.split_items(info)

    def head_parser(self,info,bs_c,data):

        # 解析article_type
        if not Row_Name.ARTICLE_TYPE in info.keys():
            article_type = bs_c.find("meta", {"name": "dc.Type"})
            if article_type != None:
                info[Row_Name.ARTICLE_TYPE] = article_type["content"]

        # 解析doi
        if not Row_Name.DOI in info.keys():
            article_doi = bs_c.find("meta", {"scheme": "doi"})
            if article_doi != None:
                info[Row_Name.DOI] = article_doi["content"]

            article_doi = bs_c.find("meta", {"name": "citation_doi"})
            if article_doi != None:
                info[Row_Name.DOI] = article_doi["content"]

        # 解析title
        if not Row_Name.TITLE in info.keys():
            article_title = bs_c.find("meta", {"name": "dc.Title"})
            if article_title != None:
                info[Row_Name.TITLE] = article_title["content"]

            article_title = bs_c.find("meta", {"name": "citation_title"})
            if article_title != None:
                info[Row_Name.TITLE] = article_title["content"]

        # 解析abs
        if not Row_Name.ABSTRACT in info.keys():
            article_abs = bs_c.find("meta", {"name": "citation_abstract"})
            if article_abs != None:
                info[Row_Name.ABSTRACT] = article_abs["content"]

            description = bs_c.find("meta", {"name": "description"})
            if description != None:
                info[Row_Name.ABSTRACT] = description["content"]

            description = bs_c.find("meta", {"property": "og:description"})
            if description != None:
                info[Row_Name.ABSTRACT] = description["content"]

        # 解析keyword
        if not Row_Name.KEYWORD in info.keys():
            article_keyword = bs_c.find("meta", {"name": "keywords"})
            if article_keyword != None:
                info[Row_Name.KEYWORD] = article_keyword["content"].replace(",", "##").replace(";", "##")

            article_keyword = bs_c.find("meta", {"name": "citation_keywords"})
            if article_keyword != None:
                info[Row_Name.KEYWORD] = article_keyword["content"].replace(",", "##").replace(";", "##")

        # 解析pub_date
        if not Row_Name.STRING_PUB_DATE in info.keys():
            pub_date = bs_c.find("meta", {"name": "prism.publicationDate"})
            if pub_date != None:
                info[Row_Name.STRING_PUB_DATE] = pub_date["content"]

            article_pdate = bs_c.find("meta", {"name": "citation_publication_date"})
            if article_pdate != None:
                info[Row_Name.STRING_PUB_DATE] = article_pdate["content"]

        # 解析start_page
        if not Row_Name.START_PAGE in info.keys():
            article_fpage = bs_c.find("meta", {"name": "citation_firstpage"})
            if article_fpage != None:
                info[Row_Name.START_PAGE] = article_fpage["content"]

        # 解析end_page
        if not Row_Name.END_PAGE in info.keys():
            article_epage = bs_c.find("meta", {"name": "citation_lastpage"})
            if article_epage != None:
                info[Row_Name.END_PAGE] = article_epage["content"]

        # 解析copyright
        if not Row_Name.COPYRIGHT_STATEMENT in info.keys():
            article_copyright = bs_c.find("meta", {"name": "dc.copyright"})
            if article_copyright != None:
                info[Row_Name.COPYRIGHT_STATEMENT] = article_copyright["content"]

            article_copyright = bs_c.find("meta", {"name": "dc.Rights"})
            if article_copyright != None:
                info[Row_Name.COPYRIGHT_STATEMENT] = article_copyright["content"]

        # 解析作者及机构
        if not Row_Name.AUTHOR_NAME in info.keys():
            author = None
            aff = None
            try:
                author, aff = self.get_author_and_aff_from_head(bs_c)
            except:
                pass

            if author != None:
                info[Row_Name.AUTHOR_NAME] = author
            if aff != None:
                info[Row_Name.AFFILIATION] = aff

        # 解析pdf_url
        if not Row_Name.FULLTEXT_URL in info.keys():
            article_pdfurl = bs_c.find("meta", {"name": "citation_pdf_url"})
            if article_pdfurl != None:
                info[Row_Name.FULLTEXT_URL] = article_pdfurl["content"]

        info[Row_Name.ABS_URL] = data.url
        info[Row_Name.PAGEURL] = data.url

        return info

    def split_items(self,info):

        # 计算总页码
        if Row_Name.START_PAGE in info and Row_Name.END_PAGE in info:
            info[Row_Name.PAGE_TOTAL] = self.get_page_total(info[Row_Name.START_PAGE], info[Row_Name.END_PAGE])
        # elif not Row_Name.START_PAGE in info and  not Row_Name.END_PAGE in  info:
        #     pass
        # else:
        #     info[Row_Name.PAGE_TOTAL]=1

        # 拆分copyright
        if Row_Name.COPYRIGHT_STATEMENT in info:
            year, header_string = self.clean_copyright(info[Row_Name.COPYRIGHT_STATEMENT])
            info[Row_Name.COPYRIGHT_YEAR] = year
            info[Row_Name.COPYRIGHT_HOLDER] = header_string

        return info


    def first(self,temp_data):
        '''

        :param temp_data:
        :return:
        '''
        pass

    def second(self,info,text,soup=None):
        '''

        :param article_info:
        :return:
        '''
        pass



    def get_author_and_aff_from_head(self,soup, node=None, author=None, aff=None,
                                     author_tag_name="citation_author",
                                     aff_tag_name="citation_author_institution", last_node=None):

        '''

        从网页head中提取作者机构
            要求：作者机构同时有

        例：
            有HTML标签如下：
            <meta name="citation_author" content="Mohammad Kazem Moslemi">
            <meta name="citation_author_institution" content="Department of Urology, Kamkar Hospital, School of Medicine, Qom University of Medical Sciences, Qom, Iran">
            <meta name="citation_author" content="Mohammad Soleimani">
            <meta name="citation_author_institution" content="Eye Research Center, Department of Ophthalmology, Tehran University of Medical Sciences, Tehran, Iran">
            <meta name="citation_author" content="Hamid Reza Faiz">
            <meta name="citation_author_institution" content="Eye Research Center, Department of Ophthalmology, Tehran University of Medical Sciences, Tehran, Iran">
            <meta name="citation_author" content="Poupak Rahimzadeh">
            <meta name="citation_author_institution" content="Department of Anesthesiology, Iran University of Medical Sciences, Tehran, Iran">
            <meta name="citation_title" content="Cortical blindness after complicated general anesthesia in urological surgery">

            提取结果为：('Mohammad Kazem Moslemi##Mohammad Soleimani##Hamid Reza Faiz##Poupak Rahimzadeh',
                        'Department of Urology, Kamkar Hospital, School of Medicine, Qom University of Medical Sciences, Qom, Iran##Eye Research Center, Department of Ophthalmology, Tehran University of Medical Sciences, Tehran, Iran##Eye Research Center, Department of Ophthalmology, Tehran University of Medical Sciences, Tehran, Iran##Department of Anesthesiology, Iran University of Medical Sciences, Tehran, Iran')


        :param soup:  整个网页的BeautifulSoup对象
        :param node:  递归用参数：表示当前标签
        :param author: 递归用参数：表示提取的作者
        :param aff: 递归用参数：表示提取的机构
        :param author_tag_name: 作者标签的名称
        :param aff_tag_name: 机构标签的名称
        :param last_node:
        :return:
        '''

        if author == None:
            author = ""
        if aff == None:
            aff = ""

        if node == None:
            node = soup.find("meta", {"name": author_tag_name})
            aff_node = soup.find("meta", {"name": aff_tag_name})
            if node == None or aff_node == None:
                logger.debug("作者或机构为空！")
                return None, None
            author = node["content"] + "##"
            last_node = author_node_name

        next = node.next_sibling

        if "\n" == next:
            return self.get_author_and_aff_from_head(soup, node=next, author=author, aff=aff,
                                                author_tag_name=author_tag_name,
                                                aff_tag_name=aff_tag_name, last_node=last_node)
        if next.name != "meta":
            return self.clear_head_author_aff(author, aff)
        if not "name" in next.attrs.keys():
            return  self.clear_head_author_aff(author, aff)

        if next["name"] == aff_tag_name:
            aff += next["content"] + ";"
            last_node = aff_node_name
            return  self.get_author_and_aff_from_head(soup, node=next, author=author, aff=aff,
                                                author_tag_name=author_tag_name,
                                                aff_tag_name=aff_tag_name, last_node=last_node)
        elif next["name"] == author_tag_name:

            if last_node == author_node_name:
                author += next["content"] + "##"
                aff = aff[:-1] + "##$$##"
            else:
                author += next["content"] + "##"
                aff = aff[:-1] + "##"
            last_node = author_node_name
            return  self.get_author_and_aff_from_head(soup, node=next, author=author, aff=aff,
                                                author_tag_name=author_tag_name,
                                                aff_tag_name=aff_tag_name, last_node=last_node)
        else:
            return  self.clear_head_author_aff(author, aff)

    def clear_head_author_aff(self,author, aff):
        if author == "":
            logger.info("作者有误！")
            return None, None
        else:
            author = author[:-2]
            if aff[-1] == ";":
                aff = aff[:-1]
            elif aff[-1] == "#":
                aff = aff[:-1] + "$$"
            else:
                raise ValueError("机构末尾字符有误！")
            aus = author.split("##")
            affs = aff.split("##")
            # print(len(aus), author)
            # print(len(affs), aff)
            if len(aus) != len(affs):
                raise ValueError("作者机构匹配有误！")
            return author, aff

    def clean_copyright(self,line):
        line=line.replace("©","").strip()
        year = re.search("\d{4}",line)
        cr=re.search("copyright",line.lower())

        if cr !=None:
            print(line[cr.start():cr.end()])
            print(line)
            line=line.replace(line[cr.start():cr.end()],"").strip()
            print(line)
        if year != None:
            return  year.group(),line.replace(year.group(), "")
        else:
            return None,line

    def get_page_total(self,start,end):
        try:
            if isinstance(start,int):
                num_0=start
            else:
                num_0 = int(re.search("\d+", start).group())
            if isinstance(end,int):
                num_1=end
            else:
                num_1 = int(re.search("\d+", end).group())
            return num_1-num_0+1
        except:
            logger.error("页码出错！")
            return ""


    def pipe(self,au, aff_dict, aff, email_dict, email):
        '''
        根据传入的作者来匹配其邮箱与机构
        :param au:  作者名与脚标的组合 例：Hessam Khodabandehlo1*
        :param aff_dict: 存储所有机构的字典 格式：key=脚标，value=机构名
        :param aff:
        :param email_dict: 存储邮箱的字典 格式：key=脚标，value=邮箱
        :param email:
        :return:
        '''
        au = au.strip()
        if au[-1] in aff_dict:
            aff += aff_dict[au[-1]] + ";"
            return self.pipe(au[:-1], aff_dict, aff, email_dict, email)
        elif au[-1] in email_dict:
            email = email_dict[au[-1]] + ";"
            return self.pipe(au[:-1], aff_dict, aff, email_dict, email)
        else:
            return au, aff[:-1], email[:-1]

    def clear_lines(self,line):
        '''
        清洗作者数字脚标之间的","
        :param line:
        :return:
        '''
        tn = re.search("\d,\d", line)
        if tn != None:
            num = tn.start() + tn.group().index(",")
            # print(line[:num]+line[num+1:])
            return self.clear_lines(line[:num] + line[num + 1:])
        else:
            return line

    def get_author_email_aff(self,author_dict, email_dict, aff_dict):
        '''
        传入作者、邮箱、地址的字典，返回匹配好的字符串
        :param author_dict:  作者名--key  脚标（list）--value
        :param email_dict: 脚标--key  邮箱--value
        :param aff_dict: 脚标--key 地址--value
        :return:
        '''
        authors = ""
        emails = ""
        affs = ""
        has_aff = False
        has_email = False
        for key in author_dict.keys():
            find_email = False
            find_aff = False
            authors += key + "##"

            if len(author_dict[key])==0:
                if Row_Name.NO_SUP_KEY in email_dict:
                    emails += email_dict[Row_Name.NO_SUP_KEY] + ";"
                    find_email = True
                    has_email = True
                elif Row_Name.NO_SUP_KEY in aff_dict:
                    affs += aff_dict[Row_Name.NO_SUP_KEY] + ";"
                    find_aff = True
                    has_aff = True
                else:
                    pass
            else:
                for sup in author_dict[key]:
                    if sup in email_dict:
                        emails += email_dict[sup] + ";"
                        find_email = True
                        has_email = True
                    elif sup in aff_dict:
                        affs += aff_dict[sup] + ";"
                        find_aff = True
                        has_aff = True
                    else:
                        pass
            if find_email:
                emails = emails[:-1] + "##"
            else:
                emails += "$$##"
            if find_aff:
                affs = affs[:-1] + "##"
            else:
                affs += "$$##"
        if not has_email:
            emails = ""
        if not has_aff:
            affs = ""
        # print(authors[:-2], emails[:-2], affs[:-2])
        return authors[:-2], emails[:-2], affs[:-2]

    def clear_authors(self,author_line, key_set, split_char=","):
        """
        清洗作者
            传入一行包含多个作者及其脚标的字符串
            返回一个字典（key：作者名 value：脚标（list））

        主要针对英语，其他语言可能出问题
        :param author_line:
        :param key_set:
        :param split_char:
        :return:
        """
        author_line = author_line.replace(" and", split_char).replace("\u200b","")
        # and_num=author_line.find("and")
        # if and_num !=-1:
        #     author_line[and_num-1] in
        last_author = None
        author_dict = {}
        for au in author_line.split(split_char):
            au=au.strip()
            if au == "":
                continue

            if au in key_set or len(au)==1:
                # 拆出的是脚标
                if last_author == None:
                    raise ValueError("解析出错！")
                else:
                    if last_author in author_dict:
                        author_dict[last_author].append(au)
                    else:
                        author_dict[last_author] = [au]
            else:
                # 拆出的非脚标（可能是脚标的混合、作者、作者脚标混合）
                author_name, sup_list = self.split_author_sup(au, key_set, [])
                if author_name == None:
                    if last_author == None:
                        raise ValueError("解析出错！")
                else:
                    last_author = author_name

                if last_author in author_dict:
                    author_dict[last_author].extend(sup_list)
                else:
                    author_dict[last_author] = sup_list
        return author_dict



    def split_author_sup(self,text, key_set, sup_list,auto_split=True,check_last=True):
        '''
        抽取作者名字中的脚标


        :param text:
        :param key_set:
        :param sup_list:
        :param auto_split:
        :return:
        '''

        num = self.get_sup(text, key_set, 0)
        if num == 0:
            #在text最后没有脚标
            min=-1
            for key in key_set:
                if key in text:
                    if auto_split:
                        # 在text存在脚标，但不在text最后，提取所有脚标，并舍弃脚标后的文字
                        key_num=text.find(key)
                        if min!=-1:
                            if key_num<min:
                                min=key_num
                        else:
                            min=key_num
                        sup_list.append(key)

                    else:
                        raise ValueError("脚标位置有误或有未知的脚标！")
            if min!=-1:
                text=text[:min]

            if check_last:
                #检查text最后是否是*等非字母
                # print("-------------",text)
                text=self.find_last(text)
                # print(text)
                if text==None:
                    raise ValueError("作者名为空！")

            return text, sup_list
        else:
            #找到脚标text[-num:]
            sup_list.append(text[-num:])
            if num == len(text):
                #整个text都是脚标
                return None, sup_list
            else:
                #继续判断text中是否还有脚标
                return self.split_author_sup(text[:-num], key_set, sup_list)

    def find_last(self, text, index=-1):
        '''
        检查最后一位是否是字母
        :param text:
        :param index:
        :return:
        '''
        if index == len(text):
            return None
        if index == -1:
            index = 1
        # print(text,index)
        if text[-index].isalpha():
            if index==1:
                return text
            else:
                return text[:-(index-1)]
        else:
            return self.find_last(text, index + 1)

    def find_first(self, text, index=0):
        '''
        检查第一位是否是字母
        :param text:
        :param index:
        :return: 非字母与字母
        '''

        # print(text,index)
        if text[index].isalpha():
            if index==0:
                return None,text
            else:
                return text[:index],text[index:]
        else:
            return self.find_first(text, index + 1)

    def get_sup(self,text, key_set, num):
        '''

        判断最后一位或多位的数是否在key_set中
        例如：
            key_set中有1,11   --两个脚标
            text为name111    --该name有两个脚标1和11但没有分割符

            get_sup方法返回数字2，表示text的后两位是一个脚标

        :param text:
        :param key_set:
        :param num:
        :return:
        '''

        if num==len(text):
            return num
        new_num = num + 1
        text=text.strip()


        if text[-new_num:] in key_set :
            return self.get_sup(text, key_set, new_num)
        else:
            return num

    def download_html(self,url,*dir_name):
        logger.info("下载HTML,下载链接："+url)
        if dir_name:
            file_path = self.creat_filename(dir_name[0],"txt")
        else:
            date_time = time.strftime("%Y%m%d", time.localtime())
            file_path = self.creat_filename(date_time,"txt")
        try:
            self.download(url, file_path)
        except:
            logger.error("HTML下载出错。")
            try:
                os.remove(file_path)
            except:
                pass
            return None
        return file_path

    def download_pdf(self,url,dir_name="test",post=False,post_data=None,check_pdf=True):
        '''
        下载PDF，若下载的PDF出错则返回None
        :param url:
        :param dir_name: PDF文件夹名称
        :return:
        '''
        logger.info("下载PDF,下载链接："+url)
        wait()
        file_path=self.creat_filename(dir_name)

        try:
            if post:
                self.download(url,file_path,post,post_data)
            else:
                self.download(url,file_path)
            pdffile = open(file_path, "rb+")
            if check_pdf:
                self.checkpdf(pdffile)
            pdffile.close()
        except:
            logger.error("PDF下载出错。")
            pdffile.close()
            os.remove(file_path)
            return None
        return file_path.replace(self.DOWNLOAD_DIR,"")

    def creat_filename(self,dir_name,*subfix):
        if not os.path.exists(self.DOWNLOAD_DIR):
            os.mkdir(self.DOWNLOAD_DIR)
        if not os.path.exists(self.DOWNLOAD_DIR+dir_name):
            os.mkdir(self.DOWNLOAD_DIR+dir_name)

        uid=str(uuid.uuid1())
        suid=''.join(uid.split('-'))
        if subfix:
            return self.DOWNLOAD_DIR+dir_name+"/"+suid+"."+subfix[0]
        else:
            return self.DOWNLOAD_DIR+dir_name+"/"+suid+".pdf"

    def download(self,url, file,post=False,post_data=None):

        if post:
            data=requests.post(url.strip(),data=post_data,verify=False,timeout=30)
        else:
            data = requests.get(url.strip(),headers=header, verify=False,timeout=30)
        # print(data.text)
        data.encoding = 'utf-8'
        file = open(file, "wb+")
        file.write(data.content)
        file.close()

    def checkpdf(self,file):
        pdf = PyPDF2.PdfFileReader(file,strict=False)
        pages=pdf.getNumPages()
        return pages



class Row_Name:
    NO_SUP_KEY="0"
    FILENAME = "filename"
    EXCELNAME = "excelname"
    SERIAL_NUMBER = "serial_number"
    EDITOR = "editor"
    ERROR_REPORT = "error_report"
    PUBLISHER = "publisher"
    ISSN = "issn"
    EISSN = "eissn"
    JOURNAL_TITLE = "journal_title"
    ORIGINALJID = "originaljid"
    JID = "jid"
    YEAR = "year"
    VOLUME = "volume"
    ISSUE = "issue"
    ATTACH = "attach"
    ISSUE_TOTAL = "issue_total"
    ISSUE_TITLE = "issue_title"
    STRING_COVER_DATE = "string_cover_date"
    ISSUE_HISTORY = "issue_history"
    ARTICLE_ID = "article_id"
    DOI = "doi"
    ARTICLE_SEQ = "article_seq"
    ELOCATION_ID = "elocation_id"
    ARTICLE_TYPE = "article_type"
    TITLE = "title"
    SUBTITLE = "subtitle"
    TRANS_TITLE = "trans_title"
    TRANS_SUBTITLE = "trans_subtitle"
    LANGUAGE = "language"
    LANGUAGE_ALTERNATIVES = "language_alternatives"
    ABSTRACT = "abstract"
    TRANS_ABSTRACT = "trans_abstract"
    KEYWORD = "keyword"
    TRANS_KEYWORD = "trans_keyword"
    KEYWORD_ALTERNATIVES = "keyword_alternatives"
    SUBJECT = "subject"
    CLASSIFICATION = "classification"
    START_PAGE = "start_page"
    END_PAGE = "end_page"
    PAGE_TOTAL = "page_total"
    RANGE_PAGE = "range_page"
    STRING_PUB_DATE = "string_pub_date"
    RECEIVED_DATE = "received_date"
    REVISED_DATE = "revised_date"
    ACCEPTED_DATE = "accepted_date"
    ONLINE_DATE = "online_date"
    COPYRIGHT_STATEMENT = "copyright_statement"
    COPYRIGHT_YEAR = "copyright_year"
    COPYRIGHT_HOLDER = "copyright_holder"
    LICENSE = "license"
    REFERENCE = "reference"
    ABS_URL = "abs_url"
    PAGEURL = "pageurl"
    FULLTEXT_URL = "fulltext_url"
    FULLTEXT_PDF = "fulltext_pdf"
    CORRESPONDING = "corresponding"
    ARTICLE_NOTE = "article_note"
    AWARDS = "awards"
    AUTHOR_NAME = "author_name"
    NAME_ALTERNATIVES = "name_alternatives"
    COLLAB = "collab"
    EMAIL = "email"
    AFFILIATION = "affiliation"
    AFF_ALTERNATIVES = "aff_alternatives"
    AFF_ADDRESS = "aff_address"
    CONTRIB_ADDRESS = "contrib_address"
    BIO = "bio"
    TEMP_URL="temp_url"
    TEMP_AURL="temp_aurl"
    COLUME_NUM={"filename":0,
                "excelname":1,
                "serial_number":2,
                "editor":3,
                "error_report":4,
                "publisher":5,
                "issn":6,
                "eissn":7,
                "journal_title":8,
                "originaljid":9,
                "jid":10,
                "year":11,
                "volume":12,
                "issue":13,
                "attach":14,
                "issue_total":15,
                "issue_title":16,
                "string_cover_date":17,
                "issue_history":18,
                "article_id":19,
                "doi":20,
                "article_seq":21,
                "elocation_id":22,
                "article_type":23,
                "title":24,
                "subtitle":25,
                "trans_title":26,
                "trans_subtitle":27,
                "language":28,
                "language_alternatives":29,
                "abstract":30,
                "trans_abstract":31,
                "keyword":32,
                "trans_keyword":33,
                "keyword_alternatives":34,
                "subject":35,
                "classification":36,
                "start_page":37,
                "end_page":38,
                "page_total":39,
                "range_page":40,
                "string_pub_date":41,
                "received_date":42,
                "revised_date":43,
                "accepted_date":44,
                "online_date":45,
                "copyright_statement":46,
                "copyright_year":47,
                "copyright_holder":48,
                "license":49,
                "reference":50,
                "abs_url":51,
                "pageurl":52,
                "fulltext_url":53,
                "fulltext_pdf":54,
                "corresponding":55,
                "article_note":56,
                "awards":57,
                "author_name":58,
                "name_alternatives":59,
                "collab":60,
                "email":61,
                "affiliation":62,
                "aff_alternatives":63,
                "aff_address":64,
                "contrib_address":65,
                "bio":66
                }


if __name__ == '__main__':
    url="https://www.omicsonline.org/open-access/pectinaseultrasound-synergistic-extraction-of-chlorogenic-acid-fromflos-lonicera-japonicae-2155-9821-1000333.pdf"
    # url="https://www.omicsonline.org/open-access-pdfs/pectinaseultrasound-synergistic-extraction-of-chlorogenic-acid-fromflos-lonicera-japonicae-2155-9821-1000333.pdf"
    file="c:/File/sdf.pdf"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    data = requests.get(url.strip(), headers=header, verify=False, timeout=30)
    # print(data.text)
    data.encoding = 'utf-8'
    file = open(file, "wb+")
    file.write(data.content)
    file.close()







        




