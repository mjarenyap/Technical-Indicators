"""
This is a template algorithm on Quantopian for you to adapt and fill in.
"""
import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS

import talib

def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    # AAPL, MSFT, and SPY
    context.securities = [sid(24)]
    context.long_ema_period = 50
    context.short_ema_period = 20
    context.bar_interval = '1d'
    context.bar_count = 200
    
    schedule_function(rebalance,
                      date_rules.every_day(),
                      time_rules.market_open(minutes=30))

def rebalance(context, data):
    ema_vs_ema(context, data)
    
def ema_vs_ema(context, data):    
    stock_series = data.history(context.securities, fields="price", bar_count=context.bar_count, frequency=context.bar_interval)
    
    for s in context.securities:
        long_ema = talib.EMA(stock_series[s][-(context.long_ema_period):], timeperiod=context.long_ema_period)
        short_ema = talib.EMA(stock_series[s][-(context.short_ema_period):], timeperiod=context.short_ema_period)
        open_orders = get_open_orders()
        
        if short_ema[-1] > long_ema[-1]:
            if s not in open_orders and is_wide(short_ema[-1], long_ema[-1]) >= 1:
                order_target_percent(s, 1.0)
                
        elif short_ema[-1] < long_ema[-1]:
            if s not in open_orders and is_wide(short_ema[-1], long_ema[-1]) >= 1:
                order_target_percent(s, -1.0)
    
def ema_vs_closing(context, data):
    period = 2
    freq = "1d"
    my_stock_series = data.history(context.securities, fields="price", bar_count=period, frequency=freq)
    
    for s in context.securities:
        ema_result = talib.EMA(my_stock_series[s], timeperiod=period)[-1]
        # curr_price = data.history(context.securities[s], "price", bar_count=1, frequency=freq)
        curr_price = my_stock_series[s].iloc[-1]
        open_orders = get_open_orders()

        if curr_price > ema_result:
            if s not in open_orders:
                order_target_percent(s, 1.0)

        elif curr_price < ema_result:
            if s not in open_orders:
                order_target_percent(s, -1.0)
                
def is_wide(line_1, line_2):
    mouth = abs(line_1 - line_2)
    return mouth