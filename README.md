# USTreasuryCurve
This code pulls in the nominal and real yield curves from the US Treasury's website for a date range (inclusive) into a Pandas dataframe. The nominal rates start on January 2, 1990 and the real rates begin on January 2, 2003. The US Treasury updates these yields daily.

# Install package
pip install ustreasurycurve

# Usage
import ustreasurycurve as ustcurve

# Pull in nominal US Treasury curve
ustcurve = ustcurve.nominalRates('2010-06-30', '2022-06-30')

# Pull in real US Treasury curve
ustrcurve = ustcurve.realRates('2010-06-30', '2022-06-30')
