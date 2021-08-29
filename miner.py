import re
import sqlite3 as sql
import requests as rq
from bs4 import BeautifulSoup as bs

sql_connection = sql.connect("dict.db")
cursor = sql_connection.cursor()

cursor.execute("create table if not exists dict(id INTEGER PRIMARY KEY, k1 TEXT, reading TEXT, tr TEXT)")

res = rq.get("https://tangorin.com/vocabulary/65005")
data = bs(res.text, 'html.parser')

uls = data.find('ul', class_="vocab-item-list")
lis = uls.find_all('li', class_='vocab-item')



for i, li in enumerate(lis):
    # if i > 10:
    #     break

    li = li.text
    if "【" not in li:
        continue

    aa = re.split(r"\W", li, maxsplit=2)
    text = aa[2].lstrip()

    print("\n\n", aa[0])
    print(aa[1])
    print(text)


    cursor.execute("insert into dict(k1, reading, tr) values(?, ?, ?)", (aa[0], aa[1], text))


sql_connection.commit()
