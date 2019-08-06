import ccxt
import arrow
import utils_db

def get_ratio_sum(data, direction):
    if direction == 'bids':
        bids = data
        
        s001 = 0
        s005 = 0
        s010 = 0
        s020 = 0
        depth_ratio = 0
        depth_sum = 0
        
        depth_ratio = bids[0][0]/bids[-1][0] - 1
        for bid in data:
            price,amount = bid
            depth_sum += price * amount
            ratio = bids[0][0]/price - 1

            if ratio <= 0.010001 and depth_ratio >= 0.00978001:
                s001 += price * amount
            if ratio <= 0.05001 and depth_ratio >= 0.05001:
                s005 += price * amount
            if ratio <= 0.10001 and depth_ratio >= 0.1001:
                s010 += price * amount
            if ratio <= 0.20001 and depth_ratio >= 0.2001:
                s020 += price * amount
        res = {'bid_s001':s001,
                'bid_s005':s005,
                'bid_s010':s010,
                'bid_s020':s020,
                'bid_depth_ratio': depth_ratio,
                'bid_depth_sum': depth_sum}

        return res

    if direction == 'asks':
        asks = data 
        s001 = 0
        s005 = 0
        s010 = 0
        s020 = 0
        depth_ratio = 0
        depth_sum = 0
        
        depth_ratio = asks[-1][0]/asks[0][0] - 1
        for ask in asks:
            price,amount = ask
            depth_sum += price * amount
            ratio = price/asks[0][0] - 1

            if ratio <= 0.010001 and depth_ratio >= 0.009781001:
                s001 += price * amount

            if ratio <= 0.05001 and depth_ratio >= 0.05001:
                s005 += price * amount

            if ratio <= 0.10001 and depth_ratio >= 0.1001:
                s010 += price * amount

            if ratio <= 0.20001 and depth_ratio >= 0.2001:
                s020 += price * amount
        res = {'ask_s001':s001,
                'ask_s005':s005,
                'ask_s010':s010,
                'ask_s020':s020,
                'ask_depth_ratio': depth_ratio,
                'ask_depth_sum': depth_sum}
        return res

def huobi():

    huobipro = ccxt.huobipro()
    params = {'depth': 20,  'type':'step3'}
    data = huobipro.fetch_order_book('BTC/USDT', params = params)
    bids = data['bids']
    asks = data['asks']

    price = (bids[0][0] + asks[0][0])/2
    bids_info = get_ratio_sum(bids, 'bids')
    asks_info = get_ratio_sum(asks, 'asks')

    res = {}
    res.update(bids_info)
    res.update(asks_info)
    res['price'] = price
    res['exchange'] = 'huobi'
    return res

def binance():
    bnb = ccxt.binance()
    params = {'limit': 1000}
    data = bnb.fetch_order_book('BTC/USDT', params = params)
    bids = data['bids']
    asks = data['asks']

    price = (bids[0][0] + asks[0][0])/2
    bids_info = get_ratio_sum(bids, 'bids')
    asks_info = get_ratio_sum(asks, 'asks')

    res = {}
    res.update(bids_info)
    res.update(asks_info)
    res['price'] = price
    res['exchange'] = 'binance'
    return res

def bitfinex():
    bfx = ccxt.bitfinex()
    params = {'limit_asks':3000, 'limit_bids':3000}
    data = bfx.fetch_order_book('BTC/USD', params=params)
    asks = data['asks']
    bids = data['bids']

    price = (asks[0][0]+bids[0][0])/2
    bids_info = get_ratio_sum(bids, 'bids')
    asks_info = get_ratio_sum(asks, 'asks')

    res = {}
    res.update(bids_info)
    res.update(asks_info)
    res['price'] = price
    res['exchange'] = 'bitfinex'

    return res

def bitstamp():
    bs = ccxt.bitstamp() 
    params = {'group': 1}
    data = bs.fetch_order_book('BTC/USD', params=params)
    asks = data['asks']
    bids = data['bids']

    price = (asks[0][0]+bids[0][0])/2
    bids_info = get_ratio_sum(bids, 'bids')
    asks_info = get_ratio_sum(asks, 'asks')

    res = {}
    res.update(bids_info)
    res.update(asks_info)
    res['price'] = price
    res['exchange'] = 'bitstamp'

    return res
def coinbase():
    cb = ccxt.coinbasepro() 
    params = {'level': 3}
    data = cb.fetch_order_book('BTC/USD', params=params)
    asks = data['asks']
    bids = data['bids']

    price = (asks[0][0]+bids[0][0])/2
    bids_info = get_ratio_sum(bids, 'bids')
    asks_info = get_ratio_sum(asks, 'asks')

    res = {}
    res.update(bids_info)
    res.update(asks_info)
    res['price'] = price
    res['exchange'] = 'coinbase'

    return res
def main():
    dhuobi = huobi()
    dbnb = binance()
    
    try:
        dbfx = bitfinex()
    except:
        dbfx = None
    dcb = coinbase()
    bts = bitstamp()

    print('001')
    exs = ['huobi', 'bnb', 'bfx', 'cb', 'bts']
    idx = 0
    for ex in [dhuobi, dbnb, dbfx, dcb, bts]:
        if ex is None:continue
        print('@%s bid_s001: %s ask_s001: %s'%(exs[idx],ex['bid_s001']/1000000, ex['ask_s001']/1000000))
        idx += 1
    print('005')
    idx = 0
    for ex in [dhuobi, dbnb, dbfx, dcb, bts]:
        if ex is None:continue
        print('@%s bid_s005: %s ask_s005: %s'%(exs[idx],ex['bid_s005']/1000000, ex['ask_s005']/1000000))
        idx += 1
    
    date = arrow.now().datetime
    for exchange in [dhuobi, dbnb, dbfx, dcb, bts]:
        if exchange is None:continue
        exchange['date'] = date
        utils_db.insert(exchange)

if __name__ == '__main__':
    main()
