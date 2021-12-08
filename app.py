import os
from itertools import chain

import pymysql
from flask import Flask, render_template, request, session, jsonify
from db import connmysql
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
DB = connmysql(user="root", password="12345678", database="phms")
config = {'host': '127.0.0.1',
          'port': 3306,
          'user': 'root',
          'password': '12345678',
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
    day_weight_dict = {}
    for item in result:
        day = str(item[1]).split(" ")[0]
        day_weight_dict.update({day: float(item[0])})
    return day_weight_dict


def getHistoryDietCalorie(patientId, recentDays=30):
    sql = "select calorie,date from diet where patientId=%d order by date limit %d" % (patientId, recentDays)
    result = DB.select(sql)
    day_calorie_dict = {}
    for item in result:
        day = str(item[1]).split(" ")[0]
        if day in day_calorie_dict:
            day_calorie_dict[day] += float(item[0])
        else:
            day_calorie_dict.update({day: float(item[0])})
    return day_calorie_dict


def getRecodeDays(patientId):
    sql = "select date from diet where patientId=%d " % patientId
    result = DB.select(sql)
    days = []
    for item in result:
        day = str(item[0]).split(" ")[0]
        if day in days:
            continue
        else:
            days.append(day)
    return len(days)


def getMaxMinWeight(patientId):
    sql = "select max(weight),min(weight),avg(weight) FROM weight_history where patientId=%d " % patientId
    result = DB.select(sql)[0]
    return round(float(result[0]), 2), round(float(result[1]), 2), round(float(result[2]), 2)


def getAllDietRecord(patientId):
    sql = "select foodName, intake, calorie, date from diet where patientId=%d order by date desc" % patientId
    result = DB.select(sql)
    data = []
    for item in result:
        data.append(list(item))
    return data


@app.route('/DietHome')
def dietHome():
    patient_id = 1
    record_days = getRecodeDays(patient_id)
    max_weight, min_weight, avg_weight = getMaxMinWeight(patient_id)
    diet_info = getAllDietRecord(patient_id)
    info = {
        "record_days": record_days,
        'min_weight': min_weight,
        "max_weight": max_weight,
        "avg_weight": avg_weight,
        "diet_info": diet_info
    }
    return render_template('DietHome.html', info=info)


@app.route('/historyWeight')
def historyWeight():
    patient_id = 1
    day_weight_dict = getHistoryWeight(patient_id, 30)
    day_calorie_dict = getHistoryDietCalorie(patient_id, 30)
    calorie = []
    weight = []
    days = list(set(list(day_weight_dict.keys())).union(set(list(day_calorie_dict.keys()))))
    days.sort()
    for day in days:
        if day in day_calorie_dict:
            calorie.append(day_calorie_dict[day])
        else:
            calorie.append(None)
        if day in day_weight_dict:
            weight.append(day_weight_dict[day])
        else:
            weight.append(None)

    return json.dumps({"y_data":calorie, 'y_data1': weight,'x':days })


@app.route("/addDiet")
def addDiet():
    patientId = 1
    foodName = request.args.get("food")
    intake = request.args.get("intake")
    date = request.args.get("time")
    calorie = request.args.get("calorie")
    sql = "insert into diet(patientId,foodName, intake, date, calorie) values (%d, '%s','%s','%s','%s')" % (
    patientId, foodName, intake, date, calorie)
    DB.update(sql)
    return "ok"


@app.route("/deleteDiet")
def deleteDiet():
    patientId = 1
    foodName = request.args.get("food")
    intake = request.args.get("intake")
    date = request.args.get("time")
    sql = "delete from diet where patientId = %d and foodName='%s' and intake='%s' and date='%s'" % (
    patientId, foodName, intake, date)
    DB.update(sql)
    return "ok"


@app.route("/addWeight")
def addWeight():
    patientId = 1
    date = request.args.get("time")
    weight = request.args.get("weight")
    sql = "insert into weight_history(patientId,weight,date) values (%d,'%s','%s')" % (
    patientId, weight,date)
    DB.update(sql)
    return "ok"

@app.route('/MedicationHome/')
def MedicationHome():
    patient = request.args.get("name")
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "SELECT * FROM `medication`"
    cur.execute(sql)
    medications = cur.fetchall()
    conn.close()
    return render_template('MedicationHome.html', medications=medications)


@app.route('/MedicationAdd', methods=['POST', 'GET'])
def MedicationAdd():
    patient = request.args.get("name")
    if request.method == 'POST':
        disease = request.form['disease']
        doctor = request.form['doctor']
        nextDate = request.form['nextDate']
        temp = request.form['temp']
        print('temp: ', temp)

        medicines = temp.split('/')
        medicines.remove("")
        print(medicines)
        print(len(medicines))
        nums = len(medicines)

        date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        flag = date
        sql = "INSERT INTO medication(disease, doctor, date, nextDate, flag) values('%s', '%s', '%s', '%s', '%s')" % (disease, doctor, date, nextDate, flag)
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = "SELECT medicationId FROM `medication` WHERE flag=%s" % (flag)
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        cur.execute(sql)
        medicationId = cur.fetchone()
        print(medicationId)

        for i in range(nums):
            m = medicines[i].split(',')
            medicine = m[0]
            type = m[1]
            comment = m[2]
            sql = "INSERT INTO medication_medicine(medicationId, medicine, type, comment) values('%s', '%s', '%s', '%s')" % (medicationId[0], medicine, type, comment)
            print(sql)
            conn = pymysql.connect(**config)
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()

        conn.close()
        return redirect(url_for('MedicationHome'))
    else:
        return render_template('MedicationAdd.html')


@app.route('/MedicationDetail')
def MedicationDetail():
    medicationId = request.args.get('medicationId')
    print(medicationId)
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "SELECT * FROM `medication` WHERE medicationId=%s" % (medicationId)
    cur.execute(sql)
    medication = cur.fetchone()
    print(medication)

    sql = "SELECT * FROM `medication_medicine` WHERE medicationId=%s" % (medicationId)
    cur.execute(sql)
    medicines = cur.fetchall()

    medicine=[]

    conn.close()
    return render_template('MedicationDetail.html', medication=medication, medicines=medicines, medicine=medicine)


@app.route('/MedicationEdit', methods=['POST', 'GET'])
def MedicationEdit():
    if request.method == 'POST':
        medicationId = request.form["medicationId"]
        disease = request.form['disease']
        doctor = request.form['doctor']
        nextDate = request.form['nextDate']
        sql = "UPDATE medication SET disease='%s', doctor='%s', nextDate='%s' WHERE medicationId=%s" % (disease, doctor, nextDate, medicationId)
        print(sql)
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
    return redirect(url_for('MedicationHome'))

@app.route('/MedicationDel', methods=['POST', 'GET'])
def MedicationDel():
    if request.method == 'POST':
        medicationId = request.get_json()['medicationId']
        sql = "DELETE FROM medication WHERE medicationId=%s " % (medicationId)
        print(sql)
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return 'ok'

@app.route('/MedicineDel', methods=['POST', 'GET'])
def MedicineDel():
    if request.method == 'POST':
        mmId = request.get_json()['mmId']
        sql = "DELETE FROM medication_medicine WHERE mmId=%s " % (mmId)
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return 'ok'

@app.route('/MedicineEdit', methods=['POST', 'GET'])
def MedicineEdit():
    mmId = request.args.get('mmId')
    medicationId = request.args.get('medicationId')
    print(mmId, medicationId)
    if request.method == 'POST':
        mmId = request.form['mmId']
        medicationId = request.form['meId']
        medicine = request.form['medicine']
        type = request.form['type']
        comment = request.form['comment']
        sql = "UPDATE medication_medicine SET medicine='%s', type='%s', comment='%s' WHERE mmId=%s" % (medicine, type, comment, mmId)
        print(sql)
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('MedicationHome'))
    else:
        sql = "SELECT * FROM `medication_medicine` WHERE mmId=%s" % (mmId)
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        cur.execute(sql)
        medicine = cur.fetchone()

        sql = "SELECT * FROM `medication` WHERE medicationId=%s" % (medicationId)
        cur.execute(sql)
        medication = cur.fetchone()

        sql = "SELECT * FROM `medication_medicine` WHERE medicationId=%s" % (medicationId)
        cur.execute(sql)
        medicines = cur.fetchall()

        conn.close()
        return render_template('MedicationDetail.html', medication=medication, medicines=medicines, medicine=medicine)



if __name__ == '__main__':
    app.run()
