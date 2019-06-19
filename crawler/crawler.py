import datetime
import re
import time
from urllib import request
import pymysql

from bs4 import BeautifulSoup

error_url_list = []  # 待处理的出错url
unhandled_error_url = []  # 无法处理的url
error_record = []  # 插入失败的数据


def get_save_data_with_date(start_time, end_time):
    url = get_url(start_time, end_time)
    page_num = get_page_num(url) + 1
    for n in range(1, page_num):
        try:
            print(start_time + "To" + end_time + ":")
            real_url = url + "&page=" + str(n)
            data = get_table(url, n)
            insert_data(data)

        except Exception:
            print("\t" + "Fail to crawl/save " + "Page:" + str(n) +
                  "，retry at last")
            time.sleep(5)
            error_url_list.append(real_url)

    print("handle error url:")
    for url in error_url_list:
        print("\t" + url)
    print()
    handle_error()
    print("Unable to handle:")
    for tp in unhandled_error_url:
        for s in tp:
            print("\tURL: " + s[0])
            print("\tReason: " + s[1])
    print("Unable to insert into database:")
    for dt in error_record:
        print(dt)


def get_save_data_with_year(start_year, end_year):
    """ 获取并保存数据 """

    date_list = get_date_list(start_year, end_year)
    raw = len(date_list)
    for raw in range(0, raw):
        start_time = date_list[raw][0]
        end_time = date_list[raw][1]
        url = get_url(start_time, end_time)

        page_num = get_page_num(url) + 1
        for n in range(1, page_num):
            try:
                print(start_time + "To" + end_time + ":")
                real_url = url + "&page=" + str(n)
                data = get_table(url, n)
                insert_data(data)

            except Exception:
                print("\t" + "Fail to crawl/save " + "Page:" + str(n) +
                      "，retry at last")
                time.sleep(5)
                error_url_list.append(real_url)

    print("handle error url:")
    for url in error_url_list:
        print("\t" + url)
    print()
    handle_error()
    print("Unable to handle:")
    for tp in unhandled_error_url:
        for s in tp:
            print("\tURL: " + s[0])
            print("\tReason: " + s[1])
    print("Unable to insert into database:")
    for dt in error_record:
        print(dt)


def handle_error():
    """处理出错URL"""
    new_list = []
    for url in error_url_list:
        if url not in new_list:
            new_list.append(url)

    for url in new_list:
        try:
            pattern1 = r"(\d{4}-\d{1,2}-\d{1,2})"
            dates = re.compile(pattern1).findall(url)
            start_time = dates[0]
            end_time = dates[1]
            pattern2 = "page=([0-9]{1,})"
            m = re.compile(pattern2).findall(url)
            n = m[0]
            print(start_time + "To" + end_time + ":")
            data = get_table(url, n)
            insert_data(data)

        except Exception as e:
            print("\t" + "Fail to crawl ")
            time.sleep(5)
            temp_list = []
            temp_list.append(url)
            temp_list.append(e)
            unhandled_error_url.append(temp_list)


def insert_data(rows):
    """
        将返回的表格数据插入数据库
    """
    mysql_host = 'localhost'
    mysql_db = 'database'
    mysql_user = 'root'
    mysql_password = ''
    mysql_port = 3306
    connect = pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        password=mysql_password,
        db=mysql_db,
        charset='utf8')
    cursor = connect.cursor()

    s_count = 0
    f_count = 0
    sql = "INSERT INTO price_data (date, kind, price, market) VALUES ('%s', '%s', %.1f ,'%s')"
    for row in rows:
        try:
            data = (row[0], row[1], float(row[2]), row[3])
            cursor.execute(sql % data)
            connect.commit()
            s_count += 1
            # print('\t'+'1 reord is successfully inserted')
        except:
            error_record.append(data)
            f_count += 1
            print('\t' + 'Fail to insert 1 record ')
    print('\t' + str(s_count) + ' records have been successfully inserted.')
    print('\t' + ' Fail to insert ' + str(f_count) + ' records.')
    connect.close()


