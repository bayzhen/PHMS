import os
import pymysql
from flask import Flask, render_template, request, session, jsonify
from db import connmysql
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
DB = connmysql(user="PHMS", password="123456", database="phms")
config = {'host': '101.35.143.22',
          'port': 3306,
          'user': 'PHMS',
          'password': '123456',
          'charset': 'utf8',
          'db': 'phms',
          'autocommit': True
          }


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/register_D')
@app.route('/page1')
def page1():
    return render_template("register_doctor.html")


@app.route('/register_P/')
@app.route('/page2')
def page2():
    return render_template("register_patient.html")


@app.route('/login/', methods=["POST"])
def login():
    username = request.values.get('username')
    password = request.values.get('password')
    identity = request.values.get('type')

    sql = "select * from %s where username='%s' and password='%s';" % (identity, username, password)
    count_select = DB.select(sql)
    if (count_select):
        session['username'] = username
        session['password'] = password
        session['identity'] = identity
        # 根据身份 跳转不同页面
        if (identity == 'patient'):
            return render_template("PersonalHome.html", username=username)
        elif (identity == 'doctor'):
            return render_template("DoctorHome.html", username=username)
    else:
        return render_template("index.html", message='Username or Password Error')


@app.route('/register_patient/', methods=["POST"])
def register():
    username = request.values.get('username')
    password = request.values.get('password')
    name = request.values.get('name')
    gender = request.values.get('sex')
    height = request.values.get('height')
    weight = request.values.get('weight')
    age = request.values.get('age')
    phoneNum = request.values.get('phone')
    job = request.values.get('job')
    email = request.values.get('email')

    sql = "insert into patient(username,password,name,gender,height,weight,age,phoneNum,job,email) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (
        username, password, name, gender, height, weight, age, phoneNum, job, email)
    count_select = DB.update(sql)
    return jsonify('OK')


@app.route('/is_exist/', methods=["POST"])
def is_exist():
    username = request.values.get('username')
    sql = "select * from patient where username='%s';" % (username)
    count_select = DB.select(sql)
    valid = ''
    if (len(count_select) == 0):
        valid = True
    else:
        valid = False
    return jsonify({"valid": valid})


@app.route('/is_exist_doctor/', methods=["POST"])
def is_exist_doctor():
    username = request.values.get('username')
    sql = "select * from doctor where username='%s';" % (username)
    count_select = DB.select(sql)
    valid = ''
    if (len(count_select) == 0):
        valid = True
    else:
        valid = False
    return jsonify({"valid": valid})


@app.route('/register_doctor/', methods=["POST"])
def register_doctor():
    username = request.values.get('username')
    password = request.values.get('password')
    name = request.values.get('name')
    gender = request.values.get('sex')
    workID = request.values.get('workID')
    department = request.values.get('department')
    age = request.values.get('age')
    phoneNum = request.values.get('phone')
    major = request.values.get('major')
    email = request.values.get('email')

    sql = "insert into doctor(username,password,name,gender,workID,department,age,phoneNum,major,email) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (
        username, password, name, gender, workID, department, age, phoneNum, major, email)
    count_select = DB.update(sql)
    return jsonify('OK')


@app.route('/')
def DoctorHome():
    return render_template('DoctorHome.html')


@app.route('/PersonalHome/')
def PersonalHome():
    return render_template('PersonalHome.html')


@app.route('/PatientsPage/')
def index():
    sql = "select * from patients;"
    names = DB.select(sql)
    data_dict = {}
    for i in range(0, len(names)):
        data_dict[i + 1] = list(names[i])
    return render_template('PatientsPage.html', data_dict=data_dict)


@app.route('/test1/', methods=["GET", "POST"])
def test1():
    PatientName = request.args.get("name")
    sql = "select * from patients where name='%s';" % (PatientName)
    names = DB.select(sql)
    data_dict = {}
    for i in range(0, len(names)):
        print(names[i])
        data_dict[1 + i] = names[i]
    return render_template('PatientsPage.html', data_dict=data_dict)


@app.route('/test2/', methods=["GET", "POST"])
def test2():
    name = request.args.get("Name")
    age = request.args.get("Age")
    HeartRate = request.args.get("HeartRate")
    BloodPressure = request.args.get("BloodPressure")
    BloodSugar = request.args.get("BloodSugar")
    Cholesterol = request.args.get("Cholesterol")
    GlycerinTrihydrate = request.args.get("GlycerinTrihydrate")
    UricAcid = request.args.get("UricAcid")
    Platelet = request.args.get("Platelet")
    Glutopropase = request.args.get("Glutopropase")
    sql = "update patients set Age='%s', HeartRate='%s' ,BloodPressure='%s', BloodSugar='%s',Cholesterol='%s' ,GlycerinTrihydrate='%s',UricAcid='%s',Platelet='%s', Glutopropase='%s' where Name='%s';" % (
        age, HeartRate, BloodPressure, BloodSugar, Cholesterol, GlycerinTrihydrate, UricAcid, Platelet, Glutopropase,
        name)
    DB.update(sql)

    sql = "select * from patients;"
    names = DB.select(sql)
    data_dict = {}
    for i in range(0, len(names)):
        print(names[i])
        data_dict[1 + i] = names[i]
    return render_template('PatientsPage.html', data_dict=data_dict)


