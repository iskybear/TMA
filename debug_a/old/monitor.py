from datetime import datetime
from tma.monitor.market import get_market_status
from tma.monitor.market import get_indices_status
from tma.monitor.single import get_shares_status
from tma.utils import run_at_trade_time

from debug_a.utils import push2wx
from debug_a.config import conf


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
