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
    context.small = 30
    context.large = 70
    context.bar_interval = '1d'
    context.bar_count = 200
    
    schedule_function(rebalance,date_rules.every_day(), time_rules.market_open(minutes=30))

def rebalance(context, data):
    period = 14
    stock_series = data.history(context.securities, 'price', context.bar_count, context.bar_interval)
    
    open_orders = get_open_orders()
    
    for s in context.securities:
        rsi = talib.RSI(stock_series[s], timeperiod=period)
        rsi_result = rsi[-1]
        
        if rsi_result <= context.small:
            if s not in open_orders:
                order_target_percent(s, -1.0)
                
        elif rsi_result >= context.large:
            if s not in open_orders:
                order_target_percent(s, 1.0)