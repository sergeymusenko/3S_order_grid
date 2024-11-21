#!/usr/bin/env python3
"""\
grid.py - Build Limit Order Grid for 3S Crypto Trading Strategy.
Print results. Return Orders Dictionary.

Спасибо каналу 'Не Наблюдатель'! Смотри https://www.youtube.com/watch?v=tODWA2E27uE
"БЕСПРОИГРЫШНАЯ СТРАТЕГИЯ 2024 ДЛЯ ФЬЮЧЕРСОВ"
	3S strategy:		это сделает сетку
		сетка		4        0%	 6.67%
		перекрытие	16%      4%	13.34%
		мартингейл	100%    10%	26.68%
		логарифм	1.2     16%	53.31%
"""


__project__  = "Build Limit Order Grid for 3S Crypto Trading Strategy"
__part__     = 'Grid module'
__author__   = "Sergey V Musenko"
__email__    = "sergey@musenko.com"
__copyright__= "© 2024, musenko.com"
__license__  = "MIT"
__credits__  = ["Sergey Musenko"]
__date__     = "2024-10-09"
__version__  = "0.1"
__status__   = "dev"


import math
from termcolor import colored


def getGrid(symbol, marginAmount, marginInCont, startPrice, direction, orders, overlap, martingale=1, logarithm=1, firstOrdAmnt=0, printout=True):
	# prepare parameters
	marginAmount = float(marginAmount)
	marginInCont = bool(marginInCont)
	startPrice = float(startPrice)
	direction = -1 if direction < 0  else 1
	dirColor = 'light_red' if direction < 0 else 'light_green'
	dirText = 'SHORT' if direction < 0  else 'LONG'
	dirSign = 1 if direction < 0 else -1 # LONG position needs SHORT grid
	orders = int(orders)
	orders = orders if orders >= 2 else 2
	overlap = float(overlap)
	martingale = abs(float(martingale))
	logarithm = abs(float(logarithm))
	logarithm = logarithm if logarithm >= 0.1 and logarithm <= 2.9 else 1
	firstOrdAmnt = float(firstOrdAmnt)
	amountRound = 0 if marginInCont else 4 # int if Amount in Contracts

	# print settings
	if printout:
		print(f"{colored('3S', 'light_green')} strategy for {colored(symbol, 'light_yellow')} " + colored(dirText, dirColor))
		print(f"    Margin Amount: {marginAmount} {'' if not marginInCont else 'contracts'}")
		if firstOrdAmnt > 0:
			print(f"    FirstOrd Amnt: {firstOrdAmnt}, it means Margin Amount", colored("will be DIFFERENT", attrs=['underline']))
		print(f"    Start Price  : {startPrice}")
		print(f"    Orders       : {orders}")
		print(f"    Overlap      : {overlap}%")
		print(f"    Martingale   : {martingale}%")
		print(f"    Logarithm    : {logarithm}")

	# prepare the Martingale
	martingaleList = []
	martingaleCur = 100. # 1st order is 100%
	martnglTotal = 0.
	for i in range(0,orders):
		martingaleList.append(martingaleCur)
		martnglTotal += martingaleCur
		martingaleCur += martingaleCur * martingale / 100
	if martingale < 0: # for negative Martingale, but we do not use it yet...
		martingaleList.reverse()

	# prepare logarithmic price levels
	priceLevels = []
	endPrice = startPrice * (1 + dirSign * overlap / 100)
	startLog = math.log10(startPrice)
	endLog = math.log10(endPrice)
	normalized_indices = [(i / (orders - 1)) ** logarithm for i in range(orders)]
	priceLevels = [math.pow(10, startLog + i * (endLog - startLog)) for i in normalized_indices]

	# fill the Grid
	Grid = {}
	amountLen = 0 # get longest amount string
	positionsSymbol = 0 # total in Symbol
	positionsUSDT = 0 # total in USDT
	firstOrdAmntWeight = firstOrdAmnt / martingaleList[0] # will use it to calc amount from martingaleList
	for i in range(0,orders):
		# price with logarithm
		price = priceLevels[i]
		pricePercent = dirSign * abs(100 * (startPrice - price) / startPrice)
		# recalc order amounts to minOrdAmount
		# order amount with Martingale
		if firstOrdAmnt: # calculation based on First Order Amount and Martingale
			amount = round(firstOrdAmntWeight * martingaleList[i], amountRound)
			amountPercent = 100 * martingaleList[i] / martnglTotal
		else: # calculation based on total Margin Amount and Martingale
			amount = round(marginAmount * martingaleList[i] / martnglTotal, amountRound)
			amountPercent = 100 * amount / marginAmount
		amountLen = amountLen if len(str(amount)) < amountLen else len(str(amount)) 
		# position price
		positionsUSDT += amount # total in USDT
		positionsSymbol += amount * price # total in Symbol
		Grid[i] = {
			'price': price, # float
			'pricePercent': pricePercent, # float
			'amount': amount, # float
			'amountPercent': amountPercent, # float
			'positionPrice': positionsSymbol / positionsUSDT, # float, average Position Price
		}

	# print out orders
	if printout:
		print(colored("Grid", 'light_green') + ':')
		priceLen = 1 + len(str(startPrice))
		priceDec = 1 + len(str(startPrice).split('.')[1])
		checkPercenttotal = 0
		for i in Grid:
			order = Grid[i]
			orderPrice = colored(f"{order['price']:{priceLen}.0{priceDec}f}", 'light_yellow')
			orderAmount = colored(f"{order['amount']:{amountLen}.0{amountRound}f}", 'light_yellow')
			pricePercentStr = f"({order['pricePercent']:.01f}%),"
			amountPercent = order['amountPercent']
			# checkPercenttotal += amountPercent
			positionPrice = colored(f"{order['positionPrice']:{priceLen}.0{priceDec}f}", 'light_yellow')
			print(f"    Order#{i}: price {orderPrice} {pricePercentStr:9} amount {orderAmount} ({amountPercent:4.01f}%), position price {positionPrice}")
		if firstOrdAmnt:
			print(f"    Margin Amount is {colored(f'{positionsUSDT}', 'light_yellow')} because of First Order Amount is {firstOrdAmnt}")
		if checkPercenttotal:
			print(f"check total amount percent: {checkPercenttotal}")

	return Grid


if __name__ == '__main__':
	print(f'{__project__}\n{__part__} testing:')

	# testing:
	symbol		= 'BTCUSDT' # just for info
	startPrice	= 75000		# start at price
	marginAmount= 1000	# amount in Symbol or USDT
	marginInCont= 0		# True means amount in Contracts, not Coins/USDT
	direction	= 1		# -1='SHORT', 1="LONG"
	orders		= 4		# number of orders in grid, must be >=2, there is no sense for >=10
	overlap		= 16	# cover % from start price
	martingale	= 100	# % Martingale, 0 means NO
	logarithm	= 1.6	# price offset is logarithmic, 1 means NOT, must be >=0.1 and <=2.9
	firstOrdAmnt= 0		# calc grid starting with this 1st order, total Margin Amount will be different!

	# call getGrid()
	getGrid(symbol, marginAmount, marginInCont, startPrice, direction, orders, overlap, martingale, logarithm, firstOrdAmnt)
	# that's all folks!
