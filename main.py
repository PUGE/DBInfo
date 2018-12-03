import pymysql.cursors



# 连接数据库并获取信息
def creat(host, port, user, password):
  info = {
    "database": []
  }
  connection = pymysql.connect(host=host, port=port, user=user, password=password, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
  with connection.cursor() as cursor:
    # 取出权限信息
    cursor.execute('show grants;')
    connection.commit()
    grants = cursor.fetchall()
    # print(grants)
    info["grants"] = grants

    cursor.execute('show databases;')
    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
    connection.commit()
    dbList = cursor.fetchall()
    # 取出所有的数据库
    for item in dbList:
      systemDbList = ["information_schema", "mysql", "sys", "performance_schema"]
      dbName = item["Database"]
      if dbName not in systemDbList:
        

        # 取出所有的表信息
        cursor.execute('show table status from %s;' % dbName)
        connection.commit()
        dbList = cursor.fetchall()
        # print(dbList)
        # for item in dbList:

        dbInfo = {
          dbName: dbList
        }

        info["database"].append(dbInfo)
    connection.close()
    return info
if __name__ == '__main__':
  info = creat('115.28.108.130', 3306, "test", "123456")
  print(info)