import talib

def ema_vs_ema(stock, data):
	stock_series = data.history(stock, fields="price", bar_count=200, frequency='1d')
	long_ema = talib.EMA(stock_series[-(50):], timeperiod=50)
	short_ema = talib.EMA(stock_series[-(20):], timeperiod=20)

	'''
	EMA vs EMA algorithm
	if short_ema[-1] > long_ema[-1]: BUY
	short_ema[-1] < long_ema[-1]: SELL
	'''

	return [long_ema, short_ema]

def ema_vs_closing(stock, data):
	period = 2 # getting the PREVIOUS and CURRENT status of the stock
	freq = "1d"
	stock_series = data.history(stock, fields="price", bar_count=period, frequency=freq)
	ema_result = talib.EMA(stock_series, timeperiod=period)[-1]
	curr_price = stock_series.iloc[-1]

	'''
	EMA vs PRICE algorithm
	if curr_price > ema_result: BUY
	elif curr_price < ema_result: SELL
	'''

	return [ema_result, curr_price]

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

	return [rsi_result, small, large]

def obv(stock, data):
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

	return stock_series[-1]

	return 

