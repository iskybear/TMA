# coding: utf-8
import sys
sys.path.insert(0, r"C:\ZB\git_repo\zengbin93\TMA")

import tushare as ts
from fuzzywuzzy import fuzz
import tma

pro = ts.pro_api()


def get_news(start_date='2018-11-22 09:00:00', end_date='2018-11-22 12:00:00'):
    """
    如果是某一天的数据，可以输入日期 20181120 或者 2018-11-20，
    比如要想取2018年11月20日的新闻，可以设置start_date='20181120',
    end_date='20181121' （大于数据一天）

    如果是加时间参数，可以设置：start_date='2018-11-20 09:00:00',
    end_date='2018-11-20 22:05:03'
    """
    sources = ["sina", "wallstreetcn", "10jqka", "eastmoney", "yuncaijing"]

    news = []
    for src in sources:
        df = pro.news(src=src, start_date=start_date, end_date=end_date)
        for i, row in df.iterrows():
            new = row["title"].strip() + row["content"].strip()
            news.append(new)
    return news


def get_top_news(news, top=30):
    ranker = tma.TfidfDocRank(news, N=10)
    top_news = [x[1] for x in ranker.rank(top=top+30)]

    for i, new in enumerate(top_news):
        print(i)
        for j in range(i + 1, len(top_news)):
            distance = fuzz.ratio(new, top_news[j])
            if distance > 80:
                top_news[j] = 'drop'
    top_news = [new for new in top_news if new != "drop"]

    return top_news[:top]


if __name__ == '__main__':
    news = get_news()
