# coding=UTF-8
# -------------------讀網頁內容外加篩選網頁class，抓取特定內容，並存入檔案中--------------------------
import pymysql
import urllib.request
from bs4 import BeautifulSoup
import os

HOST = os.environ['DB_HOST']
PORT = int(os.environ['DB_PORT'])
USER = os.environ['DB_USER']
PASSWARD = os.environ['DB_PASSWARD']
DATABASE = os.environ['DB_DATABASE']
try:
    conn = pymysql.connect(host=HOST, port=PORT, user=USER,
                           passwd=PASSWARD, db=DATABASE, charset='utf8mb4')
    curr = conn.cursor()
    print('開始連接資料庫')
except:
    print('資料庫連接失敗')
    raise

url = "http://www.smeacommercialdistrict.tw/location/street"

response = urllib.request.urlopen(url)
data = response.read()
text = data.decode('utf-8-sig')

soup = BeautifulSoup(text, "lxml")  # parse

# 第一種 html_div = soup.body.section.div.div.div.div.div
# 第一種 city_name = html_div.find_all(
# 第一種     'h3', attrs={'class': 'county_title'})
# 第一種 table_content = html_div.find_all(
# 第一種     'table', attrs={'class': 'table table-striped table-bordered table-sm contactus_table'})

# 第二種 html_div = soup.select('div.col-12')
# 第二種 city_name = html_div[0].find_all(
# 第二種     'h3', attrs={'class': 'county_title'})
# 第二種 table_content = html_div[0].find_all(
# 第二種     'table', attrs={'class': 'table table-striped table-bordered table-sm contactus_table'})

# find vs select 前面只會找第一個 (find_all = select)

html_div = soup.find('div',class_="col-12")
# city_name =soup.select('h3.county_title') # 一直用soup去找 速度會部會慢?
# table_content =soup.select('table.table table-striped table-bordered table-sm contactus_table') # 一直用soup去找 速度會部會慢?
# county_form =soup.select("#county_form")

city_name = html_div.find_all(
    'h3', attrs={'class': 'county_title'})

table_content = html_div.find_all(
    'table', attrs={'class': 'table table-striped table-bordered table-sm contactus_table'})

# range(len(xxx)) vs enumerate(xxx) 前者不可傳val 後者可傳 
for index in range(len(city_name)):
    table_tbody_tr = table_content[index].select(
        'tbody > tr')
    for index2, val2 in enumerate(table_tbody_tr):
        curr.execute("""INSERT IGNORE INTO `businessDistrict` 
			(`id`, `city`, `businessName`,`region`, `businessArea`)
			 VALUES (%s,%s,%s,%s,%s)""",
                     (table_tbody_tr[index2].contents[1].contents[0], city_name[index].contents[0], table_tbody_tr[index2].contents[3].contents[0], table_tbody_tr[index2].contents[5].contents[0], table_tbody_tr[index2].contents[7].contents[0]))
        conn.commit()  # 確認送出(必要)
curr.close()        
conn.close()
