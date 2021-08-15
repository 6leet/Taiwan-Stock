import mysql.connector as connector
from mysql.connector import cursor
import json

def checkDBExist(co_id, year, season, sheet_name):
    connection = connector.connect(host='localhost', database='taiwan_stock', user='root')
    if connection.is_connected():
        cursor = connection.cursor()
        # print(sheet_name)
        sql = 'select * from ' + sheet_name + ' where co_id=' + str(co_id) + ' and year=' + str(year) + ' and season=' + str(season) + ';'
        print(sql)
        cursor.execute(sql)

        results = []
        for (co_id, year, season, result) in cursor:
            results.append(result)

        cursor.close()
        connection.close()

        if len(results) == 0:
            return None
        else:
            return json.loads(results[0])

def writetoDB(co_id, year, season, sheet_name, result):
    connection = connector.connect(host='localhost', database='taiwan_stock', user='root')
    if connection.is_connected():
        cursor = connection.cursor()
        sql = 'insert into ' + sheet_name + ' (co_id, year, season, result) values (%s, %s, %s, %s);'
        print(sql)
        json_obj = json.dumps(result)
        data = (str(co_id), str(year), str(season), json_obj)
        cursor.execute(sql, data)

        connection.commit()
        cursor.close()
        connection.close()