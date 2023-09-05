import sys
sys.path.append('/usr/local/server')
import time
# import threading
# import traceback
# import Toolbox as tb
# import numpy as np
# from django.shortcuts import render
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
                                'bnb-htusdt','chzusdt']
        self.comboSymbols = ['atomusdt']
        self.coinSwapSymbols = ['btcusd', 'ethusd', 'dotusd', 'uniusd', 'ltcusd', 'eosusd',
                                'xrpusd', 'trxusd', 'adausd', 'bchusd']
        self.coinsSymbols = [
            'btcusdt(lego)',
            #'btcusd(wt)',
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
                            'oceanusdt', 'filusdt',
                            'ltcusdt',
                            'sushiusdt',
                            'bchusdt',
                            ]
        # self.redbullSymbols = ['btcusdt', 'ethusdt', 'trxusdt', 'test21']
        self.coinStoreSymbols = [
            'btcusdt',
            'ethusdt',
            'trxusdt',
            'uniusdt',
            'aaveusdt',
            'linkusdt',
            'sushiusdt',
            'zrxusdt',
            'dogeusdt',
            '1inchusdt',
            'snxusdt',
            'compusdt',
            'lrcusdt',
            'mkrusdt',
            'grtusdt',
            'oceanusdt',
            'manausdt',
            'rsrusdt',
            'yfiusdt',
            'maticusdt',
            'trbusdt',
            'omgusdt',
            'rlcusdt',
            'crvusdt',
            'enjusdt',
            'aliceusdt',
            'sxpusdt',
            'chzusdt',
            'akrousdt',
            'dentusdt',
            'bakeusdt',
            'sandusdt',
            'unfiusdt',
            'reefusdt',
            'dotusdt',
            'renusdt',
            'ksmusdt',
            'chrusdt',
            'srmusdt',
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


# paras = Params()
# redis = tb.Redis()  # 配置redis
#redis2 = tb.Redis(host='18.178.124.254')  # 配置redis
# redis2 = tb.Redis()
# data = redis2.query()
# print(data)
# for i in data:
#     if i[:13] == 'depth_result_':
#         print(i)
# data = redis2.get(f'depth_result_btc')
# print(len(data[5]), type(data[5]))
# tempdata = [i[:10] for i in data[5]]
# print(tempdata)
# exit()

prefixDic = {
    'usdtSwap': 'wbfUsdtSwap',
    'combo': 'wbfUsdtSwap',
    'coinSwap': 'wbfCoinSwap',
    'coins': 'wbfCoins',
    'spot': 'wbfSpot',
    'etp': 'wbfSpotETP',
    'coinStore': 'coinStoreSpot',
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
        f"<a href='{paras.door}usdtSwap/{paras.usdtSwapSymbols[0]}/'>正向永续合约</a>",
        f"<a href='{paras.door}coinStoreUsdtSwap/{paras.coinStoreUsdtSwapSymbols[0]}/'>coinStore正向永续</a>",
        f"<a href='{paras.door}coinSwap/{paras.coinSwapSymbols[0]}/'>反向永续合约</a>",
        f"<a href='{paras.door}spot/{paras.spotSymbols[0]}/'>现货</a>",
        f"<a href='{paras.door}etp/{paras.etpSymbols[0]}/'>ETP</a>",
        f"<a href='{paras.door}coinStore/{paras.coinStoreSymbols[0]}/'>coinStore</a>",
        f"<a href='{paras.door}coins/{paras.coinsSymbols[0]}/'>全币种合约</a>",
    ]
    jump2 = [
        f"<a href='{paras.door}hedgeAccount/'>套保账户</a>",
        f"<a href='{paras.door}depth/{paras.depthSymbols[0]}/'>流动性监控</a>",
        f"<a href='{paras.door}fundingRate/'>各交易所资金费率监控</a>",
    ]
    jump3 = [
        # f"<a href='{paras.door}binanceUsdtSwap/{paras.binanceUsdtSwapSymbols[0]}/'>币安正向合约</a>",
        f"<a href='{paras.door}arbitrage/{paras.arbitrageSymbols[0]}/'>套利</a>",
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
            pls[i] = np.nansum([float(i.split(':')[-1]) for i in data])
        except:
            print(traceback.format_exc())
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
        content['content'] = redis2.get(f'wbfCoins_{symbol}_table')
        for d in content['content']:
            d[-1] = f"<a href='{paras.door}coins/{symbol}/{d[1]}/hisDeals'>{d[-1]}</a>"
        content['info'] = redis2.get(f'wbfCoins_{symbol}_info')
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
    except:
        pass
    return render(request, 'monitorNew.html', content)


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
    key = ['timestamp', 'content', 'data_volume',
           'volume_timelist', 'time_liqu_list', 'data_liqu_list']
    print(data)
    for i, k in enumerate(key):
        if k == 'data_liqu_list':
            tempdata = [i[:10] for i in data[i]]
            content[k] = tempdata
        else:
            content[k] = data[i]
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

if __name__ == '__main__':
    # res = [{'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559205, 'clientOrderId': None, 'price': 0.28119, 'vol': 4318.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559206, 'clientOrderId': None, 'price': 0.28109, 'vol': 5080.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559212, 'clientOrderId': None, 'price': 0.28461, 'vol': 37.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559201, 'clientOrderId': None, 'price': 0.28159, 'vol': 2152.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559200, 'clientOrderId': None, 'price': 0.28169, 'vol': 1791.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559220, 'clientOrderId': None, 'price': 0.28541, 'vol': 120.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559213, 'clientOrderId': None, 'price': 0.28471, 'vol': 44.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559207, 'clientOrderId': None, 'price': 0.28099, 'vol': 5944.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559217, 'clientOrderId': None, 'price': 0.28511, 'vol': 82.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559209, 'clientOrderId': None, 'price': 0.28431, 'vol': 22.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559214, 'clientOrderId': None, 'price': 0.28481, 'vol': 52.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559211, 'clientOrderId': None, 'price': 0.28451, 'vol': 31.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559210, 'clientOrderId': None, 'price': 0.28441, 'vol': 26.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559203, 'clientOrderId': None, 'price': 0.28139, 'vol': 3074.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559215, 'clientOrderId': None, 'price': 0.28491, 'vol': 61.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559222, 'clientOrderId': None, 'price': 0.28561, 'vol': 141.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559219, 'clientOrderId': None, 'price': 0.28531, 'vol': 107.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559216, 'clientOrderId': None, 'price': 0.28501, 'vol': 71.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559208, 'clientOrderId': None, 'price': 0.28421, 'vol': 18.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559218, 'clientOrderId': None, 'price': 0.28521, 'vol': 94.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559204, 'clientOrderId': None, 'price': 0.28129, 'vol': 3652.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559202, 'clientOrderId': None, 'price': 0.28149, 'vol': 2577.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401391, 'symbol': 'ftm/usdt', 'orderId': 1742555474559221, 'clientOrderId': None, 'price': 0.28551, 'vol': 132.2, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401390, 'symbol': 'ftm/usdt', 'orderId': 1742555474559198, 'clientOrderId': None, 'price': 0.28245, 'vol': 1228.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401390, 'symbol': 'ftm/usdt', 'orderId': 1742555474559197, 'clientOrderId': None, 'price': 0.28255, 'vol': 1012.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401390, 'symbol': 'ftm/usdt', 'orderId': 1742555474559199, 'clientOrderId': None, 'price': 0.28235, 'vol': 1486.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401390, 'symbol': 'ftm/usdt', 'orderId': 1742555474559195, 'clientOrderId': None, 'price': 0.28275, 'vol': 682.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401390, 'symbol': 'ftm/usdt', 'orderId': 1742555474559196, 'clientOrderId': None, 'price': 0.28265, 'vol': 832.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401388, 'symbol': 'ftm/usdt', 'orderId': 1742555474559193, 'clientOrderId': None, 'price': 0.28344, 'vol': 12.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401388, 'symbol': 'ftm/usdt', 'orderId': 1742555474559194, 'clientOrderId': None, 'price': 0.28354, 'vol': 15.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401388, 'symbol': 'ftm/usdt', 'orderId': 1742555474559191, 'clientOrderId': None, 'price': 0.28324, 'vol': 8.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401388, 'symbol': 'ftm/usdt', 'orderId': 1742555474559190, 'clientOrderId': None, 'price': 0.28314, 'vol': 7.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661830401388, 'symbol': 'ftm/usdt', 'orderId': 1742555474559192, 'clientOrderId': None, 'price': 0.28334, 'vol': 10.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744341, 'clientOrderId': None, 'price': 0.27789, 'vol': 12844.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744336, 'clientOrderId': None, 'price': 0.27839, 'vol': 6967.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744333, 'clientOrderId': None, 'price': 0.27869, 'vol': 4353.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744337, 'clientOrderId': None, 'price': 0.2783, 'vol': 8042.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744340, 'clientOrderId': None, 'price': 0.27799, 'vol': 11675.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744328, 'clientOrderId': None, 'price': 0.27919, 'vol': 1806.2, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744339, 'clientOrderId': None, 'price': 0.27809, 'vol': 10433.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744330, 'clientOrderId': None, 'price': 0.27899, 'vol': 2598.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744334, 'clientOrderId': None, 'price': 0.27859, 'vol': 5121.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744331, 'clientOrderId': None, 'price': 0.27889, 'vol': 3099.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744329, 'clientOrderId': None, 'price': 0.27909, 'vol': 2170.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744335, 'clientOrderId': None, 'price': 0.27849, 'vol': 5992.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744342, 'clientOrderId': None, 'price': 0.2778, 'vol': 13766.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744332, 'clientOrderId': None, 'price': 0.2788, 'vol': 3681.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083401, 'symbol': 'ftm/usdt', 'orderId': 1742536266744338, 'clientOrderId': None, 'price': 0.27819, 'vol': 9206.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083396, 'symbol': 'ftm/usdt', 'orderId': 1742536266744322, 'clientOrderId': None, 'price': 0.27986, 'vol': 1498.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083396, 'symbol': 'ftm/usdt', 'orderId': 1742536266744321, 'clientOrderId': None, 'price': 0.27995, 'vol': 1238.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083396, 'symbol': 'ftm/usdt', 'orderId': 1742536266744320, 'clientOrderId': None, 'price': 0.28005, 'vol': 1021.2, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1661812083396, 'symbol': 'ftm/usdt', 'orderId': 1742536266744319, 'clientOrderId': None, 'price': 0.28015, 'vol': 839.5, 'matchVol': 329.5, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814444, 'clientOrderId': None, 'price': 0.26879, 'vol': 4846.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814442, 'clientOrderId': None, 'price': 0.26899, 'vol': 3562.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814450, 'clientOrderId': None, 'price': 0.26819, 'vol': 9575.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814436, 'clientOrderId': None, 'price': 0.26959, 'vol': 1256.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814445, 'clientOrderId': None, 'price': 0.26869, 'vol': 5594.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814443, 'clientOrderId': None, 'price': 0.26889, 'vol': 4168.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814439, 'clientOrderId': None, 'price': 0.26929, 'vol': 2156.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814441, 'clientOrderId': None, 'price': 0.26909, 'vol': 3028.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814447, 'clientOrderId': None, 'price': 0.26849, 'vol': 7257.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814438, 'clientOrderId': None, 'price': 0.26939, 'vol': 1807.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814446, 'clientOrderId': None, 'price': 0.26859, 'vol': 6403.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814440, 'clientOrderId': None, 'price': 0.26919, 'vol': 2561.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814437, 'clientOrderId': None, 'price': 0.26949, 'vol': 1509.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814449, 'clientOrderId': None, 'price': 0.26829, 'vol': 8934.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511307, 'symbol': 'ftm/usdt', 'orderId': 1737718508814448, 'clientOrderId': None, 'price': 0.26839, 'vol': 8120.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814421, 'clientOrderId': None, 'price': 0.27231, 'vol': 416.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814430, 'clientOrderId': None, 'price': 0.27321, 'vol': 1854.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814429, 'clientOrderId': None, 'price': 0.27311, 'vol': 1606.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814424, 'clientOrderId': None, 'price': 0.27261, 'vol': 714.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814422, 'clientOrderId': None, 'price': 0.27241, 'vol': 500.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814426, 'clientOrderId': None, 'price': 0.27281, 'vol': 1004.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814432, 'clientOrderId': None, 'price': 0.27341, 'vol': 2406.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814434, 'clientOrderId': None, 'price': 0.27361, 'vol': 2962.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814431, 'clientOrderId': None, 'price': 0.27331, 'vol': 2123.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814433, 'clientOrderId': None, 'price': 0.27351, 'vol': 2692.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814428, 'clientOrderId': None, 'price': 0.27301, 'vol': 1382.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814423, 'clientOrderId': None, 'price': 0.27251, 'vol': 599.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814427, 'clientOrderId': None, 'price': 0.27291, 'vol': 1181.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814425, 'clientOrderId': None, 'price': 0.27271, 'vol': 849.2, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511305, 'symbol': 'ftm/usdt', 'orderId': 1737718508814435, 'clientOrderId': None, 'price': 0.27371, 'vol': 3175.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511303, 'symbol': 'ftm/usdt', 'orderId': 1737718508814414, 'clientOrderId': None, 'price': 0.27156, 'vol': 285.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511303, 'symbol': 'ftm/usdt', 'orderId': 1737718508814411, 'clientOrderId': None, 'price': 0.27126, 'vol': 158.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511303, 'symbol': 'ftm/usdt', 'orderId': 1737718508814417, 'clientOrderId': None, 'price': 0.27053, 'vol': 583.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511303, 'symbol': 'ftm/usdt', 'orderId': 1737718508814419, 'clientOrderId': None, 'price': 0.27033, 'vol': 861.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511303, 'symbol': 'ftm/usdt', 'orderId': 1737718508814420, 'clientOrderId': None, 'price': 0.27023, 'vol': 1042.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511303, 'symbol': 'ftm/usdt', 'orderId': 1737718508814415, 'clientOrderId': None, 'price': 0.27166, 'vol': 345.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511303, 'symbol': 'ftm/usdt', 'orderId': 1737718508814412, 'clientOrderId': None, 'price': 0.27136, 'vol': 193.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511303, 'symbol': 'ftm/usdt', 'orderId': 1737718508814413, 'clientOrderId': None, 'price': 0.27146, 'vol': 235.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511303, 'symbol': 'ftm/usdt', 'orderId': 1737718508814416, 'clientOrderId': None, 'price': 0.27063, 'vol': 478.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1657217511303, 'symbol': 'ftm/usdt', 'orderId': 1737718508814418, 'clientOrderId': None, 'price': 0.27043, 'vol': 710.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923504887, 'symbol': 'ftm/usdt', 'orderId': 1737410220130665, 'clientOrderId': None, 'price': 0.25425, 'vol': 274.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923504887, 'symbol': 'ftm/usdt', 'orderId': 1737410220130660, 'clientOrderId': None, 'price': 0.25324, 'vol': 759.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923504887, 'symbol': 'ftm/usdt', 'orderId': 1737410220130664, 'clientOrderId': None, 'price': 0.25415, 'vol': 225.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923504887, 'symbol': 'ftm/usdt', 'orderId': 1737410220130663, 'clientOrderId': None, 'price': 0.25406, 'vol': 185.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923504887, 'symbol': 'ftm/usdt', 'orderId': 1737410220130659, 'clientOrderId': None, 'price': 0.25334, 'vol': 624.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923504887, 'symbol': 'ftm/usdt', 'orderId': 1737410220130666, 'clientOrderId': None, 'price': 0.25435, 'vol': 333.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923504887, 'symbol': 'ftm/usdt', 'orderId': 1737410220130667, 'clientOrderId': None, 'price': 0.25445, 'vol': 403.2, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923504887, 'symbol': 'ftm/usdt', 'orderId': 1737410220130658, 'clientOrderId': None, 'price': 0.25344, 'vol': 512.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923504887, 'symbol': 'ftm/usdt', 'orderId': 1737410220130662, 'clientOrderId': None, 'price': 0.25305, 'vol': 1114.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923504887, 'symbol': 'ftm/usdt', 'orderId': 1737410220130661, 'clientOrderId': None, 'price': 0.25314, 'vol': 921.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923498849, 'symbol': 'ftm/usdt', 'orderId': 1737410213838956, 'clientOrderId': None, 'price': 0.25173, 'vol': 4458.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923498849, 'symbol': 'ftm/usdt', 'orderId': 1737410213838958, 'clientOrderId': None, 'price': 0.25154, 'vol': 5983.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923498849, 'symbol': 'ftm/usdt', 'orderId': 1737410213838957, 'clientOrderId': None, 'price': 0.25163, 'vol': 5183.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548066, 'clientOrderId': None, 'price': 0.25213, 'vol': 2306.2, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548065, 'clientOrderId': None, 'price': 0.25223, 'vol': 1933.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548069, 'clientOrderId': None, 'price': 0.25183, 'vol': 3810.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548075, 'clientOrderId': None, 'price': 0.25124, 'vol': 8686.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548077, 'clientOrderId': None, 'price': 0.25105, 'vol': 10242.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548071, 'clientOrderId': None, 'price': 0.25163, 'vol': 5183.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548068, 'clientOrderId': None, 'price': 0.25193, 'vol': 3239.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548067, 'clientOrderId': None, 'price': 0.25204, 'vol': 2739.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548063, 'clientOrderId': None, 'price': 0.25243, 'vol': 1343.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548073, 'clientOrderId': None, 'price': 0.25143, 'vol': 6849.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548072, 'clientOrderId': None, 'price': 0.25154, 'vol': 5983.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548076, 'clientOrderId': None, 'price': 0.25114, 'vol': 9556.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548074, 'clientOrderId': None, 'price': 0.25133, 'vol': 7762.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548070, 'clientOrderId': None, 'price': 0.25173, 'vol': 4458.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492807, 'symbol': 'ftm/usdt', 'orderId': 1737410207548064, 'clientOrderId': None, 'price': 0.25233, 'vol': 1614.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547999, 'clientOrderId': None, 'price': 0.25637, 'vol': 3871.2, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547990, 'clientOrderId': None, 'price': 0.25546, 'vol': 1109.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547991, 'clientOrderId': None, 'price': 0.25557, 'vol': 1312.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547993, 'clientOrderId': None, 'price': 0.25576, 'vol': 1806.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547998, 'clientOrderId': None, 'price': 0.25627, 'vol': 3518.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547992, 'clientOrderId': None, 'price': 0.25566, 'vol': 1543.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547997, 'clientOrderId': None, 'price': 0.25617, 'vol': 3144.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547987, 'clientOrderId': None, 'price': 0.25516, 'vol': 654.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547995, 'clientOrderId': None, 'price': 0.25597, 'vol': 2423.9, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547988, 'clientOrderId': None, 'price': 0.25526, 'vol': 783.2, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547989, 'clientOrderId': None, 'price': 0.25536, 'vol': 934.2, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547994, 'clientOrderId': None, 'price': 0.25587, 'vol': 2099.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207548000, 'clientOrderId': None, 'price': 0.25647, 'vol': 4149.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547986, 'clientOrderId': None, 'price': 0.25507, 'vol': 544.4, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492804, 'symbol': 'ftm/usdt', 'orderId': 1737410207547996, 'clientOrderId': None, 'price': 0.25608, 'vol': 2774.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'LIMIT', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492802, 'symbol': 'ftm/usdt', 'orderId': 1737410207547985, 'clientOrderId': None, 'price': 0.25305, 'vol': 1114.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492802, 'symbol': 'ftm/usdt', 'orderId': 1737410207547984, 'clientOrderId': None, 'price': 0.25314, 'vol': 921.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492802, 'symbol': 'ftm/usdt', 'orderId': 1737410207547981, 'clientOrderId': None, 'price': 0.25344, 'vol': 512.1, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492802, 'symbol': 'ftm/usdt', 'orderId': 1737410207547983, 'clientOrderId': None, 'price': 0.25324, 'vol': 759.7, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492802, 'symbol': 'ftm/usdt', 'orderId': 1737410207547982, 'clientOrderId': None, 'price': 0.25334, 'vol': 624.6, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'buy', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492801, 'symbol': 'ftm/usdt', 'orderId': 1737410207547976, 'clientOrderId': None, 'price': 0.25406, 'vol': 207.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492801, 'symbol': 'ftm/usdt', 'orderId': 1737410207547978, 'clientOrderId': None, 'price': 0.25425, 'vol': 307.8, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492801, 'symbol': 'ftm/usdt', 'orderId': 1737410207547977, 'clientOrderId': None, 'price': 0.25415, 'vol': 253.0, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492801, 'symbol': 'ftm/usdt', 'orderId': 1737410207547980, 'clientOrderId': None, 'price': 0.25445, 'vol': 451.5, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}, {'ts': 1656923492801, 'symbol': 'ftm/usdt', 'orderId': 1737410207547979, 'clientOrderId': None, 'price': 0.25435, 'vol': 373.3, 'matchVol': 0.0, 'amt': None, 'matchAmt': None, 'side': 'sell', 'offset': None, 'type': 'POST_ONLY', 'postOnly': None, 'fee': None, 'feeAsset': None, 'status': None, 'source': None}]
    # try:
    #     for r in res:
    #         print(r)
    #         if r['side'] == 'buy':
    #             buy_order = [r['price'], round(r['vol'] - r['matchVol'], 3)]
    #             dict_buy_order = {}
    #             for i in buy_order:
    #                 if i[0] not in dict_buy_order.keys():
    #                     dict_buy_order[i[0]] = 0
    #                 dict_buy_order[i[0]] += i[1]
    #             buy_order = list(dict_buy_order.items())
    #             print(buy_order)
    #             buy_order.sort(key=lambda x: x[0], reverse=True)
    #         else:
    #             sell_order = [r['price'], round(r['vol'] - r['matchVol'], 3)]
    #             dict_sell_order = {}
    #             for i in sell_order:
    #                 if i[0] not in dict_sell_order.keys():
    #                     d1.7854e-08ict_sell_order[i[0]] = 0
    #                 dict_sell_order[i[0]] += i[1]
    #             sell_order = list(dict_sell_order.items())
    #             sell_order.sort(key=lambda x: x[0], reverse=True)
    # except:
    #     sell_order = []
    #     buy_order = []
    #
    # print(buy_order)


