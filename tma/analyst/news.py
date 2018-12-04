# coding: utf-8
import tma
from fuzzywuzzy import fuzz


def get_top_news(news, top=10):
    """返回最重要的 top 个新闻

    :param news: list of news
    :param top: int
    :return: top news
    """
    ranker = tma.TfidfDocRank(news, N=10)
    top_news = [x[1] for x in ranker.rank(top=top+30)]

    for i, new in enumerate(top_news):
        for j in range(i + 1, len(top_news)):
            distance = fuzz.ratio(new, top_news[j])
            if distance > 80:
                top_news[j] = 'drop'
    top_news = [new for new in top_news if new != "drop"]

    return top_news[:top]