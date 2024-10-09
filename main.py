#!/usr/bin/env python3
"""\
main.py - Build Limit Order Grid for 3S Crypto Trading Strategy. Print results.

Спасибо каналу 'Не Наблюдатель'! Смотри https://www.youtube.com/watch?v=tODWA2E27uE
"БЕСПРОИГРЫШНАЯ СТРАТЕГИЯ 2024 ДЛЯ ФЬЮЧЕРСОВ"
	3S strategy:		это сделает сетку
		сетка		4        0%	 6.67%
		перекрытие	16%      4%	13.34%
		мартингейл	100%    10%	26.68%
		логарифм	1.2     16%	53.31%
"""


__project__  = "Build Limit Order Grid, print results"
__part__     = 'Main script'
__author__   = "Sergey V Musenko"
__email__    = "sergey@musenko.com"
__copyright__= "© 2024, musenko.com"
__license__  = "MIT"
__credits__  = ["Sergey Musenko"]
__date__     = "2024-10-09"
__version__  = "0.1"
__status__   = "prod"


import math
from termcolor import colored


# GRID settings
symbol		= 'SOLUSDT' # just for info
marginAmount= 100	# amount in symbol or USDT
marginInCont= True	# True means contracts, not coins
startPrice	= 140	# start here
direction	= -1	# -1 or 'SHORT' - or - +1 or "LONG"
orders		= 4		# number of orders in grid, must be >=2, there is no sense for >=10
overlap		= 16	# cover % from start price
martingale	= 100	# % Martingale, 0 means NO, can be <0
logarithm	= 1.2	# price amount logarithm, 1 means NO, must be >=0.1 and <=2.9


def getGrid(symbol, marginAmount, startPrice, direction, orders, overlap, martingale=1, logarithm=1, printout=True):
	# prepare settings
	marginAmount = float(marginAmount)
	startPrice = float(startPrice)
	direction = 'SHORT' if direction=='SHORT' or direction<0  else 'LONG'
	dirColor = 'light_red' if direction=='SHORT' else 'light_green'
	dirSign = -1 if direction=='SHORT' else 1
	orders = int(orders)
	orders = orders if orders>=2 else 2
	overlap = float(overlap)
	martingale = float(martingale)
	martingaleRev = False if martingale>=0 else True
	martingale = abs(martingale)
	logarithm = abs(float(logarithm))
	logarithm = logarithm if logarithm>=0.1 and logarithm<=2.9 else 1

	# print settings
	if printout:
		print(f"{colored('3S', 'light_green')} strategy for {colored(symbol, 'light_yellow')} " + colored(direction, dirColor))
		print(f"    Margin Amount: {marginAmount} {'' if not marginInCont else 'contracts'}")
		print(f"    Start Price  : {startPrice}")
		print(f"    Orders       : {orders}")
		print(f"    Overlap      : {overlap}%")
		print(f"    Martingale   : {martingale}%")
		print(f"    Logarithm    : {logarithm}")

	# prepare the Martingale
	martingaleList = []
	martingaleCur = 100.
	martnglTotal = 0.
	for i in range(0,orders):
		martingaleList.append(martingaleCur)
		martnglTotal += martingaleCur
		martingaleCur += martingaleCur * martingale / 100
	if martingaleRev:
		martingaleList.reverse()

	# prepare logarithm price levels
	priceLevels = []
	endPrice = startPrice * (1 + dirSign * overlap / 100)
	startLog = math.log10(startPrice)
	endLog = math.log10(endPrice)
	normalized_indices = [(i / (orders - 1)) ** logarithm for i in range(orders)]
	priceLevels = [math.pow(10, startLog + i * (endLog - startLog)) for i in normalized_indices]

	# fill the Grid
	Grid = {}
	amountRound = 0 if marginInCont else 4
	for i in range(0,orders):
		# price with logarithm
		price = priceLevels[i]
		pricePercent = dirSign * abs(100 * (startPrice - price) / startPrice)
		# order amount with Martingale
		amount = round(marginAmount * martingaleList[i] / martnglTotal, amountRound)
		amountPercent = 100 * amount / marginAmount
		Grid[i] = {
			'price': price,
			'pricePercent': pricePercent,
			'amount': amount,
			'amountPercent': amountPercent,
		}

	# print out orders
	if printout:
		print(colored("Grid:", 'light_green'))
		priceLen = 1 + len(str(startPrice))
		priceDec = 1 + len(str(startPrice).split('.')[1])
		for i in Grid:
			order = Grid[i]
			orderPrice = colored(f"{order['price']:{priceLen}.0{priceDec}f}", 'light_yellow')
			orderAmount = colored(f"{order['amount']}", 'light_yellow')
			pricePercentStr = f"({order['pricePercent']:.01f}%),"
			amountPercent = order['amountPercent']
			print(f"    Order#{i}: price {orderPrice} {pricePercentStr:9} amount {orderAmount} ({amountPercent:.01f}%)")

	return Grid


if __name__ == '__main__':
	# call function, it returns grid as dictionary
	Grid = getGrid(symbol, marginAmount, startPrice, direction, orders, overlap, martingale, logarithm)
	# and now you can use Grid and open real Limit Orders at Exchange...

# that's all folks!
