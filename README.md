# USTreasuryCurve
This code pulls all the available nominal and real yield curves from the US Treasury's website into a Pandas dataframe. The nominal rates start on January 2, 1990 and the real rates begin on January 2, 2003. The US Treasury updates these yields daily.

#Pull in nominal US Treasury curve

ustcurve = ustcurve.nominalRates()

#Pull in real US Treasury curve

ustrcurve = ustcurve.realRates()
