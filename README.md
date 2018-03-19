# national_data_spider


##介绍
- 本爬虫爬取的是国家统计局的的季度数据`http://data.stats.gov.cn/easyquery.htm?cn=B01`，略改一点可以改为爬月度和年度数据。

##爬取策略

- 直接爬取查询数据接口`http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgjd&rowcode=zb&colcode=sj&wds=%5B%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0101%22%7D%5D&k1=1521429745007`
- `url`中`wdcode`为查询条件名称，有指标（zb）和时间（sj）两种；`valuecode`为对查询条件对应的值
- 返回的是json数据，易于解析(其实下面点开节点已经查询了一遍数据了，但是页面解析没有这个方便。所幸数据量不大，对服务造成的请求压力不大)
- 查询条件中的，指标的值不能从页面获取，需要动态地根据树结构去算。
- 算叶节点code策略为：先用Selenium浏览器打开页面，自动单开所有节点（节点数据是动态获取刷新的，点开之后才能在page_source中找到），然后用xpath解析page_source，递归算出叶节点code


##环境

- 版本Python3(我用的Anaconda3)，安装对应Scrapy框架
- pip安装Selenium包，并下载chromedriver(谷歌浏览器驱动)放入开发环境（我直接Anaconda下），或者使用是指明路径
- 安装MongoDB数据库

