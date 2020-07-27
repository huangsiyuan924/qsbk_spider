'''
-*- coding: utf-8 -*-
@Author  : Haxp
@Time    : 27/07/2020 8:22 PM
@Software: PyCharm
@File    : MysqlUtil.py
@Email   : huangsiyuan924@gmail.com
'''
import json

import pymysql





class MysqlHelper():

    def __init__(self):
        # 连接MySQL
        self.db = pymysql.connect("localhost", "root", "asdasdasd", "test")
        # 创建cursor对象
        self.cursor = self.db.cursor()

        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS qsbk(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        title VARCHAR(150) NOT NULL,
                        author VARCHAR(30) NOT NULL,
                        content TEXT NOT NULL,
                        stats_time DATETIME NOT NULL,
                        heat INT NOT NULL,
                        good_comments_list BLOB,
                        comments_list BLOB
                        )
        ''')

    def insert_qsbk(self, title, author, content, stats_time,heat, good_comments_list, comments_list):
        sql = "INSERT INTO qsbk(title, author, content, stats_time,heat, good_comments_list, comments_list) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (title, author, content, stats_time, heat, good_comments_list , comments_list)
        self.cursor.execute(sql)
        self.db.commit()
    def close(self):
        self.db.close()




def test():
    helper = MysqlHelper()
    helper.cursor.execute("SELECT comments_list FROM qsbk")
    mydata = helper.cursor.fetchall()
    for i in range(len(mydata)):
        datas = json.loads(mydata[i][0], encoding='utf-8', strict=False)
        for data in datas:
            print(data[0] + ": " + data[1])
        print("*" * 40)
if __name__ == '__main__':
    test()
