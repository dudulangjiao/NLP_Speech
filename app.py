import click
import mysql.connector
from main import main
from models.other import get_sql
@click.command()
def hello():
    """使用python的click把一些建立数据表等调试中临时运行的操作放在这里"""

    # 创建一些数据表
    cnx = mysql.connector.connect(user='root', password='314159',
                                  host='localhost',
                                  database='SpeechCollection')
    cursor = cnx.cursor(dictionary=True)
    sql_dict = get_sql()  #调用get_sql函数读取sql脚本文件中的命令

    for k, v in sql_dict.items():
        cursor.execute(v)

    cursor.close()
    cnx.close()

    # 主程序命令，从项目跟目录main.py模块中引入main()
    main()

if __name__ == '__main__':
    hello()
