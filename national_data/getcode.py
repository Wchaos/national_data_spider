import codecs

import os
from scrapy import Selector
from selenium import webdriver
import time


order_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H",
              "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
zhibiao_list = []

def get_page():
    """打开浏览器，把所有节点点开，保存网页为文件"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    url = 'http://data.stats.gov.cn/easyquery.htm?cn=B01'
    driver.get(url)
    time.sleep(2)
    but_close = driver.find_element_by_xpath("/html/body/div[2]/em")
    if but_close:
        but_close.click()
        print("已关闭浏览器提醒===========")

    """循环点开所有level节点"""
    start = 2
    for i in range(1, 5):
        node_list = driver.find_elements_by_xpath('//li[@class="level%d"]' % i)
        if node_list:
            end = start + len(node_list)
            for j in range(start, end):
                """找到当前level元素,点击"""
                print("treeZhiBiao_%d_span" % (j))
                driver.find_element_by_id("treeZhiBiao_%d_span" % (j)).click()
                time.sleep(2)
            start = end

    """保存page_source为文件"""
    content = driver.page_source
    with codecs.open('page_source.html', 'w+', 'utf-8') as f:
        f.write(content)
    driver.quit()


"""打开文件，解析出所有节点code"""

def parse(content, level, parent_code):
    selector = Selector(text=content)
    node_list = selector.xpath('//li[@class="level%d"]' % level).extract()
    for index, node_content in enumerate(node_list, 1):
        # print(level)
        zhibiao_dict = {}
        selector1 = Selector(text=node_content)
        # print(node_content)
        node_name = selector1.xpath('//a[@class = "level%d"]/span[2]/text()' % level).extract_first()
        zhibiao_dict["zhibiao"] = node_name

        code = "%s%s%s" % (parent_code, order_list[int(index / 36)], order_list[int(index % 36)])
        # print(code)
        zhibiao_dict["code"] = code
        next_level = level + 1
        child_node = selector1.xpath('//li[@class = "level%d"]' % next_level).extract()
        if child_node:
            zhibiao_dict["has_child"] = True
            parse(node_content, level=next_level, parent_code=code)
        else:
            zhibiao_dict["has_child"] = False

        zhibiao_list.append(zhibiao_dict)

def get_zhibiao_list():
    if not os.path.exists('./national_data/page_source.html'):
        get_page()
    with codecs.open('./national_data/page_source.html', 'r', 'utf-8') as f:
        content = f.read()
        parse(content, level=1, parent_code="A")
    # print(len(zhibiao_list))
    # print(zhibiao_list)
    return zhibiao_list

def get_leaf_code_list():
    zhibiao_list = get_zhibiao_list()
    code_list = []
    for zhibiao_dict in zhibiao_list:
        if not zhibiao_dict["has_child"]:
            code_list.append(zhibiao_dict["code"])
    # print(code_list)
    return code_list




