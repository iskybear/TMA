# coding: utf-8
"""
A股相关信息推送任务
====================================================================
"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time

from tma.monitor.market import get_market_status
from tma.monitor.market import get_indices_status
from tma.monitor.market import get_top_plate
from tma.monitor.single import get_shares_status
from tma.utils import run_at_trade_time
from tma.sms import push2wx
from tma.analyst.news import get_top_news
from tma.collector.ts import get_news


class Config:
    server_chan_key = "SCU10748T12f471f07094648d297222fc649e374d598bf38bc81fd"
    bear_send_key = ""


conf = Config()


@push2wx(send_key=conf.server_chan_key, by='server_chan')
def after_close_report():
    title = "今日收盘报告 | %s" % datetime.now().__str__().split('.')[0]
    flow = get_top_plate()
    market = get_market_status()
    indices = get_indices_status()
    info = "\n".join((market, indices, flow))
    return title, info


@run_at_trade_time
@push2wx(send_key=conf.bear_send_key, by='bear')
def market_status_inform():
    """交易时间段内，市场状态和指数行情"""

    status = []
    # 构造播报信息 - 市场
    market_status = get_market_status()
    status.append(market_status)

    # 构造播报信息 - 指数
    indices_status = get_indices_status()
    status.append(indices_status)

    title = "市场状态播报 - %s" % datetime.now().__str__().split('.')[0]
    content = ''.join(status)

    return title, content


@run_at_trade_time
@push2wx(send_key=conf.server_chan_key, by='server_chan')
def shares_status_inform(codes):
    title = "个股行情播报 - %s" % datetime.now().__str__().split(".")[0]
    content = get_shares_status(codes)
    return title, content


@push2wx(send_key=conf.server_chan_key, by="server_chan")
def report_news():
    """推送快讯"""
    cur_t = datetime.now()
    title = "最近6小时最重要的20条快讯 | %s" % cur_t.__str__().split('.')[0]
    six_h = timedelta(hours=6)
    pre_t = cur_t - six_h

    news = get_news(start_date=pre_t.__str__(), end_date=cur_t.__str__())
    top_news = get_top_news(news, top=20)

    content = ""
    for i, new in enumerate(top_news, 1):
        c = "\n### **第%i条快讯**\n --- \n%s\n\n" % (i, new)
        content += c

    return title, content.strip()


def main():
    scheduler = BackgroundScheduler()

    # 收盘报告
    scheduler.add_job(func=after_close_report, trigger="cron",
                      hour='19', day_of_week='mon-fri',
                      next_run_time=datetime.now())

    # 交易时段的个股行情推送
    scheduler.add_job(func=shares_status_inform, trigger='cron',
                      hour='9,10,11,13,14,15', minute='*/30',
                      day_of_week='mon=fri')

    # 交易时段的市场状态推送
    scheduler.add_job(func=market_status_inform, trigger='cron',
                      hour='10,11,13,14', day_of_week='mon=fri')

    # 推送新闻快讯
    scheduler.add_job(func=report_news, trigger="cron", hour='2,8,14,20,',
                      minute='0', day='*', next_run_time=datetime.now())

    scheduler.start()
    try:
        while 1:
            time.sleep(100000)
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == '__main__':
    main()

