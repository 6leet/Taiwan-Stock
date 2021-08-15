# 2019-
import sheets
import checker

co_id = 2330
year = 2019
season = 1
sheet = sheets.Sheet(co_id, year, season)

print(checker.netProfitGrowth(sheet))
print(checker.revenueGrowth(sheet))
print(checker.debtRate(sheet))
print(checker.currentRatio(sheet))
print(checker.cashSafetyLevel(sheet))
print(checker.daysSalesOutstanding(sheet))
print(checker.daysInventoryOutstanding(sheet))