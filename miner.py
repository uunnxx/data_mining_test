import re
import sqlite3 as sql
import requests as rq
from bs4 import BeautifulSoup as bs


TANGORIN_URI = 'https://tangorin.com/vocabulary/65005'


def get_vocab_items():
    res = rq.get(TANGORIN_URI)
    data = bs(res.text, 'html.parser')
    uls = data.find('ul', class_="vocab-item-list")
    return uls.find_all('li', class_='vocab-item')


def vocab_pieces(vocab_items):
    for vocab_item in vocab_items:
        vocab_item = vocab_item.text
        if "【" in vocab_item:
            kanji, reading, translation = re.split(r"\W", vocab_item, maxsplit=2)
        elif "《" in vocab_item:
            reading, kanji, translation = re.split(r"\W", vocab_item, maxsplit=2)
        else:
            kanji, translation = re.split(r"\W", vocab_item, maxsplit=1)
            reading = ''

        translation = translation.lstrip()

        yield kanji, reading, translation


def main():
    vocab_items = get_vocab_items()

    with sql.connect("./static/dict.db") as sql_connection:
        cursor = sql_connection.cursor()
        cursor.execute("create table if not exists dict(id INTEGER PRIMARY KEY, k1 TEXT, reading TEXT, tr TEXT)")

        for vocab_piece in vocab_pieces(vocab_items):
            cursor.execute("insert into dict(k1, reading, tr) values(?, ?, ?)", vocab_piece)


if __name__ == '__main__':
    main()
