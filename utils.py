import pickle

def tryOrError(map: dict, key: str, timeinfo: str):
    return map[key][timeinfo]

def tryOrZero(map: dict, key: str, timeinfo: str):
    if key in map:
        return map[key][timeinfo]
    else:
        print("no key: " + key)
        return 0

def checkPageExist(soup):
    find = soup.find('font')
    if find == None:
        return True
    elif find.text == '檔案不存在!':
        return False
    return True

def parseSheet(soup, sheet_name):
    # get known account id
    with open(sheet_name + "_known_id.txt", "rb") as fp:  # Unpickling
        idlist = pickle.load(fp)
    fp.close()

    if sheet_name == 'balancesheet':
        sheet = soup.find('div', id='BalanceSheet').find_next_sibling().find_next_sibling()
    elif sheet_name == 'incomestatement':
        sheet = soup.find('div', id='StatementOfComprehensiveIncome').find_next_sibling().find_next_sibling()
    elif sheet_name == 'cashflowstatement':
        sheet = soup.find('div', id='StatementsOfCashFlows').find_next_sibling().find_next_sibling()

    sheet_dict = {}
    for field in sheet.find_all('tr'):
        account_id = ''
        account_name = ''
        # get each field's data
        for data in field.findChildren('td', recursive=False):
            # account_id
            if data.has_attr('style'):
                account_id = data.text
                sheet_dict[account_id] = {}

            # year value x ?, can be done better
            # MAIN DIFFERENCE
            elif data.has_attr('class'):
                _pre = data.find('pre')
                if _pre is not None:

                    _year = _pre.find_next()['contextref']
                    if len(_year) == len('FromYYYYMMDDtoYYYYMMDD'): # FromYYYYMMDDtoYYYYMMDD       
                        year = _year[4:12] + '-' + _year[14:]
                    elif len(_year) == len('AsofYYYYMMDD'): # AsofYYYYMMDD
                        year = _year[4:]
                    else:
                        year = _year

                    value = float(_pre.find_next().text.replace(',', ''))
                    sheet_dict[account_id][year] = value
            else:
                account_name = data.find_next().text.replace('\u3000', '')

        # add unknown account_id
        if account_id != '' and account_id is not None and account_id not in idlist:
            print('|', account_id, '|', account_name, '|')
            idlist.append(account_id)
        if account_id == '':
            print('|', account_id, '|', account_name, '|')

    # write unknown account_id to known
    print(idlist)
    with open(sheet_name + "_known_id.txt", "wb") as fp:  #Pickling
        pickle.dump(idlist, fp)
    fp.close()

    return sheet_dict