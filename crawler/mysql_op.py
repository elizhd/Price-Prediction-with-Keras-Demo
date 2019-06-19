import pymysql
import csv
import os

error_record = []



def save_contents(list, filepath):
    """保存数据为csv格式"""

    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(list)):
            writer.writerow(list[i])
    print("\t\t" + "Save successfully.")
    
def read_csv(path):
    """读取并且返回返回csv文件内容 
        返回列表list[[row1], [row2], [row3]...]"""

    rows = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows.append(row)
    return rows


def insert_data(rows):
    """
        将readerCsv() 返回的数据插入数据库
    """
    mysql_host = 'localhost'
    mysql_db = 'database'
    mysql_user = 'root'
    mysql_password = ''
    mysql_port = 3306
    connect = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user,
                              password=mysql_password, db=mysql_db, charset='utf8')
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
            print('\t'+'Fail to insert 1 record ')
    print('\t' + str(s_count) + ' records are successfully inserted.')
    print('\t' + ' Fail to insert ' + str(f_count) + ' records.')
    connect.close()


if __name__ == '__main__':
    data_file_list = os.listdir('data/')
    for file in data_file_list:
        print('insert records from ' + file + '   ..............')
        path = 'data/' + file
        rows = read_csv(path)
        insert_data(rows)
    print('Fail to record : ')
    for error in error_record:
        print(error)
print("__________end___________")


