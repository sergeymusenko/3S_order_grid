#!/usr/bin/env python3
"""\
main.py - Build Limit Order Grid for 3S Crypto Trading Strategy.

Use modules to prepare grid and creat limit orders at Crypto Exchange
"""


__project__  = "Build Limit Order Grid for 3S Crypto Trading Strategy"
__part__     = 'Main script'
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
from grid import *


# GRID settings
symbol		= 'BTCUSDT' # just for info
startPrice	= 70000		# start at price
marginAmount= 1000	# amount in Symbol or USDT
marginInCont= 0		# True means amount in Contracts, not Coins/USDT
direction	= 1		# -1='SHORT', 1="LONG"
orders		= 4		# number of orders in grid, must be >=2, there is no sense for >=10
overlap		= 16	# cover % from start price
martingale	= 60	# % Martingale, 0 means NO
logarithm	= 1.4	# price offset is logarithmic, 1 means NOT, must be >=0.1 and <=2.9
firstOrdAmnt= 0		# calc grid starting with this 1st order, total Margin Amount will be different!


# ordering settings
printout = True # Grid will print orders

if __name__ == '__main__':
	# it returns grid as a dictionary
	Grid = getGrid(symbol, marginAmount, marginInCont, startPrice, direction, orders, overlap, martingale, logarithm, firstOrdAmnt, printout)

	# and now you can use Grid and open real Limit Orders at Exchange...
	#...

# that's all folks!
