import talib
import numpy as np

def atr(stock, data):
	hist = data.history(stock, ['high', 'low', 'close'], 30, '1d')
	atr = talib.ATR(hist['high'], hist['low'], hist['close'], timeperiod=14)[-1]

	price = data.current(stock, 'price') # current stock price
	prev_close = hist['close'][-2] # previous stock price

	upside_signal = price - (prev_close + atr)
	downside_signal = prev_close - (price + atr)

	'''
	ATR ALGORITHM
	if upside_signal > 0: BUY
	elif downside_signal > 0: SELL
	'''

	return [upside_signal, downside_signal]

def stoch(stock, data):
	hist = data.history(stock, ['high', 'low', 'close'], 30, '1d')
	slowk, slowd = talib.STOCH(hist['high'], hist['low'], hist['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

	# get the most recent value
	slowk = slowk[-1]
	slowd = slowd[-1]

	'''
	if slowk < 10 or slowd < 10: BUY
	elif slowk > 90 or slowd > 90: SELL
	'''

	return [slowk, slowd]

def bollinger_bands(stock, data):
	stock_series = data.history(stock, fields="price", bar_count=200, frequency='1d')
	middle_band = stock_series.mean()
	upper_band = middle_band + np.std(stock_series) * 2
	lower_band = middle_band - np.std(stock_series) * 2

	'''
	BOLLINGER BANDS algorithm
	if stock_series[-1] > upper_band: BUY
	elif stock_series[-1] < lower_band: SELL
	'''

	return [upper_band, lower_band]

def ema_vs_ema(stock, data):
	stock_series = data.history(stock, fields="price", bar_count=200, frequency='1d')
	long_ema = talib.EMA(stock_series[-(50):], timeperiod=50)
	short_ema = talib.EMA(stock_series[-(20):], timeperiod=20)

	'''
	EMA vs EMA algorithm
	if short_ema[-1] > long_ema[-1]: BUY
	short_ema[-1] < long_ema[-1]: SELL
	'''

	return [long_ema[-1], short_ema[-1]]

def rsi(stock, data):
	period = 14
	bar_count = 200
	bar_interval = '1d'

	# benchmark indicators in order to buy / sell
	small = 30
	large = 70

	stock_series = data.history(stock, 'price', bar_count, bar_interval)
	rsi_result = talib.RSI(stock_series, timeperiod=period)[-1]

	'''
	RSI algorithm
	if rsi_result <= small: SELL
	if rsi_result >= large: BUY
	'''

	return rsi_result

def obv(stock, context, data):
	# IMPORTANT: Please set context.curr_obv = 0 in the initialize()

	period = 2 # getting the PREVIOUS and CURRENT status of the stock
	bar_interval = '1d'
	stock_series = data.history(stock, 'close', period, bar_interval)
	volume_series = data.history(stock, 'volume', period, bar_interval)

	curr_close = stock_series[-1]
	prior_close = stock_series[0]
	curr_volume = volume_series[s][-1]

	if curr_close > prior_close:
		context.curr_obv = context.curr_obv + curr_volume

	elif curr_close < prior_close:
		context.curr_obv = context.curr_obv - curr_volume

	'''
	OBV algorithm
	if context.curr_obv <= stock_series[-1]: SELL
	elif context.curr_obv >= stock_series[-1]: BUY
	'''