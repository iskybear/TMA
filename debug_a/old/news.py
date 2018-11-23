from datetime import datetime, timedelta
from tma.collector.xhn import HomePage

from debug_a.utils import push2wx
from debug_a.config import conf


@push2wx(send_key=conf.bear_send_key, by='bear')
def xhn_headline():
    """获取新华网头条新闻"""
    hp = HomePage()
    title = "新华网 - 近两日热点新闻"

    delta = timedelta(days=1)
    today = datetime.now().date()
    last_day = today - delta
    d = [today.__str__(), last_day.__str__()]

    article_list = hp.get_article_list(d)

    content = "## [新华网](http://www.xinhuanet.com/)首页头条文章\n"
    template = "* [{date} | {title}]({url}) \n"

    for a in article_list:
        article = template.format(date=a[2], title=a[1], url=a[0])
        content += article
    return title, content


