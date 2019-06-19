import re
import requests
from bs4 import BeautifulSoup
import csv
import calendar
import time
import random


def getUrls(start, end, tatalpage, startpage=1):
    """
        日期格式为"YY-MM-DD" 如 getUrl('2018-04-01','2018-04-30',1)
    """
    url = (
        "http://srh.bankofchina.com/search/whpj/search.jsp?"
        "erectDate={erectDate}&nothing={nothing}&pjname=1316&page=1").format(
            erectDate=start, nothing=end)
    urls = [url[:-1] + str(i) for i in range(startpage, tatalpage + 1)]
    return urls


def getTable(url):
    html = requests.get(url)
    # 'body > div > div.BOC_main.publish > div.pb_ft.clearfix > div.turn_page'
    soup = BeautifulSoup(html.text, 'lxml')
    raw_price = soup.select(
        'body > div > div.BOC_main.publish > table > tr > td')[:-1]
    raw_price = [i.text for i in raw_price]
    rows = [raw_price[i:i + 7] for i in range(0, len(raw_price), 7)]
    return rows


def saveContents(rows, filepath):
    """保存数据为csv格式"""

    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(rows)):
            writer.writerow(rows[i])
    print("-----------Save successfully.")


if __name__ == "__main__":
    filepath = "./data/rate_data/2018_M07-M12_rate.csv"
    # with open(filepath, 'a', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     firstrow = [
    #         '货币名称', '现汇买入价', '现钞买入价', '现汇卖出价', '现钞卖出价', '中行折算价', '发布时间'
    #     ]
    #     writer.writerow(firstrow)

    start = "2018-07-01"
    end = "2018-12-31"
    totalpage = 1373
    urls = getUrls(start, end, totalpage, startpage=5)
    j = 0
    for url in urls:
        rows = getTable(url)
        print("——————url:", url)
        time.sleep(random.uniform(1, 2))
        j = j + 1
        saveContents(rows, filepath)
        if (j % 10 == 0): time.sleep(random.uniform(3, 5))
    print(
        "____________________________________finish!____________________________________"
    )
