from tma.analyst import WeekRank
from tma.indicator import ShareDayIndicator


class Config:
    end_day = "2018-07-27"


conf = Config()

# step 1. 统计上周股票不同区间涨跌幅股票数量

wr = WeekRank(conf.end_day, refresh=True)

# 计算周涨幅大于30个点的股票数量
wr.latest_mkls[wr.latest_mkls['change_rate'] > 0.10].shape

s = ShareDayIndicator('002501')
s.run(['ma', 'lnd'])
