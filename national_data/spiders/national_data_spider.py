import json
import time
from urllib.parse import quote


from scrapy import Spider, Request
from national_data.getcode import get_leaf_code_list
from national_data.items import JDDataItem


class MySpider(Spider):

    name = "national_data"
    allowed_domains = ["data.stats.gov.cn"]


    def start_requests(self):

        """重写父类start_requests方法"""

        node_code_list = get_leaf_code_list()
        for node_code in node_code_list:
            yield self.condition_query(node_code)  # 必须yield一个Request对象

    def condition_query(self,node_code, period="1949-"):

        """树的叶节点code组装请求"""

        baseurl = "http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgjd&rowcode=zb&colcode=sj"
        dfwds = [{"wdcode": "zb", "valuecode": node_code}, {"wdcode": "sj", "valuecode": period}]
        k1 = int(round(time.time() * 1000)) #时间戳
        backurl = "&wds=[]&dfwds=" + str(dfwds) + "&k1=" + str(k1)
        url = baseurl + backurl.replace("[", quote("[")).replace("]", quote("]")).replace("{", quote("{")). \
            replace("}", quote("}")).replace(":", quote(":")).replace("'", quote('"')).replace(" ", "")
        print(url)
        return Request(url)


    def parse(self,response):

        """ 解析返回的json数据"""

        json_data = json.loads(response.body.decode("utf-8"))
        return_code = json_data.get("returncode")

        """如果获取数据成功，解析获取的数据"""
        if return_code == 200:
            return_data = json_data.get("returndata")
            data_list = return_data.get("datanodes")
            row_list = return_data.get("wdnodes")[0].get("nodes")
            year_len = len(return_data.get("wdnodes")[1].get("nodes"))

            item = JDDataItem()
            for i in range(len(row_list)):
                res_data_list = []
                for j in range(year_len):
                    res_data_list_item = {}
                    data = data_list[i * year_len + j]
                    has_data = bool(data.get("data").get("hasdata"))
                    if has_data is True:
                        res_data_list_item["name"] = row_list[i].get("cname")
                        res_data_list_item["time"] = data.get("code").split(".")[-1]
                        res_data_list_item["data"] = data.get("data").get("data")
                    if res_data_list_item:
                        res_data_list.append(res_data_list_item)
                if res_data_list:
                    item["item_name"] = row_list[i].get("cname")
                    item["item_code"] = row_list[i].get("code")
                    item["item_data"] = res_data_list
                    item["item_unit"] = row_list[i].get("unit")

                yield item





