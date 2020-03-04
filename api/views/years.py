import datetime
BASE_YEAR = 2010
CURRENT_YEAR = datetime.datetime.now().year
sql = ""

for i in range(BASE_YEAR, CURRENT_YEAR+1):
    lower = datetime.datetime(i, 1, 1, 0, 0, 0, 0)
    upper = datetime.datetime(i, 12, 31, 23, 59, 59, 9999)
    print(i)
    
    # if i != CURRENT_YEAR:
    #     sql = " UNION "
    # sql += f"""
    # (SELECT YEAR(date) 
    # WHERE 
    #     {lower} >= date AND {upper} <= date 
    # LIMIT 1)"""
print(sql)