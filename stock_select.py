import sheets
import filter

co_id = 2382
year = 2021
season = 1
# result = getBalanceSheet(co_id, year, season)
sheet = sheets.Sheet(co_id, year, season)

filter.checkNetProfitGrowth(sheet)
filter.checkDebtRate(sheet)
filter.checkCurrentRatio(sheet)
filter.checkCash(sheet)


    