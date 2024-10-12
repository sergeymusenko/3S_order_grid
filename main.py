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
symbol		= 'SOLUSDT' # just for info
startPrice	= 140	# start here
marginAmount= 1000	# amount in symbol or USDT
marginInCont= 0		# True means contracts, not coins
direction	= 1		# -1='SHORT', 1="LONG"
orders		= 4		# number of orders in grid, must be >=2, there is no sense for >=10
overlap		= 16	# cover % from start price
martingale	= 100	# % Martingale, 0 means NO, can be <0
logarithm	= 1.4	# price amount logarithm, 1 means NO, must be >=0.1 and <=2.9
minOrdAmount= 100	# calc grid starting with this, not with zero


# ordering settings
printout = True # Grid will print orders

if __name__ == '__main__':
	# it returns grid as a dictionary
	Grid = getGrid(symbol, marginAmount, marginInCont, startPrice, direction, orders, overlap, martingale, logarithm, minOrdAmount, printout)

	# and now you can use Grid and open real Limit Orders at Exchange...
	#...

# that's all folks!