def get_table(url, page):
    """读取表格 返回列表list"""

    # 模拟浏览器
    headers = (
        'User-Agent',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    )
    opener = request.build_opener()
    opener.addheaders = [headers]

    # 爬取网页数据
    url = url + "&page=" + str(page)
    html = opener.open(url, timeout=5)
    soup = BeautifulSoup(html, "html.parser")
    list = []

    trs = soup.find_all('tr')
    del trs[0]
    for tr in trs:
        r = []
        tds = tr.find_all('td')
        for td in tds:
            r.append(td.text)
        r[3] = r[3][1:-1]
        r[2] = re.findall(r'-?\d+\.?\d*e?-?\d*?', r[2])  # 提取浮点数
        r[2] = float(r[2][0])
        del r[4]
        list.append(r)
    print("\t" + "Page:" + str(page) + " has been successfully crawled.")
    return list


def get_url(startTime, endTime):
    """返回从startTime至endTime的价格信息，日期格式为"year-month-day"（字符串型） 注意：日期间隔不得超过三个月"""

    if type(startTime) != str or type(endTime) != str:
        raise Exception("请输入str型")
    url = "http://nc.mofcom.gov.cn/channel/jghq2017/price_list.shtml?par_craft_index=13075&craft_index=20413" \
          "&par_p_index=&p_index=&startTime=" + \
          str(startTime) + "&endTime=" + str(endTime)
    return url


def get_date_list(start_year, end_year):
    """获得start_year至end_year列表 参数：start_year < end_year """

    dateList = []
    ori_list = [["-01-01", "-03-31"], ["-04-01", "-06-30"],
                ["-07-01", "-09-30"], ["-10-01", "-12-31"]]

    cur = datetime.datetime.now()
    cur_year = cur.year
    cur_month = cur.month

    if (cur_year == end_year):
        # 获得end_year 日期列表
        pattern = r"(\d{4}-\d{1,2}-\d{1,2})"
        date = re.compile(pattern).findall(str(cur))
        cur_date = date[0]
        cur_year = str(cur_year)
        if (cur_month >= 1 and cur_month <= 3):
            temp_list = [cur_year + ori_list[0][0], cur_date]
            dateList.append(temp_list)
        elif (cur_month >= 4 and cur_month <= 6):
            temp_list = [[
                cur_year + ori_list[0][0], cur_year + ori_list[0][1]
            ], [cur_year + ori_list[1][0], cur_date]]
            dateList += temp_list
        elif (cur_month >= 7 and cur_month <= 9):
            temp_list = [[
                cur_year + ori_list[0][0], cur_year + ori_list[0][1]
            ], [cur_year + ori_list[1][0], cur_year + ori_list[1][1]],
                         [cur_year + ori_list[2][0], cur_date]]
            dateList += temp_list
        else:
            temp_list = [[
                cur_year + ori_list[0][0], cur_year + ori_list[0][1]
            ], [cur_year + ori_list[1][0], cur_year + ori_list[1][1]], [
                cur_year + ori_list[2][0], cur_year + ori_list[2][1]
            ], [cur_year + ori_list[3][0], cur_date]]
            dateList += temp_list

    # 获得star_year到end_year日期列表
    for year in range(start_year, end_year):
        for i in range(0, 4):
            elem1 = str(year) + ori_list[i][0]
            elem2 = str(year) + ori_list[i][1]
            list = [elem1, elem2]
            dateList.append(list)

    return dateList


def get_page_num(url):
    # 模拟浏览器
    headers = (
        'User-Agent',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    )
    opener = request.build_opener()
    opener.addheaders = [headers]

    # 爬取网页数据
    url = url + "&page=" + str(1)
    html = opener.open(url)
    soup = BeautifulSoup(html, "html.parser")
    # 获取页数
    scripts = soup.find_all('script')
    script = str(scripts[-1])
    pattern = r"var v_PageCount = ([0-9]{1,})"
    page = re.compile(pattern).findall(script)
    page = int(page[0])
    return page


if __name__ == '__main__':
    # get_save_data_with_year(2014,2018)
    get_save_data_with_date("2018-07-17", "2018-07-20")
    print("________________end________________")
