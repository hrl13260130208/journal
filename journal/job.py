from journal.redis_manager import name_manager
from journal import excel_rw
from configparser import ConfigParser
import threading
import json
import logging
from  journal.common import Row_Name
import random


logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger("logger")

class configs:
    def __init__(self,path="config.cfg"):
        self.path=path
        self.conf = ConfigParser()
        self.conf.read(self.path,encoding="utf-8")

    def read_sections(self):
       return  self.conf.sections()

    def read_items(self,section):
        return self.conf.items(section)



class spider(threading.Thread):
    def __init__(self,section,items,update):
        threading.Thread.__init__(self)
        self.section=section
        self.items=items
        self.nm=name_manager()
        self.update=update

    def run(self):
        # 遍历网站所有期刊
        journals=self.nm.smembers_wbsite_journal_set(self.section)
        logger.info(self.section+"已有期刊数量:"+str(journals.__len__()))
        if journals.__len__()==0 or self.update:
            logger.info("更新"+self.section+"期刊...")
            self.update_journals()
            journals = self.nm.smembers_wbsite_journal_set(self.section)

        logger.info("爬取期刊中的信息...")
        for string in journals:
            s=json.loads(string)
            pyfile = __import__("journal.website." + self.section, fromlist=True)
            self.run_journal(pyfile,self.section,s[0],s[1])
            self.run_article(pyfile,self.section,s[0])

    def update_journals(self):
        '''
        更新网站中的期刊（执行对应网站的python文件的website的run方法）
        :return:
        '''
        pyfile = __import__("journal.website." + self.section, fromlist=True)
        c = getattr(pyfile, "website")
        for item in self.items:
            args = item[1].split(";")
            m = getattr(c(), "run")
            for arg in args:
                m(self.section, arg)


    def run_journal(self,pyfile,website,journal,url):
        '''
        爬取期刊信息，使用反射执行对应网站的python文件的journals的run方法
        :param pyfile: python文件名
        :param website:
        :param journal:
        :param url:
        :return:
        '''
        logger.info("爬取 " + journal + " 期刊级别的信息...")
        c = getattr(pyfile, "journals")
        c_instance = c()
        m = getattr(c_instance, "run")
        m(website, journal,url)

    def run_article(self,pyfile,website,journal):
        '''
        爬取文章信息，使用反射执行对应网站的python文件的article的run方法
        :param pyfile:
        :param journal:
        :return:
        '''

        logger.info("爬取 " + journal+ " 文章级别的信息...")
        ca = getattr(pyfile, "article")
        ca_instance = ca(website)
        m = getattr(ca_instance, "run")
        m(journal)

    def test_website(self,pyfile,website,url):
        logger.info("测试 " +website + " 中的期刊...")
        c = getattr(pyfile, "website")
        ca=c()
        m = getattr(ca, "get")
        m(website,url)
        list=getattr(ca,"list")
        logger.info("爬取期刊如下：")
        for l in list:
            logger.info("期刊标题："+str(l[0])+"\t链接："+str(l[1])+"\t原始数据："+str(l))
        return list


    def test_journal(self,pyfile,website,journal,url):
        logger.info("测试 " + journal + " 期刊层的信息...")
        c = getattr(pyfile, "journals")
        c_instance = c()
        m = getattr(c_instance, "get")
        infos=m(website, journal,url)
        logger.info("爬取到的期刊层信息如下：")
        for info in infos:
            logger.info("年份：" + str(info[Row_Name.YEAR]) + "\tvolume：" + str(info[Row_Name.VOLUME]) + "\tissue：" + str(
                info[Row_Name.ISSUE]) + "\t链接：" + str(info[Row_Name.TEMP_URL]) + "\t原始数据：" + str(info))
        return infos

    def test_article(self,pyfile,website,journal_info):
        logger.info("爬取 " + journal_info[Row_Name.JOURNAL_TITLE] + " 文章级别的信息...")
        ca = getattr(pyfile, "article")
        ca_instance = ca(website)
        m1 = getattr(ca_instance, "first")
        infos=m1(journal_info)
        logger.info("爬取到的文章列表如下：")
        for info in infos:
            logger.info("链接：" + str(info[Row_Name.TEMP_AURL]) + "\t原始数据：" + str(info))
        logger.info("随机选取一篇文章进行下一步测试！")
        num=int(random.random()*len(infos))

        logger.info("选取文章如下：")
        logger.info("链接：" + str(infos[num][Row_Name.TEMP_AURL]) + "\t原始数据：" + str(infos[num]))

        m2=getattr(ca_instance,"get_article")

        article_info=m2(infos[num])
        logger.info("爬取到具体文章信息如下：")
        for key in article_info.keys():
            logger.info("key:"+str(key)+"\t value:"+str(article_info[key]))



