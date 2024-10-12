#!/usr/bin/env python3
"""\
grid.py - Build Limit Order Grid for 3S Crypto Trading Strategy.
Create Limit Orders at Crypto Exchange from Order Grid as a dictionary:

Grid = {
	[int]: {'price': [flot], 'pricePercent': [flot], 'amount': [flot], 'amountPercent': [flot], 'positionPrice': [flot]}
}
"""


__project__  = "Build Limit Order Grid for 3S Crypto Trading Strategy"
__part__     = 'Order Module. OKX Exchange'
__author__   = "Sergey V Musenko"
__email__    = "sergey@musenko.com"
__copyright__= "© 2024, musenko.com"
__license__  = "MIT"
__credits__  = ["Sergey Musenko"]
__date__     = "2024-10-12"
__version__  = "0.1"
__status__   = "dev"


def makeOrders(Grid):
	False


if __name__ == '__main__':
	print(f'{__project__}\n{__part__}\nThere is no test for this module')
