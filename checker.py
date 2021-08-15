import sheets
import utils

def netProfitGrowth(sheet: sheets.Sheet): # 淨利成長率
    iss = sheet.getIncomeStatement()
    netProfitGrowth = (iss['8200'][sheet.cycd] - iss['8200'][sheet.lycd]) / iss['8200'][sheet.lycd]
    return netProfitGrowth

def revenueGrowth(sheet: sheets.Sheet): # 營收成長率
    iss = sheet.getIncomeStatement()
    revenueGrowth = (iss['4000'][sheet.cycd] - iss['4000'][sheet.lycd]) / iss['4000'][sheet.lycd]
    return revenueGrowth

def debtRate(sheet: sheets.Sheet): # 負債比率
    bs = sheet.getBalanceSheet()
    debt = utils.tryOrError(bs, '2XXX', sheet.cycs)
    asset = utils.tryOrError(bs, '1XXX', sheet.cycs)

    debtRate = debt / asset
    return debtRate

def currentRatio(sheet: sheets.Sheet): # 流動比率
    bs = sheet.getBalanceSheet()
    currentAsset = utils.tryOrError(bs, '11XX', sheet.cycs)
    currentDebt = utils.tryOrError(bs, '21XX', sheet.cycs)

    currentRatio = currentAsset / currentDebt
    return currentRatio
    
def cashSafetyLevel(sheet: sheets.Sheet): # 現金安全水位（月）=> 關鍵: 2個月
    iss = sheet.getIncomeStatement()
    cfs = sheet.getCashFlowStatement()
    bs = sheet.getBalanceSheet()

    monthlyDuration = sheet.season * 3

    revenue = utils.tryOrError(iss, '4000', sheet.cyfd)
    aftertax = utils.tryOrError(iss, '8200', sheet.cyfd)
    deprec = utils.tryOrZero(cfs, 'A20100', sheet.cyfd)
    amort = utils.tryOrZero(cfs, 'A20200', sheet.cyfd)
    dividend = utils.tryOrZero(cfs, 'C04500', sheet.cyfd)
    interest = utils.tryOrZero(cfs, 'C05600', sheet.cyfd)
    # 各項開銷 = (營收-稅後淨利)
    # 月花費 = (各項開銷 - 折舊費用 - 攤銷費用 （折舊攤銷不用花錢） + 發放現金股利 + 支付之利息) / 月
    monthlyOverhead = (revenue - aftertax - deprec - amort + dividend + interest) / monthlyDuration

    cash = utils.tryOrError(bs, '1100', sheet.cycs)
    cashSafetyLevel = cash / monthlyOverhead
    return cashSafetyLevel

def daysSalesOutstanding(sheet: sheets.Sheet): # 應收帳款週轉天數 => 關鍵: 2個月內佳、不宜超過3個月
    bs = sheet.getBalanceSheet()
    iss = sheet.getIncomeStatement()

    days = sheet.season * 3 * 30

    noteRec = utils.tryOrZero(bs, '1150', sheet.cycs)
    accRec = utils.tryOrZero(bs, '1170', sheet.cycs)
    accRecAff = utils.tryOrZero(bs, '1180', sheet.cycs)
    rec = noteRec + accRec + accRecAff

    revenue = utils.tryOrError(iss, '4000', sheet.cyfd)
    daysSalesOutstanding = rec / revenue * days
    return daysSalesOutstanding

def daysInventoryOutstanding(sheet: sheets.Sheet): # 存貨週轉天數 => 關鍵: 1-2個月合理，高於2個月經營力度有問題，低於1個月除非特殊行業或理由，否則有作假帳之嫌
    bs = sheet.getBalanceSheet()
    iss = sheet.getIncomeStatement()

    days = sheet.season * 3 * 30

    inventory = utils.tryOrError(bs, '130X', sheet.cycs)
    operCost = utils.tryOrError(iss, '5000', sheet.cyfd)

    daysInventoryOutstanding = inventory / operCost * days
    return daysInventoryOutstanding
