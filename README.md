# USTreasuryCurve
This code pulls in all available nominal and real yield curves from the US Treasury's website into a Pandas dataframe. You can specify a start and/or end date if you want. The nominal rates start on January 2, 1990 and the real rates begin on January 2, 2003. The US Treasury updates these yields daily. 

# Install package
pip install ustreasurycurve

# Usage
import ustreasurycurve as ustcurve

# Pull in all available US Treasury curve data
ustcurve = ustcurve.nominalRates()

# Pull in nominal US Treasury curve between two dates
ustcurve = ustcurve.nominalRates('2010-06-30', '2022-06-30')

# Pull in real US Treasury curve starting at a date
ustrcurve = ustcurve.realRates('2010-06-30')


