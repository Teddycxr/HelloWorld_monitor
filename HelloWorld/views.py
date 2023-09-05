import sys
sys.path.append('/usr/local/server')
import time
import threading
import traceback
import Toolbox as tb
import numpy as np
from django.shortcuts import render
# usdtSwap: 正向永续 coins: 全币种 coinSwap: 反向永续


class Params():

    """要用的参数

    Attributes:
        door (str): Description
        usdtSwapSymbols (list): Description
    """

    def __init__(self):
        self.door = 'http://marketmonitor.wbfevent.io/'
        self.usdtSwapSymbols = ['btcusdt', 'ethusdt', 'eosusdt',
                                'compusdt', 'atomusdt', 'xrpusdt',
                                'ltcusdt', 'bchusdt', 'bsvusdt',
                                'etcusdt', 'trxusdt', 'linkusdt',
                                'adausdt', 'mkrusdt', 'sushiusdt',
                                'uniusdt', 'filusdt', 'grtusdt',
                                '1inchusdt', 'dashusdt', 'dotusdt',
                                'aaveusdt', 'yfiusdt', 'dogeusdt',
                                'xmrusdt', 'avaxusdt', 'snxusdt',
                                'ksmusdt', 'zecusdt', 'zilusdt',
                                'wavesusdt', 'zenusdt', 'ontusdt',
                                'grayusdt', 'pregrayusdt', 'polkausdt',
                                'defiusdt', 'nftusdt', 'hecousdt',
                                'layer2usdt', 'tornusdt', 'mirusdt',
                                'maskusdt', 'xchusdt', 'shibusdt',
                                'icpusdt', 'csprusdt', 'bnb+htusdt',
                                'bnb-htusdt','chzusdt', 'dydxusdt',
                                'lunausdt', 'solusdt']
        self.comboSymbols = ['atomusdt']
        self.coinSwapSymbols = ['btcusd', 'ethusd', 'dotusd', 'uniusd', 'ltcusd', 'eosusd',
                                'xrpusd', 'trxusd', 'adausd', 'bchusd']
        self.coinsSymbols = [
            'btcusdt(lego)',
            'btcusdt(bobc)',
            #'ethusd(wt)',
            #'btcusd(gia)',
            #'ethusd(gia)',
            #'btcusd(zs)',
            #'btcusd(aib)',
            #'ethusd(aib)',
        ]
        self.etpSymbols = ['btc3usdt', 'btc03usdt', 'eth3usdt', 'eth03usdt', 'eos3usdt', 'eos03usdt',
                           'ada3usdt', 'ada03usdt', 'link3usdt', 'link03usdt', 'dot3usdt', 'dot03usdt',
                           'uni3usdt', 'uni03usdt', 'xrp3usdt', 'xrp03usdt',
                           'fil3usdt', 'fil03usdt', 'trx3usdt', 'trx03usdt',
                           'doge3usdt', 'doge03usdt', 'shib3usdt', 'shib03usdt']
        self.spotSymbols = ['btcusdt', 'ethusdt', 'dotusdt', 'ksmusdt',
                            'oceanusdt',
                            #'filusdt',
                            'ltcusdt',
                            'sushiusdt',
                            'bchusdt',
                            #'dogeusdt',
                            'maticusdt',
                            'crvusdt',
                            'xchusdt',
                            #'axsusdt',
                            'shibusdt',
                            'nftusdt',
                            'uniusdt',
                            'cruusdt',
                            ]
        # self.redbullSymbols = ['btcusdt', 'ethusdt', 'trxusdt', 'test21']
        self.coinStoreSymbols = [
            'btcusdt',
            'ethusdt',
            'trxusdt',
            'uniusdt',
            #'aaveusdt',
            #'linkusdt',
            'sushiusdt',
            #'zrxusdt',
            'dogeusdt',
            '1inchusdt',
            #'snxusdt',
            #'compusdt',
            'lrcusdt',
            #'mkrusdt',
            'grtusdt',
            #'oceanusdt',
            'manausdt',
            'rsrusdt',
            #'yfiusdt',
            'maticusdt',
            #'trbusdt',
            #'omgusdt',
            #'rlcusdt',
            'crvusdt',
            'apeusdt',
            'aliceusdt',
            #'sxpusdt',
            'chzusdt',
            #'akrousdt',
            #'dentusdt',
            #'bakeusdt',
            'sandusdt',
            'shibusdt',
            #'cakeusdt',
            'bicousdt',
            #'unfiusdt',
            #'reefusdt',
            #'dotusdt',
            #'renusdt',
            #'ksmusdt',
            #'chrusdt',
            #'srmusdt',
            'batusdt',
            'mtrmusdt',
            'akitausdt',
            'dogekingusdt',
        ]
        self.coinStoredepthSymbols = [
            'btcusdt',
            'ethusdt',
            'trxusdt',
            'uniusdt',
            # 'aaveusdt',
            # 'linkusdt',
            'sushiusdt',
            # 'zrxusdt',
            'dogeusdt',
            '1inchusdt',
            # 'snxusdt',
            # 'compusdt',
            'lrcusdt',
            # 'mkrusdt',
            'grtusdt',
            # 'oceanusdt',
            'manausdt',
            'rsrusdt',
            # 'yfiusdt',
            'maticusdt',
            # 'trbusdt',
            # 'omgusdt',
            # 'rlcusdt',
            'crvusdt',
            'apeusdt',
            'aliceusdt',
            # 'sxpusdt',
            'chzusdt',
            # 'akrousdt',
            # 'dentusdt',
            # 'bakeusdt',
            'sandusdt',
            'shibusdt',
            # 'cakeusdt',
            'bicousdt',
            # 'unfiusdt',
            # 'reefusdt',
            # 'dotusdt',
            # 'renusdt',
            # 'ksmusdt',
            # 'chrusdt',
            # 'srmusdt',
            'batusdt',
            'mtrmusdt',
            'akitausdt',
            'dogekingusdt',
        ]
        self.coinStoreUsdtSwapSymbols = [
            'btcusdt',
            'ethusdt',
            'dotusdt',
            'linkusdt',
            'dogeusdt',
            'xrpusdt',
            'icpusdt',
            'adausdt',
            'ltcusdt',
            'etcusdt',
            'filusdt',
            'axsusdt',
            'eosusdt',
            'maticusdt',
            'uniusdt',
            'trxusdt',
            'dydxusdt',
            'bchusdt',
            'lunausdt',
            'solusdt',
            'atomusdt',
            'celousdt',
            'avaxusdt',
            'ftmusdt',
            'thetausdt',
            'bnbusdt',
            'ksmusdt',
            'celrusdt',
            'hbarusdt',
            'sandusdt',
            'bicousdt',
            'racausdt',
            'peopleusdt',
        ]
        self.binanceUsdtSwapSymbols = [
            'btcusdt',
            'eosusdt',
            'uniusdt',
            'btcusd'
        ]
        self.arbitrageSymbols = [
            'usdt_arbitrage',
            'btc_arbitrage',
            'eth_arbitrage'
        ]
        self.depthSymbols = ['btc', 'eth']


