from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from zb import create_logger
import time

from debug_a.old.news import xhn_headline
from debug_a.old.news import spider_xhn_home
from debug_a.old.monitor import market_status_inform


logger = create_logger(name='debug_a', log_file='debug_a.log', cmd=True)


def main():
    scheduler = BackgroundScheduler()

    # 数据采集任务
    scheduler.add_job(func=spider_xhn_home, trigger="cron",
                      hour='23', minute='30', day='*')

    # 消息推送任务
    scheduler.add_job(func=xhn_headline, trigger="cron",
                      hour='8', minute='30', day='*',
                      next_run_time=datetime.now())
    scheduler.add_job(func=market_status_inform, trigger="cron",
                      hour='9,10,11,13,14', minute='*/30',
                      day_of_week='mon-fri',
                      next_run_time=datetime.now())

    scheduler.start()
    try:
        while 1:
            time.sleep(100000)
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == "__main__":
    main()
