import xosd
from time import sleep

osd = xosd.XOSD(2)
osd.font = "-adobe-helvetica-bold-r-normal-*-*-320-*-*-p-*-*"
osd.colour = "red"
print 'Color as (r, g, b):', osd.colour
osd.display(0, xosd.string, "Hey there.")
osd.display(1, xosd.percentage, 30)
sleep(4)