paras = Params()
redis = tb.Redis()  # 配置redis
#redis2 = tb.Redis(host='18.178.124.254')  # 配置redis
redis2 = tb.Redis()
prefixDic = {
    'usdtSwap': 'wbfUsdtSwap',
    'combo': 'wbfUsdtSwap',
    'coinSwap': 'wbfCoinSwap',
    'coins': 'wbfCoins',
    'spot': 'wbfSpot',
    'etp': 'wbfSpotETP',
    'coinStore': 'coinStoreSpot',
    'coinStoredepth':'coinStoredepth'
}


def th_getData():   # 获取redis数据
    while 1:
        tables = [i for i in redis2.query() if 'table' in i]
        for table in tables:
            try:
                data = redis2.get(table)
                # print(data)
                setattr(paras, table, data)
            except:
                print(traceback.format_exc())
        time.sleep(30)


process = threading.Thread(target=th_getData)
process.start()


def portal(request):
    jump1 = [
        #f"<a href='{paras.door}usdtSwap/{paras.usdtSwapSymbols[0]}/'>正向永续合约</a>",
        f"<a href='{paras.door}coinStoreUsdtSwap/{paras.coinStoreUsdtSwapSymbols[0]}/'>coinStore正向永续</a>",
        #f"<a href='{paras.door}coinSwap/{paras.coinSwapSymbols[0]}/'>反向永续合约</a>",
        #f"<a href='{paras.door}spot/{paras.spotSymbols[0]}/'>现货</a>",
        #f"<a href='{paras.door}etp/{paras.etpSymbols[0]}/'>ETP</a>",
        f"<a href='{paras.door}coinStore/{paras.coinStoreSymbols[0]}/'>coinStore现货</a>",
        f"<a href='{paras.door}coins/{paras.coinsSymbols[0]}/'>全币种合约</a>",
    ]
    jump2 = [
        #f"<a href='{paras.door}hedgeAccount/'>套保账户</a>",
        f"<a href='{paras.door}depth/{paras.depthSymbols[0]}/'>流动性监控</a>",
        f"<a href='{paras.door}coinStoredepth/{paras.coinStoreSymbols[0]}/'>coinStore摆盘监控</a>",
        #f"<a href='{paras.door}fundingRate/'>各交易所资金费率监控</a>",
    ]
    jump3 = [
        # f"<a href='{paras.door}binanceUsdtSwap/{paras.binanceUsdtSwapSymbols[0]}/'>币安正向合约</a>",
        #f"<a href='{paras.door}arbitrage/{paras.arbitrageSymbols[0]}/'>套利</a>",
    ]

    content = {}
    content['jump1'] = jump1
    content['jump2'] = jump2
    content['jump3'] = jump3
    return render(request, 'portal.html', content)


