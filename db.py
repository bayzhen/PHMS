import pymysql, os


# os:为系统模块，目的为正常退出
# __init__ : 初始化属性
# __del__ : 销毁对象时，自动执行该方法
# __new__ : 实例化对象(创建一个对象)
class connmysql(object):
    obj = None  # 对象第一次为None

    def __new__(cls, *args, **kwargs):  # 单例模式
        if cls.obj is None:  # 如果对象为None
            cls.obj = super().__new__(cls)  # 就创建一个对象

        return cls.obj  # 否则直接返回

    def __init__(self, user, password, database, host="127.0.0.1", port=3306):
        # 1. 链接数据库， 得到一个对象
        try:
            self.db = pymysql.connect(
                host=host, port=port, user=user,  # 第一种
                password=password, database=database, charset="utf8"
            )
        except Ellipsis as e:
            print(e)
            os._exit(0)  # 如果第一步的链接失败，下面的所有代码都不用走，直接退出

        self.cs = self.db.cursor()  # 2.得到一个游标对象

    def select(self, sql):
        """负责查询功能"""
        # 3 执行SQL语句
        try:

            self.cs.execute(sql)
        except Exception as e:
            print(e)
            return
        # 4.获取查询结果
        r = self.cs.fetchall()
        return r  # 将结果返回

    def update(self, sql):
        """负责更行功能"""
        # 3 利用游标对象执行SQL语句
        try:
            self.cs.execute(sql)
        except Exception as e:
            print(e)
            return
        # 4.提交 如果不进行提交，所有的改变(insert, delete, update)不会生效
        self.db.commit()
        print("更新成功！")

    def __del__(self):
        self.cs.close()  # 5. 关闭链接
        self.db.close()

# DB=connmysql(user="root",password="adsl12",database="assignment2")
#
# sql1="select id,place from data2;"
# list=DB.select(sql1)
# for item in list:
#     distance=item[1].split('km')[0]
#     if(len(distance)>3):
#         distance=0
#     else:
#         distance=float(distance)
#     print(distance)
#     sql="UPDATE data2 SET distance=%f where id='%s';"%(distance,item[0])
#     DB.update(sql)

# var child="<tr><td>"+(i+1)+"</td><td>"+data[i][6]+"</td><td>"+data[i][2]+"</td><td>"+data[i][3]+"</td>"+"<td>"+"<button type='button' value="+data[i][5]+" onclick='selectByid(this)' class='btn btn-primary' data-toggle='modal' data-target='#myModal2' >edit</button>"+"</td>"+"</tr>";
