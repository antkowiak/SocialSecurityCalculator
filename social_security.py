#
# This Python script will calculate your expected retirement benefits
# from Social Security given your annual earnings. This script does
# not extrapolate potential future earnings. It only uses the income
# information provided into the EarningsRecord dictionary below.
#
# Inputs:
#           1) EarningsRecord -
#               Dictionary mapping a year to the amount of Social
#               Security eligible earnings in that particular year
#
#           2) NationalAverageWageIndexSeries -
#               Data pulled directly from the Social Security website for the
#               national average wage data
#
#
# Written by Ryan Antkowiak 2017-07-15
# Copyright (c) 2017 All Rights Reserved
#

# Import modules
from datetime import datetime
from math import floor
import xml.etree.ElementTree as et

# Earnings history by year.
# You can find out the information by logging into "my Social Security" at
# https://www.ssa.gov
# and navigating to your earnings record at
# https://secure.ssa.gov/OSSS/er/er001View.do
# Add 2016 - 2019 earning data from https://www.ssa.gov/oact/cola/AWI.html#Series

EarningsRecord = {
    1998 :      0.0,
    1999 :      0.0,
    2000 :      0.0,
    2001 :      0.0,
    2002 :      0.0,
    2003 :      0.0,
    2004 :      0.0,
    2005 :      0.0,
    2006 :      0.0,
    2007 :      0.0,
    2008 :      0.0,
    2009 :      0.0,
    2010 :      0.0,
    2011 :      0.0,
    2012 :      0.0,
    2013 :      0.0,
    2014 :      0.0,
    2015 :      0.0,
    2016 :      0.0,
    2017 :      0.0,
    2018 :      0.0,
    2019 :      0.0,
    2020 :      0.0,
    2021 :      0.0,
    2022 :      0.0,
    2023 :      0.0,
    2024 :      0.0,
}

try:
    namespaces = {'osss': 'http://ssa.gov/osss/schemas/2.0'}
    xtree = et.parse("Your_Social_Security_Statement_Data.xml")
    xroot = xtree.getroot()
    EarningsRecord.clear()

    for node in xroot.findall('osss:EarningsRecord/osss:Earnings', namespaces):
        EarningsRecord[int(node.attrib.get("startYear"))] = float( node.find("osss:FicaEarnings", namespaces).text)
except:
    print ("XML file was not found!")

# National Average Wage Index (NAWI) data as defined by:
# https://www.ssa.gov/oact/cola/AWI.html
#
NationalAverageWageIndexSeries = {
    1951 :  2799.16,   1952 :  2973.32,   1953 :  3139.44,   1954 :  3155.64,   1955 :  3301.44,
    1956 :  3532.36,   1957 :  3641.72,   1958 :  3673.80,   1959 :  3855.80,   1960 :  4007.12,
    1961 :  4086.76,   1962 :  4291.40,   1963 :  4396.64,   1964 :  4576.32,   1965 :  4658.72,
    1966 :  4938.36,   1967 :  5213.44,   1968 :  5571.76,   1969 :  5893.76,   1970 :  6186.24,
    1971 :  6497.08,   1972 :  7133.80,   1973 :  7580.16,   1974 :  8030.76,   1975 :  8630.92,
    1976 :  9226.48,   1977 :  9779.44,   1978 : 10556.03,   1979 : 11479.46,   1980 : 12513.46,
    1981 : 13773.10,   1982 : 14531.34,   1983 : 15239.24,   1984 : 16135.07,   1985 : 16822.51,
    1986 : 17321.82,   1987 : 18426.51,   1988 : 19334.04,   1989 : 20099.55,   1990 : 21027.98,
    1991 : 21811.60,   1992 : 22935.42,   1993 : 23132.67,   1994 : 23753.53,   1995 : 24705.66,
    1996 : 25913.90,   1997 : 27426.00,   1998 : 28861.44,   1999 : 30469.84,   2000 : 32154.82,
    2001 : 32921.92,   2002 : 33252.09,   2003 : 34064.95,   2004 : 35648.55,   2005 : 36952.94,
    2006 : 38651.41,   2007 : 40405.48,   2008 : 41334.97,   2009 : 40711.61,   2010 : 41673.83,
    2011 : 42979.61,   2012 : 44321.67,   2013 : 44888.16,   2014 : 46481.52,   2015 : 48098.63,
    2016 : 48642.15,   2017 : 50321.89,   2018 : 52145.80,   2019 : 54099.99,   2020 : 55628.60,
    2021 : 60575.07,   2022 : 63795.13,
}

# The first year with Social Security Earnings
EarningsRecord_FirstYear = min(EarningsRecord, key=int)

# The last year with Social Security Earnings
EarningsRecord_LastYear = max(EarningsRecord, key=int)

# The first year of NAWI data
NationalAverageWageIndexSeries_FirstYear = min(NationalAverageWageIndexSeries, key=int)

# The last year of NAWI data
NationalAverageWageIndexSeries_LastYear = max(NationalAverageWageIndexSeries, key=int)

