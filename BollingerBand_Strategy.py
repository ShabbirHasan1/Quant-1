# I wrote this strategy for learning purpose on Blueshift 

# Tested for Start Date = 20 Jul 2014, End Date = 20 Jul 2017 

from zipline.api import order_target_percent, symbol, record, schedule_function, date_rules

def initialize(context):
    context.jj = symbol('JNJ')

    schedule_function(check_bands, date_rules.every_day())

def check_bands(context, data):
    cur_price = data.current(context.jj, 'price')

    prices = data.history(context.jj, 'price', 20, '1d')

    avg = prices.mean()
    std = prices.std()
    lower_band = avg - (2*std)
    upper_band = avg + (2*std)

    if cur_price <= lower_band:
        order_target_percent(context.jj, 1.0) 
        print('BUYING')

    elif cur_price >= upper_band:
        order_target_percent(context.jj, -1.0)
        print('SHORTING')
    
    else:
        pass

    
    record(upper = upper_band,lower = lower_band,mavg_20 = avg,price = cur_price)