class jobs:
    def __init__(self):
        self.cofig=configs()

    def run(self,update=False):
        '''
        爬取conf中配置的所有网站
        :return:
        '''
        thread=[]
        pubs={}
        # for section in self.cofig.read_sections():
        #     excel_rw.create_and_save_execel(section)
        logger.info("读取配置文件...")
        for section in self.cofig.read_sections():
            if section=="single":
                for item in self.cofig.read_items(section):
                    pubs=self.run_single_journal(item)
            else:
                if not section in pubs:
                    pubs[section]=1
                items=self.cofig.read_items(section)
                s=spider(section,items,update)
                thread.append(s)
                s.start()
        for t in thread:
            t.join()
        print("===============",pubs)
        write_data(pubs)

    def run_single_website(self, website):
        '''
        爬取指定网站
        :param website:
        :return:
        '''
        pubs = {}
        if website == "single":
            for item in self.cofig.read_items(website):
                pubs = self.run_single_journal(item)
        else:
            pubs[website] = 1
            items = self.cofig.read_items(website)
            # s = spider(website, items,False)
            s = spider(website, items,True)
            s.start()
            s.join()
        write_data(pubs)

    def run_journal_vol_issue(self,website):
        pass

    def run_single_journal(self,item):
        '''
        爬取指定的当期刊（在config中single里配置的项目）
        :param item:
        :return:
        '''
        pubs={}
        pyfile = __import__("journal.website." + item[0], fromlist=True)


        strs=item[1].split("_")
        if strs.__len__()>3:
            a=""
            for i in range(strs.__len__()-2):
                a+=strs[i+2]+"_"
            strs[2]=a[:-1]
        if not strs[0] in pubs:
            pubs[strs[0]]=1
        spi = spider(None, None, False)
        spi.run_journal(pyfile,strs[0],strs[1],strs[2])
        spi.run_article(pyfile,strs[0],strs[1])
        return pubs



    def single_journal(self,publisher,name):
        item=self.cofig.read_items("single")
        self.run_single_journal(item[0])
        write_data({publisher:1},name)


    def test_website(self,pyfile_name,website,url):
        pyfile = __import__("journal.website." +pyfile_name, fromlist=True)
        s=spider(None,None,False)
        web_list=s.test_website(pyfile,website,url)
        logger.info("随机选取一个期刊进行期刊层的测试！")
        num = int(random.random() * len(web_list))

        logger.info("选取期刊如下：")
        logger.info("期刊标题："+str(web_list[num][0])+" 链接："+str(web_list[num][1])+" 原始数据："+str(web_list[num]))

        journal_list=s.test_journal(pyfile,website,web_list[num][0],web_list[num][1])
        logger.info("随机选取一个卷期进行文章层的测试！")
        num = int(random.random() * len(journal_list))

        logger.info("选取卷期如下：")
        logger.info("年份：" + str(journal_list[num][Row_Name.YEAR]) + " volume：" + str(
            journal_list[num][Row_Name.VOLUME]) + " issue：" + str(
            journal_list[num][Row_Name.ISSUE]) + " 链接：" + str(journal_list[num][Row_Name.TEMP_URL]) + " 原始数据：" + str(
            journal_list[num]))

        s.test_article(pyfile,website,journal_list[num])

    def test_single(self):
        item = self.cofig.read_items("single")
        print(item)
        s = spider(None, None, False)
        args= item[0][1].split("_")
        pyfile = __import__("journal.website." + item[0][0], fromlist=True)


        journal_list = s.test_journal(pyfile, args[0], args[1], args[2])
        logger.info("随机选取一个卷期进行文章层的测试！")
        num = int(random.random() * len(journal_list))

        logger.info("选取卷期如下：")
        logger.info("年份：" + str(journal_list[num][Row_Name.YEAR]) + " volume：" + str(
            journal_list[num][Row_Name.VOLUME]) + " issue：" + str(
            journal_list[num][Row_Name.ISSUE]) + " 链接：" + str(journal_list[num][Row_Name.TEMP_URL]) + " 原始数据：" + str(
            journal_list[num]))

        s.test_article(pyfile, args[0],journal_list[num])





def write_data(pubs,*name):
    logger.info("创建并写入execl...")
    for pub_key in pubs.keys():
        if name.__len__() != 0:
            excel_rw.create_and_save_execel(pub_key,name[0])
        else:
            excel_rw.create_and_save_execel(pub_key)

    logger.info("生成日志...")
    excel_rw.write_logs()

    logger.info("任务完成。")


