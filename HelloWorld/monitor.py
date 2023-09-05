import sys
sys.path.append('/usr/local/server')
import numpy as np
import pandas as pd
import Toolbox as tb
import psutil as psu
import command
from wbfAPI.data import DataClient as dc
from wbfAPI import exchange
import os
import time
import traceback
timeGap = 30


class Monitor():
    '''============================================================'''
    '''==========================Warning Function=================='''
    '''============================================================'''

    def _aliveWarning(self, config, data):
        """运行状态报警

        Args:
            config ([type]): [description]
            data ([type]): [description]
        """
        if config['aliveWarning'] and 'off' in data[0]:
            tb.warning(f"{config['cnName']} 掉线!! 撤掉所有挂单",
                       contractSymbol=self.contractSymbol)
            try:
                config[self.exchange].cancelAll(self.contractSymbol)
            except:
                pass
            config['aliveWarning'] = False
            if config.get('keepAlive', False):
                command.start(config['pidName'][0])

        elif 'off' not in data[0]:
            if not config['aliveWarning']:
                tb.warning(f"{config['cnName']} 上线!!",
                           contractSymbol=self.contractSymbol)
            config['aliveWarning'] = True

    def _balanceWarning(self, config, data):
        for exc, value in data.items():
            if value['leverRate'] <= (1/config.get('leverLimit', 3)*100):
                if time.time() - config.get('warningTime', 0) >= 600:
                    config['warningTime'] = time.time()
                    tb.warning(
                        f"{config['cnName']} 杠杆超过 {config.get('leverLimit', 3)}!!!", contractSymbol=self.contractSymbol, method='margin')
                    if config.get('phoneNumber', 15210166821):
                        try:
                            tb.warningCall(f"{self.contractSymbol} {config['cnName']} 杠杆超过{config.get('leverLimit', 3)}", config.get('phoneNumber', 15210166821))  
                        except:
                            pass

    def _loadYaml(self, yaml):
        """读取配置文件

        Args:
            yaml (TYPE): Description
        """
        config = tb.loadYaml(yaml)
        # 配置全局变量
        [setattr(self, v, k) for v, k in config['base'].items()]
        del config['base']

        # 配置log
        self.log1 = tb.Log('monitorRecord.log')
        self.log2 = tb.Log('monitorError.log')

        return config

    def _reset(self):
        self.dc = dc.SDK(f"{getattr(self, 'contractId', 0)}")

    def __init__(self, yaml):
        config = self._loadYaml(yaml)
        # self.redis = tb.Redis(host='18.178.124.254')
        self.redis = tb.Redis(host=getattr(self, 'redisHost', '10.57.7.241'))
        # self.redis = tb.Redis()
        self.dc = dc.SDK(f"{getattr(self, 'contractId', 0)}")
        self.binanceSpotRest = exchange.binanceSpot.AccountRest('', '')
        # self.binanceCoinSwapUnitDic = {
        #     'btc/usd': 100,
        # }
        if getattr(self, 'model', 'default') == 'arbitrage':
            self.binanceCoinSwapUnitDic = exchange.binanceCoinSwap.AccountRest('', '').getContract()['data']
            self.binanceCoinFuturesUnitDic = exchange.binanceCoinFutures.AccountRest('', '').getContract()['data']
            self.huobiCoinFuturesUnitDic = exchange.huobiCoinFutures.AccountRest('', '').getContract()['data']
        self.init(config)  # 初始化
        pass

    def init(self, config):
        # uid池子
        self.uids = [config[v]['uid'] for v in config if 'trace' not in config[v]['strategyName']]

        # 配置账号
        for v in list(config.keys()):
            config[v]['excList'] = [l[0] for l in config[v]['exchange']]

            for exc in config[v]['exchange']:
                exc, *key = exc
                config[v][exc] = getattr(
                    getattr(exchange, exc), 'AccountRest')(*key)

            # 报警开关
            config[v]['aliveWarning'] = True
            # 昨日资产
            try:
                config[v]['yesterdayAsset'] = eval(self.redis.lrange(
                    f"{self.exchange}_{self.contractSymbol}_{config[v]['uid']}_yesterdayAsset",
                    start=0,
                    end=0,
                )[0])[1]
            except:
                self.log2.write(traceback.format_exc())
        self.accountConfig = config

    def getPidList(self):
        """拿取进程名称
        """
        pids = psu.pids()
        pidNames = {}
        for pid in pids:
            try:
                name = psu.Process(pid).cmdline()
                if name[-1].endswith('.py'):
                    pidNames[name[-1].split('/')[-1]] = pid
            except:
                continue
        self.pidNames = pidNames

    def pushServerKeepAlive(self):
        """保持DataPushServer运行
        """
        process = f"DataPushServer{self.contractId}.py"
        if process not in self.pidNames:
            os.system(
                f"cd /usr/local/server && nohup python -u DataPushServer{self.contractId}.py > DataPushServer{self.contractId}.log 2>&1 &")
            tb.warning(
                f"监测到DataPushServer{self.contractId}进程掉线 重启进程", contractSymbol=self.contractSymbol)

    def priceInfo(self):
        """获取价格信息
        """
        self.current = 0
        self.clp = 0
        self.tick = {'未知': [0, 0]}

        try:
            self.clpD = self.dc.getClearPrice(
                symbol=self.contractSymbol, exc=getattr(self, 'clpExchange', self.exchange))
            self.clp = round(self.clpD['data'][1], self.precision)
            self.tick = dict(zip(self.clpD['extra']['compoName'], [[np.round(self.clpD['extra']['compo'][i], self.precision), round(
                self.clpD['extra']['weight'][i]*100, self.precision)] for i in range(len(self.clpD['extra']['compo']))]))
        except:
            self._reset()
            self.log2.write(traceback.format_exc())
        try:
            if self.exchange == 'wbfSpotETP':
                # self.current = self.accountConfig['account1']['wbfSpotETP'].getTick(self.contractSymbol)['data'][-1][1]
                # depth = self.accountConfig['account1']['wbfSpotETP'].getDepth(self.contractSymbol)['data']
                # self.current = (depth[1][0][0] + depth[2][0][0]) / 2
                self.current = self.accountConfig['account1']['wbfSpotETP'].getMarket(self.contractSymbol)
                self.symbolCurrent = self.accountConfig['account1'][self.tickExchange].getTick(self.tickSymbol)['data'][-1][1]
            else:
                # print(getattr(self, 'tickSymbol', self.contractSymbol))
                # print(getattr(self, 'tickExchange', self.exchange))
                self.current = self.dc.getTick(symbol=getattr(self, 'tickSymbol', self.contractSymbol), exc=getattr(self, 'tickExchange', self.exchange))['data'][-1][1]
                # print(current)
        except:
            self._reset()
            self.log2.write(traceback.format_exc())
            self.current = self.clp
    
    def marketPrice(self):
        price = self.binanceSpotRest.getMarket()['data']
        self.priceDic = price

    def alive(self, config):
        """是否running
        """
        status = np.array(
            ['run' if p in self.pidNames else 'off' for p in config['pidName']])
        self._aliveWarning(config, status)
        status = '|'.join(status)  # 转成str
        return status

    def getOpenOrders(self, config):
        data = {}
        excList = config['excList']
        for exc in excList:
            try:
                res = config[exc].getOpenOrders(self.contractSymbol)['data']
            except:
                res = []
            # print(res)
            openVol = round(np.nansum([
                r['vol'] - r['matchVol'] for r in res if (r['offset'] is None or r['offset'] == 'open')
            ]), 3)
            closeVol = round(np.nansum([
                r['vol'] - r['matchVol'] for r in res if r['offset'] == 'close'
            ]), 3)
            data[exc] = f"{openVol}|{closeVol}"
        config['openOrders'] = data

    def getOpenOrdersList(self, config):
        data = {}
        excList = config['excList']
        for exc in excList:
            try:
                res = config[exc].getOpenOrders(self.contractSymbol)['data']
            except:
                res = []
            # print(res)
            orderList = [[r['price'],round(r['vol'] - r['matchVol'],3),r['side']] for r in res if (r['offset'] is None or r['offset'] == 'open')]

            data[exc] = orderList
        config['openOrdersList'] = data

    def getCurrentDepth(self, config):
        data = {}
        excList = config['excList']
        for exc in excList:
            try:
                res = config[exc].getDepth(self.contractSymbol)['data']
            except:
                res = []
            # print(res)

            data[exc] = res
        config['currentDepth'] = data

    def getPosition(self, config):
        data = {}
        excList = config['excList']
        for exc in excList:
            if 'Spot' in exc:
                res = config[exc].getBalance()['data']
                # print(res)
                res = [r for r in res if r['balance'] > 0] 
                data[exc] = {r['symbol']: round(r['balance'], 6) for r in res}
            elif 'CoinSwap' in exc:
                res = config[exc].getPosition(getattr(self, f"{exc}Symbol", self.contractSymbol))['data']
                for r in res:
                    if r['posSide'] is not None:
                        if r['posSide'] == -1:
                            r['symbol'] = f"-{r['symbol']}"
                data[exc] = {
                    r['symbol']: [round(r['pos'], 6), r['unrealProfitLoss'], r['pos'] * getattr(self, f"{exc}Unit", 1) / r['openPrice']] \
                    if r['pos'] != 0. else [round(r['pos'], 6), 0, 0] for r in res
                }                
            else:
                res = config[exc].getPosition(getattr(self, f"{exc}Symbol", self.contractSymbol))['data']
                data[exc] = {
                    r['symbol']: [round(r['pos'], 6), r['unrealProfitLoss'], r['openAmt']] \
                    if r['pos'] != 0. else [round(r['pos'], 6), 0, 0] for r in res
                }
        config['position'] = data

        inventory = 0
        for exc, dic in data.items():
            inventory += dic.get(self.contractSymbol, [0])[0]
        if config.get('warningPosition', 0):
            if abs(inventory) > config['warningPosition']:
                if config.get('_warningPositionFlag', True):
                    tb.warningCall(f"{self.contractSymbol} {config['cnName']} 头寸超过{config['warningPosition']}", config.get('phoneNumber', 18981142505)) 
                    config['_warningPositionFlag'] = False
            else:
                config['_warningPositionFlag'] = True
        # print(config['position'])
        if self.timing <= 3 * timeGap:
            self.redis.lpush(
                f"{self.exchange}_{self.contractSymbol}_{config['uid']}_yesterdayPosition",
                str([self.date, data]),
                length=365,
            )
        
    def accountPosition(self, config):
        data = {}
        excList = config['excList']
        for exc in excList:
            if 'Spot' in exc:
                res = config[exc].getBalance()['data']
                data[exc] = {i['symbol']: round(i['balance'], 4) for i in res if i['balance']!=0.}
            else:
                res = config[exc].getBalance()['data']
                res = {i['symbol']: i['balance'] for i in res if i['balance']!=0.}
                pos = config[exc].getPosition('all')['data']
                config[f'{exc}PositionDetails'] = pos
                pos = {i['symbol']: i['pos'] for i in pos if i['pos']!=0.}
                res.update(pos)
                data[exc] = res
        config['position'] = data

    def getBalance(self, config):
        data = {}
        excList = config['excList']
        # legalCurrency = config.get('legalCurrency', 'usdt')
        legalCurrency = getattr(self, 'legalCurrency', 'usdt')
        for exc in excList:
            if 'Spot' in exc:
                bal = config['position'][exc]
                diff = bal.get(self.coin, 0) - config.get(f"{exc}BaseCoinVol", config['baseCoinVol'])
                asset = round(config['baseCoinPrice'] * config.get(f"{exc}BaseCoinVol", config['baseCoinVol'])
                              + bal.get(legalCurrency, 0)
                              + diff * self.current, 2)
                leverRate = float('inf')
            else:
                res = config[exc].getBalance()['data']
                bal = [r['balance']
                       for r in res if r['symbol'] == legalCurrency][0] if len(res) > 0 else 0
                config['position'][exc].update(
                    {r['symbol']: [round(r['balance'], 3), 0, 0] for r in res if r['balance'] != 0.}
                )
                # print(config['position'])
                unrealized = np.nansum(
                    [v[1] for v in config['position'][exc].values()]
                )
                asset = round(bal + unrealized, 2)
                # print(asset)
                # print((abs(config['position'][exc].get(self.contractSymbol, [0, 0, 0])[0]) * self.current))
                leverRate = round(asset / (abs(config['position'][exc].get(getattr(self, f'{exc}Symbol', self.contractSymbol), [0, 0, 0])[0])* getattr(self, f'{exc}Unit', 1) * getattr(self, 'symbolCurrent', self.current)) * 100, 1)
            totalPL = round(asset - config[f"{exc}InitAsset"], 2)
            # totalPLRate = round(
            #     (asset / config[f"{exc}InitAsset"] - 1) * 100, 2)
            todayPL = round(
                asset - config.get('yesterdayAsset', {exc: np.nan}).get(exc, np.nan), 2)
            data[exc] = {
                'asset': asset,
                'totalPL': totalPL,
                # 'totalPLRate': totalPLRate,
                'todayPL': todayPL,
                'leverRate': leverRate,
            }
        self._balanceWarning(config, data)  # 风控

        # 算总
        if len(data) > 1:
            totalAsset = round(np.nansum([data[exc]['asset'] for exc in data]), 2)
            totalTotalPL = round(np.nansum([data[exc]['totalPL'] for exc in data]), 2)
            totalTodayPL = round(np.nansum([data[exc]['todayPL'] for exc in data]), 2)
            data['total'] = {
                'asset': totalAsset,
                'totalPL': totalTotalPL,
                'todayPL': totalTodayPL,
            }
        config['balance'] = data
        assetSnapShot = {exc: data[exc]['asset'] for exc in data}
        if self.timing >= 235800:
            yesterdayPL = {k: v['todayPL'] for k, v in data.items()}
            yesterdayPL['uid'] = config['uid']
            self.redis.set(f"{self.exchange}_{self.contractSymbol}_{config['uid']}_yesterdayPL", str(yesterdayPL))
        # 资产快照
        if self.timing <= 3 * timeGap:
            assetSnapShot = {exc: data[exc]['asset'] for exc in data}
            self.redis.lpush(
                f"{self.exchange}_{self.contractSymbol}_{config['uid']}_yesterdayAsset",
                str([self.date, assetSnapShot]),
                length=365,
            )
            config['yesterdayAsset'] = assetSnapShot

    def accountBalance(self, config):
        data = {}
        excList = config['excList']
        for exc in excList:
            if 'Spot' in exc:
                if getattr(self, 'legalCurrency', 'usdt') == 'usdt':
                    asset = np.nansum([self.priceDic.get(f'{k}/usdt', 1)*v for k, v in config['position'][exc].items()])
                else:
                    asset = np.nansum([v for k, v in config['position'][exc].items() if k==self.legalCurrency])
            elif 'CoinSwap' in exc:
                pos = config[f'{exc}PositionDetails']
                bal = config['position'][exc]
                for i in pos:
                    s = f"{i['symbol']}t"
                    bal[s.split('/')[0]] = round(bal[s.split('/')[0]] + float(i['unrealProfitLoss']), 4)
                asset = np.nansum([self.priceDic.get(f'{k}/usdt', 1)*v for k, v in bal.items() if not k.endswith('/usd')])
                nominalAsset = np.nansum([abs(getattr(self, f"{exc}UnitDic").get(k, 10)*v) for k, v in bal.items() if k.endswith('/usd')])
                leverRate = round(asset / nominalAsset * 100, 2)
            elif 'CoinFutures' in exc:
                pos = config[f'{exc}PositionDetails']
                bal = config['position'][exc]   
                if 'binance' in exc:  # 火币不需要调整
                    for i in pos:
                        s = i['symbol'].split('/')[0]
                        bal[s] = round(bal[s] + float(i['unrealProfitLoss']), 4)
                # print(bal)
                if getattr(self, 'legalCurrency', 'usdt') == 'usdt': 
                    asset = np.nansum([self.priceDic.get(f'{k}/usdt', 0)*v for k, v in bal.items() if not k.endswith('/usd')])
                    nominalAsset = np.nansum([abs(getattr(self, f"{exc}UnitDic").get(k, 10)*v) for k, v in bal.items() if '/usd/' in k])
                else:
                    asset = np.nansum([v for k, v in config['position'][exc].items() if k==self.legalCurrency])
                    nominalAsset = np.nansum([abs(getattr(self, f"{exc}UnitDic").get(k, 10)*v/self.priceDic.get(k.split('/')[0]+'/usdt')) for k, v in bal.items() if '/usd/' in k])
                leverRate = round(asset / nominalAsset * 100, 2)
                # print(asset, nominalAsset, leverRate)
            leverRate = float('inf') if 'Spot' in exc else leverRate
            totalPL = round(asset - config[f"{exc}InitAsset"], 4)
            totalPLRate = (asset / config[f"{exc}InitAsset"] - 1) * 100
            todayPL = round(
                asset - config.get('yesterdayAsset', {exc: np.nan}).get(exc, np.nan), 4)
            data[exc] = {
                'asset': asset,
                'totalPL': totalPL,
                'totalPLRate': totalPLRate,
                'todayPL': todayPL,
                'leverRate': leverRate,
            }
        self._balanceWarning(config, data)  # 风控

        # risk exposure
        for exc in excList:
            if 'Spot' in exc:
                pass
            elif 'CoinSwap' in exc:
                pos = config['position'][exc]
                for s in pos:
                    if s.endswith('/usd'):
                        coinSwap = pos[s] * getattr(self, f"{exc}UnitDic").get(s, 10)
                        spot = pos[s.split('/')[0]] * self.priceDic[s+'t']
                        pos[s] = f"{pos[s]}|{(coinSwap+spot):0.2f}"
            elif 'CoinFutures' in exc:
                pos = config['position'][exc]
                for s in pos:
                    if '/usd/' in s:
                        coinFutures = pos[s] * getattr(self, f"{exc}UnitDic").get(s, 10)
                        spot = pos[s.split('/')[0]] * self.priceDic[s.split('/')[0]+'/usdt']
                        pos[s] = f"{pos[s]}|{(coinFutures+spot):0.2f}"

        # 算总
        if len(data) > 1:
            totalAsset = round(np.nansum([data[exc]['asset'] for exc in data]), 4)
            totalTotalPL = round(np.nansum([data[exc]['totalPL'] for exc in data]), 4)
            totalTodayPL = round(np.nansum([data[exc]['todayPL'] for exc in data]), 4)
            totalPLRate = (totalAsset / (totalAsset - totalTotalPL) - 1) * 100
            data['total'] = {
                'asset': totalAsset,
                'totalPL': totalTotalPL,
                'todayPL': totalTodayPL,
                'totalPLRate': totalPLRate
            }
        config['balance'] = data
        assetSnapShot = {exc: data[exc]['asset'] for exc in data}
        if self.timing >= 235800:
            yesterdayPL = {k: v['todayPL'] for k, v in data.items()}
            yesterdayPL['uid'] = config['uid']
            self.redis.set(f"{self.exchange}_{self.contractSymbol}_{config['uid']}_yesterdayPL", str(yesterdayPL))
        # 资产快照
        if self.timing <= 3 * timeGap:
            assetSnapShot = {exc: data[exc]['asset'] for exc in data}
            self.redis.lpush(
                f"{self.exchange}_{self.contractSymbol}_{config['uid']}_yesterdayAsset",
                str([self.date, assetSnapShot]),
                length=365,
            )
            config['yesterdayAsset'] = assetSnapShot

    def getExposure(self, config):
        data = {}
        excList = config['excList']
        for exc in excList:
            if 'ETP' in exc:
                data[exc] = round((config['position'][exc].get(self.coin, 0) - config.get(f"{exc}BaseCoinVol", config['baseCoinVol'])) * getattr(self, f'{exc}Unit', 1) * self.current / getattr(self, 'symbolCurrent', 10), 6)
            elif 'Spot' in exc:
                data[exc] = round((config['position'][exc].get(self.coin, 0) - config.get(f"{exc}BaseCoinVol", config['baseCoinVol'])) * getattr(self, f'{exc}Unit', 1), 6)
            else:
                data[exc] = round(
                    config['position'][exc].get(getattr(self, f"{exc}Symbol", self.contractSymbol), [0,0,0])[0] * getattr(self, f'{exc}Unit', 1), 6) \
                    - round(
                        config['position'][exc].get(f"-{getattr(self, f'{exc}Symbol', self.contractSymbol)}", [0])[0] * getattr(self, f'{exc}Unit', 1), 6
                    )
        if len(data) > 1:  # 算总
            data['total'] = round(np.nansum(list(data.values())), 6)
        config['exposure'] = data

    def getDeals(self, config):
        data = {}
        excList = config['excList']
        today = int(tb.timestamp(strFormat='%Y%m%d'))
        for exc in excList:
            count = 100
            if self.timing <= 3 * timeGap:
                self.redis.delete(f"{self.exchange}_{self.contractSymbol}_{config['uid']}_{exc}_todayDeals")
                # continue
            try:
                res = config[exc].getDeals(self.contractSymbol, count=count)['data']
            except:
                res = [{'tradeId': -1, 'ts': time.time()}]

            # 读取deals
            exist = self.redis.get(f"{self.exchange}_{self.contractSymbol}_{config['uid']}_{exc}_todayDeals")
            if len(exist) == 0:
                tradeId, vol = 0, 0
                selfVol = 0
            else:
                tradeId, vol = exist
                # print(tradeId, vol)
                if 'wbf' in exc:
                    vol, selfVol = [float(i) for i in vol.split('|')]
                res = [i for i in res if i['tradeId'] > tradeId]
                # print(res)

            res = [
                i for i in res
                if int(time.strftime('%Y%m%d', time.localtime(int(i['ts']/1000)))) >= today
            ]
            data[exc] = round(np.nansum([i['vol'] for i in res]) * getattr(self, f'{exc}Unit', 1) + vol, 2)
            if 'wbf' in exc:  # 自成交
                # print([i for i in res if i['myUserId']==i['oppUserId']])
                selfTrade = round(np.nansum([i['vol'] for i in res if ((i['myUserId'] in self.uids) and (i['oppUserId'] in self.uids))]) * getattr(self, f'{exc}Unit', 1) + selfVol, 2)
                data[exc] = f"{data[exc]}|{selfTrade}"
            
            if len(res) > 0:
                self.redis.set(f"{self.exchange}_{self.contractSymbol}_{config['uid']}_{exc}_todayDeals", str([res[-1]['tradeId'], data[exc]]))

        if self.timing >= 235800:
            self.redis.set(f"{self.exchange}_{self.contractSymbol}_{config['uid']}_yesterdayDeals", str(data))

        config['deals'] = data

    def getTurnOver(self, config):
        data = {}
        yesterdayDeals = self.redis.get(f"{self.exchange}_{self.contractSymbol}_{config['uid']}_yesterdayDeals")
        if len(yesterdayDeals) == 0:
            for exc in config['excList']:
                data[exc] = 0.
        else:
            for exc in list(yesterdayDeals.keys()):
                try:
                    if 'wbf' in exc:
                        vol = float(yesterdayDeals[exc].split('|')[0])
                    else:
                        vol = yesterdayDeals[exc]
                    turnover = round(vol * self.current / config['balance'][exc]['asset'], 2)
                    data[exc] = turnover
                except:
                    continue
        # print(self.current)
        # print(yesterdayDeals)
        # print(config['balance'])
        # print(data)
        # if self.timing >= 235800:
        #     self.redis.set(f"{self.exchange}_{self.contractSymbol}_{config['uid']}_yesterdayTurnOver", str(data))
        config['turnover'] = data

    def main(self):
        if getattr(self, 'model', 'default') == 'default':
            self.timing = int(tb.timestamp(strFormat='%H%M%S'))
            self.date = tb.timestamp()

            self.getPidList()  # 获取进程
            self.pushServerKeepAlive()  # 保持程序稳定运行
            self.priceInfo()

            df = pd.DataFrame(np.zeros((len(self.accountConfig), 12)))
            for i, account in enumerate(self.accountConfig):
                try:
                    config = self.accountConfig[account]
                    time.sleep(1)
                    self.getOpenOrders(config)
                    self.getPosition(config)
                    self.getBalance(config)
                    self.getExposure(config)
                    self.getDeals(config)
                    self.getTurnOver(config)

                    # 合约的仓位调整
                    for exc in config['position']:
                        if 'Spot' not in exc:
                            config['position'][exc] = {
                                k: v[0] for k, v in config['position'][exc].items()}
                    df.iloc[i, 0] = config['cnName']
                    # df.iloc[i, 1] = f"{config['strategyName']}{config['strategyId']}"
                    df.iloc[i, 1] = int(config['uid'])
                    df.iloc[i, 2] = self.alive(config)
                    df.iloc[i, 3] = '\n'.join(
                        [f"{exc}:{config['balance'][exc]['asset']}" for exc in config['balance']])
                    df.iloc[i, 4] = '\n'.join(
                        [f"{exc}:{config['balance'][exc]['todayPL']}" for exc in config['balance']])
                    df.iloc[i, 5] = '\n'.join(
                        [f"{exc}:{config['balance'][exc]['totalPL']}" for exc in config['balance']])
                    # df.iloc[i, 7] = '\n'.join(
                    #     [f"{exc}: {config['balance'][exc]['totalPLRate']:0.4f}%" for exc in config['balance']])
                    df.iloc[i, 6] = '\n'.join(
                        [f"{exc}:{config['balance'][exc]['leverRate']}%" for exc in config['balance']\
                        if 'leverRate' in config['balance'][exc]])
                    df.iloc[i, 7] = '\n'.join(
                        [f"{exc}:{config['openOrders'][exc]}" for exc in config['openOrders']])
                    df.iloc[i, 8] = '\n'.join(
                        [f"{exc}:{config['position'][exc]}" for exc in config['position']])
                    df.iloc[i, 9] = '\n'.join(
                        [f"{exc}:{config['exposure'][exc]}" for exc in config['exposure']])
                    df.iloc[i, 10] = '\n'.join(
                        [f"{exc}:{config['deals'][exc]}" for exc in config['deals']])
                    df.iloc[i, 11] = '\n'.join(
                        [f"{exc}:{config['turnover'][exc]}" for exc in config['turnover']])
                    # df.iloc[i, 12] = '\n'.join(
                    #     [f"{exc}:{config['openOrdersList'][exc]}" for exc in config['openOrdersList']])
                    # df.iloc[i, 13] = '\n'.join(
                    #     [f"{exc}:{config['currentDepth'][exc]}" for exc in config['currentDepth']])

                    self.getOpenOrdersList(config)
                    self.getCurrentDepth(config)
                    data_orderlist = config['openOrdersList']
                    data_depth = config['currentDepth']
                except:
                    self.log2.write(traceback.format_exc())
                    continue
            table = str(df.values.tolist())
            table = table.replace('wbfUsdtSwap', 'wbf').replace('wbfCoins', 'wbf').replace('wbfCoinSwap', 'wbf')\
                .replace('wbfSpot', 'wbf').replace('binanceUsdtSwap', 'binance').replace('binanceCoinSwap', 'binance')\
                .replace('binanceSpot', 'binance').replace('coinStoreUsdtSwap', 'csUSwap')

            self.redis.set(
                f"{self.exchange}_{self.contractSymbol.replace('/', '')}_orderlist", str(data_orderlist))
            self.redis.set(
                f"{self.exchange}_{self.contractSymbol.replace('/', '')}_datadepth", str(data_depth))

            self.redis.set(
                f"{self.exchange}_{self.contractSymbol.replace('/', '')}_table", table)

            # tick去nan
            for k in list(self.tick.keys()):
                temp = np.array(self.tick[k])
                temp[np.isnan(temp)] = 0.
                self.tick[k] = temp.tolist()
            info = [self.date, self.coin, self.clp, self.current, self.tick, self.legalCurrency]
            # print(info)
            self.redis.set(
                f"{self.exchange}_{self.contractSymbol.replace('/', '')}_info", str(info))
            print(f"{self.exchange}_{self.contractSymbol.replace('/', '')}_info")
            # print(df)
        
        elif self.model == 'arbitrage':
            self.timing = int(tb.timestamp(strFormat='%H%M%S'))
            self.date = tb.timestamp()

            self.getPidList()  # 获取进程
            # self.pushServerKeepAlive()  # 保持程序稳定运行
            # self.priceInfo()
            self.marketPrice()

            df = pd.DataFrame(np.zeros((len(self.accountConfig), 9)))
            for i, account in enumerate(self.accountConfig):
                try:
                    config = self.accountConfig[account]
                    time.sleep(1)
                    # self.getOpenOrders(config)
                    self.accountPosition(config)
                    self.accountBalance(config)
                    # self.getExposure(config)
                    # self.getDeals(config)
                    # self.getTurnOver(config)
                    # 合约的仓位调整
                    df.iloc[i, 0] = config['cnName']
                    # df.iloc[i, 1] = f"{config['strategyName']}{config['strategyId']}"
                    df.iloc[i, 1] = int(config['uid'])
                    df.iloc[i, 2] = self.alive(config)
                    df.iloc[i, 3] = '\n'.join(
                        [f"{exc}:{config['balance'][exc]['asset']:0.4f}" for exc in config['balance']])
                    df.iloc[i, 4] = '\n'.join(
                        [f"{exc}:{config['balance'][exc]['todayPL']:0.4f}" for exc in config['balance']])
                    df.iloc[i, 5] = '\n'.join(
                        [f"{exc}:{config['balance'][exc]['totalPL']:0.4f}" for exc in config['balance']])
                    df.iloc[i, 6] = '\n'.join(
                        [f"{exc}: {config['balance'][exc]['totalPLRate']:0.4f}%" for exc in config['balance']])
                    df.iloc[i, 7] = '\n'.join(
                        [f"{exc}:{config['balance'][exc]['leverRate']:0.2f}%" for exc in config['balance']\
                        if 'leverRate' in config['balance'][exc]])
                    df.iloc[i, 8] = '\n'.join(
                        [f"{exc}:{config['position'][exc]}" for exc in config['position']])
                except:
                    self.log2.write(traceback.format_exc())
                    continue
            table = str(df.values.tolist())
            # table = table.replace('wbfUsdtSwap', 'wbf').replace('wbfCoins', 'wbf').replace('wbfCoinSwap', 'wbf')\
            #     .replace('wbfSpot', 'wbf').replace('binanceUsdtSwap', 'binance').replace('binanceCoinSwap', 'binance')\
            #     .replace('binanceSpot', 'binance')

            self.redis.set(
                f"{self.exchange}_{self.contractSymbol}_table", table)

            info = [self.date, 0, 0, 0, 0, self.legalCurrency]
            # print(info)
            self.redis.set(
                f"{self.exchange}_{self.contractSymbol}_info", str(info))
            print(f"{self.exchange}_{self.contractSymbol}_info")
            # print(df)


def _stop(yaml='monitor.yaml'):
    pass


def main(yaml='monitor.yaml'):
    task = Monitor(yaml=yaml)
    while 1:
        try:
            task.main()
        except:
            try:
                task.log2.write(traceback.format_exc())
                task._reset()
            except:
                pass
        time.sleep(timeGap)


if __name__ == '__main__':
    main()