def jump(prefix=None):
    if prefix is None:
        symbols = ['首页']
    else:
        symbols = ['首页']+getattr(paras, f'{prefix}Symbols')

    urls = [f'{paras.door}{prefix}/{symbol}/' if symbol != '首页'
            else paras.door
            for symbol in symbols]

    pls = np.full(len(symbols), np.nan)
    for i, symbol in enumerate(symbols):
        if i == 0:
            continue
        try:
            data = np.array(
                getattr(paras, f'{prefixDic.get(prefix, prefix)}_{symbol}_table'))
            data = data[:, 4]
            #print(data)
            pls[i] = np.nansum([float(i.split(':')[-1]) for i in data])
        except:
            #print(traceback.format_exc())
            continue
    pls[0] = np.nansum(pls[1:])
    urls = [[f"<a href='{url}'>{symbols[i]}\n\n{pls[i]:0.2f}</a>", pls[i]]
            for i, url in enumerate(urls)]
    return urls


def button(url, name):
    return f"<a href='{paras.door}{url}/'>{name}</a>"


def usdtSwap(request, symbol=paras.usdtSwapSymbols[0]):
    """正向永续合约

    Args:
        request (TYPE): Description
    """
    content = {}
    content['jump'] = jump('usdtSwap')
    # content['jump2'] = [button(f'usdtSwap/{symbol}/openOrders','策略挂单')]
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['content'] = redis2.get(f'wbfUsdtSwap_{symbol}_table')
        # for d in content['content']:
        #d[-1] = f"<a href='{paras.door}usdtSwap/{symbol}/{d[1]}/hisDeals'>{d[-1]}</a>"
        content['info'] = redis2.get(f'wbfUsdtSwap_{symbol}_info')
        # print(f'{symbol}_info')
        # print(content['info'])
    except:
        pass
    return render(request, 'monitorNew2.html', content)

def coinStoreUsdtSwap(request, symbol=paras.coinStoreUsdtSwapSymbols[0]):
    """正向永续合约

    Args:
        request (TYPE): Description
    """
    content = {}
    content['jump'] = jump('coinStoreUsdtSwap')
    # content['jump2'] = [button(f'usdtSwap/{symbol}/openOrders','策略挂单')]
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['content'] = redis2.get(f'coinStoreUsdtSwap_{symbol}_table')
        # for d in content['content']:
        #d[-1] = f"<a href='{paras.door}usdtSwap/{symbol}/{d[1]}/hisDeals'>{d[-1]}</a>"
        content['info'] = redis2.get(f'coinStoreUsdtSwap_{symbol}_info')
        # print(f'{symbol}_info')
        # print(content['info'])
    except:
        pass
    return render(request, 'monitorNew2.html', content)

def coins(request, symbol=paras.coinsSymbols[0]):
    """全币种

    Args:
        request (TYPE): Description
    """
    content = {}
    content['jump'] = jump('coins')
    # content['jump2'] = [button(f'coins/{symbol}/openOrders','策略挂单')]
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['content'] = redis2.get(f'coinStoreUsdtSwap_{symbol}_table')
        for d in content['content']:
            d[-1] = f"<a href='{paras.door}coins/{symbol}/{d[1]}/hisDeals'>{d[-1]}</a>"
        content['info'] = redis2.get(f'coinStoreUsdtSwap_{symbol}_info')
        # print(f'{symbol}_info')
        # print(content['info'])
    except:
        pass
    return render(request, 'monitorNew.html', content)