@app.route('/PatientsEditPage/')
def PatientsEditPage():
    return render_template('PatientsEditPage.html')


@app.route('/PersonalPage/')
def PersonalPage():
    sql = "select * from patients;"
    names = DB.select(sql)
    data_dict = {}
    for i in range(0, len(names)):
        data_dict[i + 1] = list(names[i])
    return render_template('PersonalPage.html', data_dict=data_dict)


@app.route('/test4/', methods=["GET", "POST"])
def test4():
    PatientName = request.args.get("name")
    sql = "select * from patients where name='%s';" % (PatientName)
    names = DB.select(sql)
    data_dict = {}
    for i in range(0, len(names)):
        print(names[i])
        data_dict[1 + i] = names[i]
    return render_template('PersonalPage.html', data_dict=data_dict)


@app.route('/Notehome/')
def Notehome():
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "SELECT * FROM `recipe` "
    cur.execute(sql)
    recipe_result = cur.fetchall()
    recipe_number = len(recipe_result)
    shu = []
    for i in range(recipe_number):
        shu.append(i + 1)
    print(recipe_result)
    sql = "SELECT * FROM `note` "
    cur.execute(sql)
    note_result = cur.fetchall()
    print(note_result)
    conn.close()
    return render_template('NoteHome.html', recipe_result=recipe_result, recipe_number=recipe_number,
                           note_result=note_result, shu=shu)


@app.route('/HealthArticle1/')
def HealthArticle1():
    return render_template('HealthArticle1.html')


@app.route('/HealthArticle2/')
def HealthArticle2():
    return render_template('HealthArticle2.html')


@app.route('/ChangeNote/')
def ChangeNote():
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "SELECT * FROM `recipe` "
    cur.execute(sql)
    recipe_result = cur.fetchall()
    recipe_number = len(recipe_result)
    shu = []
    for i in range(recipe_number):
        shu.append(i+1)
    print(recipe_result)
    sql = "SELECT * FROM `note` "
    cur.execute(sql)
    note_result = cur.fetchall()
    print(note_result)
    conn.close()
    return render_template('ChangeNote.html', recipe_result=recipe_result, recipe_number=recipe_number,
                           note_result=note_result, shu=shu)


@app.route('/updateRecipe/')
def updateRecipe():
    message = request.args.get("message")
    total = message.split("}")
    recipeList = []
    for i in range(len(total)):
        recipe = total[i].split("{")
        recipeList.append(recipe)
    print(recipeList)
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    for i in range(len(recipeList)):
        sql = "UPDATE `recipe` SET `picture`='%s',`name`='%s',`quantity`='%s',`description`='%s' WHERE `recipeID`='%s'" % (
            recipeList[i][1], recipeList[i][2], recipeList[i][3], recipeList[i][4], recipeList[i][0])
        print(sql)
        cur.execute(sql)
        conn.commit()
    conn.close()
    return "ok"


@app.route('/deleteRecipe/')
def deleteRecipe():
    message = request.args.get("message")
    print(message)
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "DELETE FROM `recipe` WHERE `recipeID`= '%s'" % message
    print(sql)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "ok"


@app.route('/addRecipe/')
def addRecipe():
    message = request.args.get("message")
    print(message)
    addmessage = message.split("{")
    print(addmessage)
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "INSERT INTO `recipe` (`picture`,`name`,`quantity`,`description`)VALUES('%s','%s','%s','%s')" % (
        addmessage[0], addmessage[1], addmessage[2], addmessage[3])
    print(sql)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "ok"


@app.route('/updateNote/')
def updateNote():
    message = request.args.get("message")
    print(message)
    notemessage = message.split("{")
    print(notemessage)
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "UPDATE `note` SET `healthArticle`='%s',`description`='%s',`generalNote`='%s' WHERE `noteId`=1" % (
            notemessage[0], notemessage[1], notemessage[2])
    print(sql)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "ok"


def getHistoryWeight(patientId, recentDays):
    sql = "select weight,date from weight_history where patientId=%d order by date limit %d" % (patientId, recentDays)
    result = DB.select(sql)
    data = []
    for item in result:
        data.append([str(item[1]).split(" ")[0], float(item[0])])
    return data


def getHistoryDietCalorie(patientId, recentDays=30):
    sql = "select calorie,data from diet where patientId=%d order by date limit %d" % (patientId, recentDays)
    result = DB.select(sql)
    day_calorie_dict = {}
    for item in result:
        day = str(item[1]).split(" ")[0]
        if day in day_calorie_dict:
            day_calorie_dict[day] += float(item[0])
        else:
            day_calorie_dict.update({day: float(item[0])})
    data = []
    for key in day_calorie_dict:
        data.append([key, day_calorie_dict[key]])
    return data


@app.route('/DietHome')
def dietHome():
    patient_id = 1
    historyWeight = getHistoryWeight(patient_id, 30)
    return render_template('DietHome.html')


@app.route('/historyWeight')
def historyWeight():
    patient_id = 1
    result = getHistoryWeight(patient_id, 30)
    return json.dumps({"info": result})


@app.route('/historyCalorie')
def historyCalorie():
    patient_id = 1
    result = getHistoryDietCalorie(patient_id, 30)
    return json.dumps({"info": result})


if __name__ == '__main__':
    app.run()
