# 2019-
import sheets
import checker

co_id = 2330
year = 2021
season = 2
sheet = sheets.Sheet(co_id, year, season)

print(checker.totalAsset(sheet))
print(checker.intangibleAssetRate(sheet))
print(checker.idleAssetRate(sheet))
# print(checker.operatingProfit(sheet))
# print(checker.profitBeforeTax(sheet))
print(checker.operatingProfitProportion(sheet))
print(checker.netProfitGrowth(sheet))
print(checker.revenueGrowth(sheet))
print(checker.sellingExpense(sheet))
print(checker.sellingExpenseGrowth(sheet))
print(checker.rdExpense(sheet))
print(checker.rdExpenseGrowth(sheet))
print(checker.administrativeExpense(sheet))
print(checker.grossMargin(sheet))
print(checker.debtRate(sheet))
print(checker.currentRatio(sheet))
print(checker.cashSafetyLevel(sheet))
print(checker.daysSalesOutstanding(sheet))
print(checker.daysInventoryOutstanding(sheet))
print(checker.bankLoanRatio(sheet))
print(checker.corporateBondRatio(sheet))
print(checker.EPS(sheet))
print(checker.annualizedROE(sheet))