def coinSwap(request, symbol=paras.coinSwapSymbols[0]):
    """反向永续合约

    Args:
        request (TYPE): Description
    """
    content = {}
    content['jump'] = jump('coinSwap')
    # content['jump2'] = [button(f'coinSwap/{symbol}/openOrders','策略挂单')]
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['content'] = redis2.get(f'wbfCoinSwap_{symbol}_table')
        for d in content['content']:
            d[-1] = f"<a href='{paras.door}coinSwap/{symbol}/{d[1]}/hisDeals'>{d[-1]}</a>"
        content['info'] = redis2.get(f'wbfCoinSwap_{symbol}_info')
    except:
        pass
    return render(request, 'monitorNew.html', content)


def combo(request, symbol=paras.comboSymbols[0]):
    """反向永续合约

    Args:
        request (TYPE): Description
    """
    content = {}
    content['jump'] = jump('combo')
    # content['jump2'] = [button(f'combo/{symbol}/openOrders','策略挂单')]
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['content'] = redis2.get(f'wbfUsdtSwapV2_{symbol}_table')
        for d in content['content']:
            d[-1] = f"<a href='{paras.door}combo/{symbol}/{d[1]}/hisDeals'>{d[-1]}</a>"
        content['info'] = redis2.get(f'wbfUsdtSwapV2_{symbol}_info')
    except:
        pass
    return render(request, 'monitorNew.html', content)


def spot(request, symbol=paras.spotSymbols[0]):
    """现货

    Args:
        request (TYPE): Description
    """
    content = {}
    content['jump'] = jump('spot')
    # content['jump2'] = [button(f'spot/{symbol}/openOrders','策略挂单')]
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['content'] = redis2.get(f'wbfSpot_{symbol}_table')
        for d in content['content']:
            d[-1] = f"<a href='{paras.door}spot/{symbol}/{d[1]}/hisDeals'>{d[-1]}</a>"
        content['info'] = redis2.get(f'wbfSpot_{symbol}_info')
    except:
        pass
    return render(request, 'monitorNew.html', content)


def etp(request, symbol=paras.etpSymbols[0]):
    """现货

    Args:
        request (TYPE): Description
    """
    content = {}
    content['jump'] = jump('etp')
    # content['jump2'] = [button(f'etp/{symbol}/openOrders','策略挂单')]
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['content'] = redis2.get(f'wbfSpotETP_{symbol}_table')
        for d in content['content']:
            d[-1] = f"<a href='{paras.door}etp/{symbol}/{d[1]}/hisDeals'>{d[-1]}</a>"
        content['info'] = redis2.get(f'wbfSpotETP_{symbol}_info')
    except:
        pass
    return render(request, 'monitorNew.html', content)


def binanceUsdtSwap(request, symbol=paras.binanceUsdtSwapSymbols[0]):
    """现货

    Args:
        request (TYPE): Description
    """
    content = {}
    content['jump'] = jump('binanceUsdtSwap')
    # content['jump2'] = [button(f'binanceUsdtSwap/{symbol}/openOrders','策略挂单')]
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['content'] = redis2.get(f'binanceCoinSwap_{symbol}_table')
        for d in content['content']:
            d[-1] = f"<a href='{paras.door}binanceUsdtSwap/{symbol}/{d[1]}/hisDeals'>{d[-1]}</a>"
        content['info'] = redis2.get(f'binanceCoinSwap_{symbol}_info')
    except:
        pass
    return render(request, 'monitorNew.html', content)


def arbitrage(request, symbol=paras.arbitrageSymbols[0]):
    '''套利'''
    content = {}
    content['jump'] = jump('arbitrage')    
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['content'] = redis2.get(f'arbitrage_{symbol}_table')
        content['info'] = redis2.get(f'arbitrage_{symbol}_info')
    except:
        pass
    return render(request, 'arbitrage.html', content)

def coinStore(request, symbol=paras.coinStoreSymbols[0]):
    """图灵

    Args:
        request (TYPE): Description
    """
    content = {}
    content['jump'] = jump('coinStore')
    # content['jump2'] = [button(f'coinStore/{symbol}/openOrders','策略挂单')]
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['content'] = redis2.get(f'coinStoreSpot_{symbol}_table')
        for d in content['content']:
            d[-1] = f"<a href='{paras.door}coinStore/{symbol}/{d[1]}/hisDeals'>{d[-1]}</a>"
        content['info'] = redis2.get(f'coinStoreSpot_{symbol}_info')

        content['ordersdepth'] = redis2.get(f'coinStoreSpot_{symbol}_ordersdepth')
        #print(content['info'])
    except:
        pass
    return render(request, 'monitorNew.html', content)

