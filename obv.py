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
    context.bar_interval = '1d'
    context.bar_count = 2
    context.curr_obv = 0
    
    schedule_function(rebalance,
                      date_rules.every_day(),
                      time_rules.market_open(minutes=30))

def rebalance(context, data):
    stock_series = data.history(context.securities, 'close', context.bar_count, context.bar_interval)
    
    volume_series = data.history(context.securities, 'volume', context.bar_count, context.bar_interval)
    
    open_orders = get_open_orders()
    
    for s in context.securities:
        curr_close = stock_series[s][-1]
        prior_close = stock_series[s][0]
        
        curr_volume = volume_series[s][-1]
        
        if curr_close > prior_close:
            context.curr_obv = context.curr_obv + curr_volume
            
        elif curr_close < prior_close:
            context.curr_obv = context.curr_obv - curr_volume
        
        if context.curr_obv <= stock_series[s][-1]:
            if s not in open_orders:
                order_target_percent(s, -1.0)
                
        elif context.curr_obv >= stock_series[s][-1]:
            if s not in open_orders:
                order_target_percent(s, 1.0)