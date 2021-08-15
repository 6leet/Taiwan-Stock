import sheets

def checkNetProfitGrowth(sheet: sheets.Sheet): # check if profit growth better than revenue growth
    iss = sheet.getIncomeStatement()
    # print(iss)
    netProfitGrowth = (iss['8200'][sheet.cycd] - iss['8200'][sheet.lycd]) / iss['8200'][sheet.lycd]
    revenueGrowth = (iss['4000'][sheet.cycd] - iss['4000'][sheet.lycd]) / iss['4000'][sheet.lycd]

    print('獲利成長率:', netProfitGrowth, '營收成長率', revenueGrowth)
    
    return netProfitGrowth > revenueGrowth

def checkDebtRate(sheet: sheets.Sheet): # check if debt rate is higher than a threshold
    bs = sheet.getBalanceSheet()
    debt = bs['2XXX'][sheet.cycs]
    asset = bs['1XXX'][sheet.cycs]
    debtRate = debt / asset

    print('負債比:', debtRate)

    return debtRate < 0.5

def checkCurrentRatio(sheet: sheets.Sheet): # check if current ratio is healthy
    bs = sheet.getBalanceSheet()
    current_asset = bs['11XX'][sheet.cycs]
    current_debt = bs['21XX'][sheet.cycs]
    currentRatio = current_asset / current_debt

    print('流動比率:', currentRatio)

    return currentRatio > 1.5

def checkCash(sheet: sheets.Sheet): # check 現金還能用多久 (month)
    iss = sheet.getIncomeStatement()
    cfs = sheet.getCashFlowStatement()
    print(cfs['A20100'])
    print(cfs['A20200'])
    monthly_overhead = (iss['4000'][sheet.cycd] - iss['8200'][sheet.cycd] - cfs['A20100'][sheet.cyfd] - cfs['A20200'][sheet.cyfd]) / 12

    bs = sheet.getBalanceSheet()
    months = bs['1100'][sheet.cycs] / monthly_overhead

    print('現金還能撐', months, '月')

    return months > 6