def run_article_error_test(file,url,pyname="s_fasebj"):
    '''
    重新执行出错的文章级别链接（测试）
    :param file:
    :param url:
    :return:
    '''
    file=open(file)
    for line in file.readlines():
        if line.find(url)!=-1:
            list=json.loads(line)
            dict = json.loads(list[1])
            # dict = list[1]
            if list[0] =="first":
                if dict[Row_Name.TEMP_URL] == url:
                    pyfile = __import__("journals.website." + pyname, fromlist=True)
                    ac=getattr(pyfile,"article")

                    do_run = getattr(ac(), "do_run")
                    print(do_run(json.loads(list[1])))
                    break
            elif list[0] =="second":
                if dict[Row_Name.TEMP_AURL] == url:
                    pyfile = __import__("journal.website." + pyname, fromlist=True)
                    ac = getattr(pyfile, "article")
                    m_second= getattr(ac(dict[Row_Name.PUBLISHER]), "second")
                    print(m_second(dict))
                    break
            elif list[0] =="second_back":
                if dict[Row_Name.TEMP_AURL] == url:
                    pyfile = __import__("journals.website." + pyname, fromlist=True)
                    ac = getattr(pyfile, "article")
                    m_second = getattr(ac(), "back")
                    print(m_second(dict))


def run_journal_error_test(file,url):
    '''
     重新执行出错的期刊级别链接（测试）
    :param file:
    :param url:
    :return:
    '''
    file = open(file)
    for line in file.readlines():
        if line.find(url) != -1:
            strs=line.split("_")
            pyfile = __import__("journals.website." + strs[0], fromlist=True)
            ac = getattr(pyfile, "journals")
            m_get=getattr(ac(),"get")
            print(m_get(strs[0],strs[1],strs[2]))
def run_journal(pyname,website,journal,url):
    j_spider = spider(None, None, False)
    pyfile = __import__("journals.website." + pyname, fromlist=True)
    j_spider.run_journal(pyfile, website, journal, url)
    j_spider.run_article(pyfile,website, journal)
    write_data({website:1},journal)

    # pyfile = __import__("journals.website." + strs[0], fromlist=True)
    # ac = getattr(pyfile, "journals")
    # m_get = getattr(ac(), "get")
    # print(m_get(strs[0], strs[1], strs[2]))



def run_journal_error(file):
    '''
    重新执行出错的期刊级别所有链接（运行）
    :param file:
    :return:
    '''
    file = open(file)
    j_spider=spider(None,None,False)
    pubs = {}
    for line in file.readlines():
        strs = line.split("_")
        if not strs[0] in pubs:
            pubs[strs[0]] = 1
        pyfile = __import__("journals.website." + strs[0], fromlist=True)
        j_spider.run_journal(pyfile,strs[0],strs[1],strs[2])
        j_spider.run_article(pyfile,strs[0],strs[1])

    write_data(pubs)

def run_article_error(file):
    '''
     重新执行出错的文章级别所有链接（运行）
    :param file:
    :return:
    '''
    file = open(file)
    errs={}
    pubs={}
    nm=name_manager()
    for line in file.readlines():
        # line_l=json.loads(line)
        # print(line_l)
        temp=json.loads(json.loads(line)[1])
        new_dict={}
        print(temp)
        if Row_Name.EISSN in temp:
            new_dict[Row_Name.EISSN]=temp[Row_Name.EISSN]
        if Row_Name.ISSN in temp:
            new_dict[Row_Name.ISSN]=temp[Row_Name.ISSN]
        new_dict[Row_Name.JOURNAL_TITLE]=temp[Row_Name.JOURNAL_TITLE]
        new_dict[Row_Name.PUBLISHER]=temp[Row_Name.PUBLISHER]
        new_dict[Row_Name.STRING_COVER_DATE]=temp[Row_Name.STRING_COVER_DATE]
        new_dict[Row_Name.YEAR]=temp[Row_Name.YEAR]
        new_dict[Row_Name.VOLUME]=temp[Row_Name.VOLUME]
        new_dict[Row_Name.ISSUE]=temp[Row_Name.ISSUE]
        new_dict[Row_Name.TEMP_URL]=temp[Row_Name.TEMP_URL]

        string=new_dict[Row_Name.JOURNAL_TITLE]+"_"+new_dict[Row_Name.VOLUME]+"_"+new_dict[Row_Name.ISSUE]

        if not string in errs:
            errs[string]=new_dict

    for key in errs.keys():
        pub=errs[key][Row_Name.PUBLISHER]
        if not pub in pubs:
            pubs[pub]=1
        pyfile = __import__("journals.website." + pub, fromlist=True)
        ac = getattr(pyfile, "article")
        m_get = getattr(ac(), "do_run")
        ais=m_get(errs[key])

        m_save=getattr(ac(),"save_data")
        m_save(ais,errs[key])

    write_data(pubs)



def set_discontinue_journal(url):
    '''
    存储不需要爬取期刊链接
    :param url:
    :return:
    '''
    name_manager().save_discontiune_journal(url)

if __name__ == '__main__':

    job=jobs()
    # job.test_website("MaryAnn","https://home.liebertpub.com/publications/by-type/journals-open-access/892/")
    # job.run_single_website("single")
    job.test_single()

    # run_article_error_test(r"C:\execl\20191015\article.txt","https://www.fasebj.org/doi/10.1096/fj.14-254037")





