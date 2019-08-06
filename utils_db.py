import dataset
import numpy as np
import time
import pandas as pd


def insert(records):
    db = dataset.connect('sqlite:///data.db')
    table = db['orderbook']
    table.insert(records)

def get_latest():
    db = dataset.connect('sqlite:///data.db')
    table = db['orderbook']
    cmd = 'select date from orderbook ORDER BY date desc limit 1'
    res = db.query(cmd)
    date = list(res)[0]['date']

    cmd = 'select * from orderbook where date="%s"'%date
    res = db.query(cmd)
    res = list(res)
    df = pd.DataFrame(res)    
    
    df['bid_s001'] = df['bid_s001']/1000000
    df['ask_s001'] = df['ask_s001']/1000000

    df['bid_s005'] = df['bid_s005']/1000000
    df['ask_s005'] = df['ask_s005']/1000000

    df['bid_s010'] = df['bid_s010']/1000000
    df['ask_s010'] = df['ask_s010']/1000000

    pd.set_option("display.precision", 2)

    s = 'time@%s\n'%date

    df001 = df[['exchange', 'bid_s001', 'ask_s001']]
    s001 = df001.to_string(index=False)
    s += s001
    s += '\n--------\n'

    df005 = df[['exchange', 'bid_s005', 'ask_s005']]
    s005 = df005.to_string(index=False)
    s += s005
    s += '\n--------\n'

    df010 = df[['exchange', 'bid_s010', 'ask_s010']]
    s010 = df010.to_string(index=False)
    s += s010
    return s

if __name__ == '__main__':
    s = get_latest()
    print(s)



