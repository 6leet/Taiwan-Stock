from random import seed
import sheets
import utils

def totalAsset(sheet: sheets.Sheet): # 總資產
    bs = sheet.getBalanceSheet()

    totalAsset = utils.tryOrError(bs, '1XXX', sheet.cycs)
    return totalAsset

def intangibleAssetRate(sheet: sheets.Sheet): # 無形資產比例
    bs = sheet.getBalanceSheet()

    totalAsset = utils.tryOrError(bs, '1XXX', sheet.cycs)
    intanAsset = utils.tryOrZero(bs, '1780', sheet.cycs)

    intangibleAssetRate = intanAsset / totalAsset
    return intangibleAssetRate

def idleAssetRate(sheet: sheets.Sheet):
    # 閒置資產比例
    # 1780: 無形資產、1920: 存出保證金、1460: 待出售非流動資產(或處分群組)淨額、1760: 投資性不動產淨額、1840: 遞延所得稅資產
    # <5%
    bs = sheet.getBalanceSheet()

    totalAsset = utils.tryOrError(bs, '1XXX', sheet.cycs)
    intanAsset = utils.tryOrZero(bs, '1780', sheet.cycs)
    refundDep = utils.tryOrZero(bs, '1920', sheet.cycs)
    noncurAssetForSale = utils.tryOrZero(bs, '1460', sheet.cycs)
    investProp = utils.tryOrZero(bs, '1760', sheet.cycs)
    deferTaxAsset = utils.tryOrZero(bs, '1840', sheet.cycs)

    idleAsset = intanAsset + refundDep + noncurAssetForSale + investProp + deferTaxAsset
    idleAssetRate = idleAsset / totalAsset
    return idleAssetRate


def netProfitGrowth(sheet: sheets.Sheet): # 淨利成長率
    iss = sheet.getIncomeStatement()

    netProfitGrowth = (iss['8200'][sheet.cycd] - iss['8200'][sheet.lycd]) / iss['8200'][sheet.lycd]
    return netProfitGrowth

def revenueGrowth(sheet: sheets.Sheet): # 營收成長率
    iss = sheet.getIncomeStatement()

    revenueGrowth = (iss['4000'][sheet.cycd] - iss['4000'][sheet.lycd]) / iss['4000'][sheet.lycd]
    return revenueGrowth

def debtRate(sheet: sheets.Sheet): # 負債比例
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

# 負債比高的話，要看流動負債確認有沒有還款壓力，還款壓力: 公司債 > 應付票據 > 銀行借款 > 應付員工 > 應付帳款/費用 > 其他

def bankLoanRatio(sheet: sheets.Sheet): # 銀行借款（流動比） = 2100: 短期借款、2322: 一年或一營業週期內到期之銀行長期借款、2150: 應付票據（大部分是銀行）
    bs = sheet.getBalanceSheet()

    currentAsset = utils.tryOrError(bs, '11XX', sheet.cycs)
    shortLoan = utils.tryOrZero(bs, '2100', sheet.cycs)
    oneYearLongLoan = utils.tryOrZero(bs, '2322', sheet.cycs)
    notePay = utils.tryOrZero(bs, '2150', sheet.cycs)

    bankLoan = shortLoan + oneYearLongLoan + notePay
    bankLoanRatio = bankLoan / currentAsset
    return bankLoanRatio

def corporateBondRatio(sheet: sheets.Sheet): # 公司債（流動比） = 2321: 一年或一營業週期內到期或執行賣回權公司債，發現有公司債且負債比、流動比不佳就撤
    bs = sheet.getBalanceSheet()

    currentAsset = utils.tryOrError(bs, '11XX', sheet.cycs)
    corporateBond = utils.tryOrZero(bs, '2321', sheet.cycs)

    corporateBondRatio = corporateBond / currentAsset
    return corporateBondRatio