# Dictionary to hold the Average Wage Index (AWI) adjustment by year
AWI_Factors = {}

# Keep track of the last year for which an AWI adjustment factor is calculated
Last_AWI_Year = NationalAverageWageIndexSeries_FirstYear

# Calculate the AWI adjustment factor for each year that we have data
for i in range(NationalAverageWageIndexSeries_FirstYear, NationalAverageWageIndexSeries_LastYear) :
    AWI_Factors[i] = 1 + ( (NationalAverageWageIndexSeries[NationalAverageWageIndexSeries_LastYear] - NationalAverageWageIndexSeries[i]) / NationalAverageWageIndexSeries[i])
    Last_AWI_Year = i

# If we don't have data for the most recent years, just pad out the adjustment
# factor to be "1.0" up until the last year with earnings
for i in range(Last_AWI_Year + 1, EarningsRecord_LastYear + 1) :
    AWI_Factors[i] = 1.0

# Dictionary to hold the amount of annual adjusted earnings (as adjusted by the
# AWI factors in each year) per year
AdjustedEarnings = {}

# Calculate the amount of the adjusted earnings for each year by multiplying
# the earnings in each year by the AWI adjustment factor for that specific year
for i in range(EarningsRecord_FirstYear, EarningsRecord_LastYear + 1) :
    AdjustedEarnings[i] = EarningsRecord[i] * AWI_Factors[i]

# Auxiliary helper function that will return the key of a dictionary that
# corresponds to the maximum value in the dictionary. This will be used when
# calculating the top 35 years of earnings history.
def KeyWithMaxVal(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]

# Variable to hold the accumulation of the top 35 years of adjusted annual
# earnings
Top35YearsEarnings = 0.0;

# Accumulate the top 35 years of adjusted earnings
for i in range(0, 35):
    if AdjustedEarnings:
        top_year = KeyWithMaxVal(AdjustedEarnings)
        Top35YearsEarnings += AdjustedEarnings[top_year]
        del AdjustedEarnings[top_year]

# Calculate the Average Indexed Monthly earnings (AIME) by dividing the Top 35
# years of earnings by the number of months in 35 years (35 * 12 = 420)
AIME = Top35YearsEarnings / 420.0

# Calculate the Social Security "Bend Points" for the Primary Insurance Amount
# (PIA) as defined by:
# https://www.ssa.gov/oact/cola/piaformula.html
#
FirstBendPoint = round(180.0 * NationalAverageWageIndexSeries[NationalAverageWageIndexSeries_LastYear] / 9779.44)
SecondBendPoint = round(1085.0 * NationalAverageWageIndexSeries[NationalAverageWageIndexSeries_LastYear] / 9779.44)

# Variable to hold the normal monthly benefit amount
NormalMonthlyBenefit = 0.0;

# If the calculated AIME is below the first bend point
if AIME <= FirstBendPoint:
    NormalMonthlyBenefit = 0.9 * AIME
# Otherwise, if the AIME is between the two bend points
elif AIME > FirstBendPoint and AIME <= SecondBendPoint:
    NormalMonthlyBenefit = (0.9 * FirstBendPoint) + ( 0.32 * (AIME - FirstBendPoint) )
# Otherwise if the AIME is beyond the second bend point
else:
    NormalMonthlyBenefit = (0.9 * FirstBendPoint) + ( 0.32 * (SecondBendPoint - FirstBendPoint) ) + ( 0.15 * (AIME - SecondBendPoint) )

# The monthly benefit amount is rounded down to the nearest 0.10
NormalMonthlyBenefit = (floor(NormalMonthlyBenefit * 10.0)) / 10.0

# Calculate the reduced monthly benefit. Note that this takes into account the
# worst case scenario (70%). Depending on your birth date and how early you
# begin drawing Social Security, this number may be different.
ReducedMonthlyBenefit = 0.7 * NormalMonthlyBenefit
ReducedMonthlyBenefit = (floor(ReducedMonthlyBenefit * 10.0)) / 10.0

# Print the results
print ("Top 35 Years of Adjusted Earnings _________" + "{:11.2f}".format(Top35YearsEarnings))
print ("Average Indexed Monthly Earnings (AIME) ___" + "{:11.2f}".format(AIME))
print ("First Bend Point __________________________" + "{:11.2f}".format(FirstBendPoint))
print ("Second Bend Point _________________________" + "{:11.2f}".format(SecondBendPoint))
print ("Normal Monthly Benefit ____________________" + "{:11.2f}".format(NormalMonthlyBenefit))
print ("Normal Annual Benefit _____________________" + "{:11.2f}".format(NormalMonthlyBenefit * 12.0))
print ("Reduced (70%) Monthly Benefit _____________" + "{:11.2f}".format(ReducedMonthlyBenefit))
print ("Reduced (70%) Annual Benefit ______________" + "{:11.2f}".format(ReducedMonthlyBenefit * 12.0))


