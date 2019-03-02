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
    context.long_ema_period = 26
    context.short_ema_period = 12
    context.bar_interval = '1d'
    context.bar_count = 200
    
    schedule_function(rebalance,
                      date_rules.every_day(),
                      time_rules.market_open(minutes=30))
    
    #schedule_function(handle_data, date_rules.every_day(), time_rules.market_close(hours=1))

def rebalance(context, data):
    macd_vs_signal(context, data)
    
def macd_vs_signal(context, data):    
    stock_series = data.history(context.securities, fields="close", bar_count=context.bar_count, frequency=context.bar_interval)
    
    for s in context.securities:
        ema26 = talib.EMA(stock_series[s], timeperiod=context.long_ema_period)
        ema12 = talib.EMA(stock_series[s], timeperiod=context.short_ema_period)
        macd = ema12 - ema26
        signal = talib.EMA(macd, 9)
        
        open_orders = get_open_orders()
        if macd[-1] < signal[-1]:
            if s not in open_orders:
                order_target_percent(s, 1)
        
        elif macd[-1] > signal[-1]:
            if s not in open_orders:
                order_target_percent(s, -1.0)
                
def ema12_vs_ema26(context, data):
    stock_series = data.history(context.securities, fields="close", bar_count=context.bar_count, frequency=context.bar_interval)
    
    for s in context.securities:
        ema26 = talib.EMA(stock_series[s], timeperiod=context.long_ema_period)
        ema12 = talib.EMA(stock_series[s], timeperiod=context.short_ema_period)
        
        open_orders = get_open_orders()
        if ema12[-1] > ema26[-1]:
            if s not in open_orders:
                order_target_percent(s, 1.0)
        
        elif ema12[-1] < ema26[-1]:
            if s not in open_orders:
                order_target_percent(s, -1.0)