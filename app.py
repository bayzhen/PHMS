import os

from flask import Flask, render_template, request, session, jsonify

from db import connmysql

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
DB = connmysql(user="PHMS", password="123456", database="phms")


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
    age, HeartRate, BloodPressure, BloodSugar, Cholesterol, GlycerinTrihydrate, UricAcid, Platelet, Glutopropase, name)
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


@app.route('/Notehome')
def Notehome():
    return render_template('NoteHome.html')


if __name__ == '__main__':
    app.run()
