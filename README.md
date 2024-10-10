# 3S_order_grid
**Build Limit Order Grid for 3S Crypto Trading Strategy. Fill Python Dictionary, print results.**<br>
https://github.com/sergeymusenko/3S_order_grid

Thanks to Youtube chanel NN "Не Наблюдатель"!<br>
About 3S Strategy see: https://www.youtube.com/watch?v=tODWA2E27uE

For your Order Grid you can set Start Price, Order Direction (-1=SHORT, 1=LONG), Price Overlap (spread, in %), Number
of Orders and Total Margin for position.
Also you can set Martingale in % and Logarithmic Coefficient for orders price offset.

You can just print results in console or use this code as a module to get the order grid as a Dictionary
then you can use it to set limit orders at real Crypto Exchange (may be will done with next version).

Small note about SHORT/LONG. This is a DCA strategy so if you plan to open LONG position
you need "SHORT" price grid and you gains a position while price goes down. And vice versa
for SHORT position you need "LONG" price grid. Using DCA strategy it's high probably you will not hit a Stop Loss (though it is better to set it beyond the Overlap range).

Have a good profit!


**Results printout examples:<br/>**
<img src="screenshot0.png" alt="Results printout example"><br>
<img src="screenshot1.png" alt="Results printout example"><br>
<img src="screenshot2.png" alt="Results printout example">
