
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time


def test():
    driver = webdriver.PhantomJS(executable_path=r'C:\File\soft\phantomjs\bin\phantomjs.exe')
    driver.set_window_size(1920, 1080)
    driver.get("https://www.bilibili.com")
    print(driver.title)

    element = WebDriverWait(driver, 10)
    print(driver.find_elements_by_class_name("rank-list hot-list"))

    # html = driver.execute_script("return document.documentElement.outerHTML")
    # html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    # print(html)
    # text=driver.page_source
    # print(driver.page_source)
    # soup=BeautifulSoup(text,"html.parser")
    # for ul in soup.find_all("ul",class_="rank-list hot-list"):
    #     print(ul)


    driver.quit()

def test2():
    driver = webdriver.PhantomJS(executable_path=r'D:\File\Soft\program\phantomjs\bin\phantomjs.exe')
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()

def test3():
    driver = webdriver.Chrome()
    driver.get("https://www.bilibili.com")
    time.sleep(10)
    # text = driver.page_source
    # print(driver.page_source)
    # soup = BeautifulSoup(text, "html.parser")
    # for ul in soup.find_all("ul", class_="rank-list hot-list"):
    #     print(ul)

    driver.quit()


if __name__ == '__main__':
    # test2()
    # test3()
    test()