def coinStoredepth(request, symbol=paras.coinStoreSymbols[0]):
    '''摆盘监控'''
    content = {}
    content['jump'] = jump('coinStoredepth')
    content['symbol'] = symbol.upper()
    content['test'] = 'n/a'
    try:
        content['ordersdepth'] = redis2.get(f'coinStoreSpot_{symbol}_ordersdepth')
        #print(content['ordersdepth'])
        content['info'] = redis2.get(f'coinStoreSpot_{symbol}_info')
    except:
        pass
    return render(request, 'monitor_depth.html', content)


def openOrders(request, kind='usdtSwap', symbol=paras.usdtSwapSymbols[0]):
    """当前挂单

    Args:
        request (TYPE): Description
        kind (str, optional): Description
        symbol (TYPE, optional): Description

    Returns:
        TYPE: Description
    """
    content = {}
    content['jump'] = [button(f'{kind}/{symbol}', '返回')]
    content['openBid'] = 'n/a'
    content['openAsk'] = 'n/a'
    content['closeBid'] = 'n/a'
    content['closeAsk'] = 'n/a'
    try:
        data = redis.get(f'{symbol}_openOrders')
        data = sorted(data.items(), key=lambda x: x[0], reverse=True)
        content['openBid'] = [[i[0], i[1][0], i[1][3]]
                              for i in data if (i[1][2] == 1 and i[1][1] == 1)]
        content['openAsk'] = [[i[0], i[1][0], i[1][3]]
                              for i in data if (i[1][2] == 1 and i[1][1] == -1)][::-1]
        content['closeBid'] = [[i[0], i[1][0], i[1][3]]
                               for i in data if (i[1][2] == 2 and i[1][1] == 1)]
        content['closeAsk'] = [[i[0], i[1][0], i[1][3]]
                               for i in data if (i[1][2] == 2 and i[1][1] == -1)][::-1]
    except:
        pass
    return render(request, 'openOrders.html', content)


def hisDeals(request, kind='usdtSwap', symbol=paras.usdtSwapSymbols[0], strategy='far1'):
    """成交明细

    Args:
        request (TYPE): Description
        kind (str, optional): Description
        symbol (TYPE, optional): Description
        strategy (str, optional): Description

    Returns:
        TYPE: Description
    """
    content = {}
    content['jump'] = [button(f'{kind}/{symbol}', '返回')]
    content['data'] = 'n/a'
    try:
        data = redis.get(f'{symbol}_{strategy}_hisDeals')
        data = np.frombuffer(data, 'U48')
        content['data'] = data.reshape(int(len(data)/11), 11)
    except:
        pass
    return render(request, 'hisDeals.html', content)


def hedgeAccount(request):
    """套保合约

    Args:
        request (TYPE): Description

    Returns:
        TYPE: Description
    """
    content = {}
    content['jump'] = jump()
    try:
        content['info'] = redis2.get('open_order_only_balance_array')
        content['content'] = redis2.get('open_order_only_result_array')
    except:
        pass
    return render(request, 'hedgeAccount.html', content)


def depth(request, symbol=paras.depthSymbols[0]):
    """流动性监控

    Args:
        request (TYPE): Description
        symbol (TYPE, optional): Description

    Returns:
        TYPE: Description
    """
    content = {}
    content['jump'] = jump('depth')
    content['mysymbol'] = symbol.upper()
    data = redis2.get(f'depth_result_{symbol}')
    #print(data)
    #print('==============')
    key = ['timestamp', 'content', 'data_volume',
           'volume_timelist', 'time_liqu_list', 'data_liqu_list']
    data2 = redis2.get(f'depth_signal_{symbol}')
    for i, k in enumerate(key):
        if k == 'content':
            for m in data[i]:
                if m[0] in data2.keys():
                    m += data2[m[0]]
                else:
                    m += [None]*len(list(data2.values())[0])
            content[k] = data[i][-30:]
    #print(content)
        # 增加趋势监控内容

        #if k == 'data_liqu_list':
        #    tempdata = [d[:10] for d in data[i]]
        #    content[k] = tempdata
        #else:
        #    content[k] = data[i]
    return render(request, 'depth.html', content)


def fundingRate(request):
    """资金费率监控

    Args:
        request (TYPE): Description

    Returns:
        TYPE: Description
    """
    content = {}
    content['jump'] = jump()
    try:
        info = redis2.get("fundingrate_result_info")
        content['timestamp'] = info[0]
        content['columns'] = info[1]
        content['content'] = redis2.get('fundingrate_result_array')
    except:
        pass
    return render(request, 'fundingRate.html', content)


