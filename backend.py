from flask import Flask, session, redirect, url_for, escape, request,render_template,jsonify
import mysql.connector
import hashlib 
import json
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__) 
csrf = CSRFProtect(app)
mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

cursor = mycon.cursor()

app.config['SECRET_KEY'] = 'digitalPortalForSchools'


def schools():
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    cursor.execute("select school.schoolUsername, school.address, login.name from school join login where school.schoolUsername = login.username")
    schools = cursor.fetchall()
    
    count = len(schools)
    schoolsData=[schools,count]
    mycon.close()
    return schoolsData


@app.route('/register',methods = ['GET','POST'])
def register():
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    session['msg'] = "Some error occured. Please Try again"
    if request.method == 'POST':
        try:
            name = request.form['name']
            usr = request.form['username']
            pas = (hashlib.sha512((request.form['pass']).encode())).hexdigest()
            cat = request.form['category']
            sql = "INSERT INTO login (username,password,category,name) VALUES (%s, %s, %s, %s)"
            val = (usr,pas,cat,name)
            cursor.execute(sql, val)
            
            if(cat == "student"):

                session['msg'] = "Student registered"
                
            elif(cat == "parent"):
                cont = request.form['contact1']
                add = request.form['address1']
                email = request.form['email1']
                sql = "INSERT INTO parent (parentUsername,contact,address,email) VALUES (%s, %s, %s, %s)"
                val = (usr,cont,add,email)
                cursor.execute(sql, val)
                session['msg'] ="Registration Complete"
            else:
                cont = request.form['contact']
                add = request.form['address']
                email = request.form['email']
                scl = request.form['school']
                sql = "INSERT INTO teacher (teacherUsername,schoolUsername,contact,address,email,verifiedby,verified) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (usr,scl,cont,add,email,scl,"pending")
                cursor.execute(sql, val)
                session['msg'] = "Registration Complete"
            mycon.commit()
            
        except:
            mycon.rollback()
            print("error")
      
        finally:
            mycon.close()
            data = {}
            data['msg'] = session['msg']
            return json.dumps(data)



@app.route('/signOut')
def signOut():
    session.pop('username',None)
    return redirect('/')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    session['msg'] = "Error in login"
    if request.method == 'POST':
        try:
            usr = request.form['username1']
            pas = (hashlib.sha512((request.form['password1']).encode())).hexdigest()
            mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
            cursor = mycon.cursor()
            sql = "select * from login where username=%s and password=%s"
            val = (usr,pas)
            cursor.execute(sql, val)
            
            accounts = cursor.fetchall()
            mycon.close()
            if(len(accounts)==1):
                session['username'] = usr
                print("redirecting")
                session['msg'] = "Welcome User"
                return redirect('/profile')
                
            else:
                session['msg'] = "Incorrect Username or Password"
                schoolsData = schools()
                return render_template("template.html",msg=session['msg'],schools = schoolsData)
      
        except Exception as e:
            session['msg'] = "Some Error Occured. Please try again."
            session.pop('username',None)
            print(e)
            schoolsData = schools()
            return render_template("template.html",msg=session['msg'],schools = schoolsData)
            

@app.route('/classStructure',methods=['POST','GET']) 
def classStructure():
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
    cursor = mycon.cursor()
    classData={}
    if request.method == 'POST':
        try:
            school = request.get_data()
            print("hi")
            sql = ("select classcode,standard,section from classStructure where schoolUsername=%s")
            val = (school,)
            cursor.execute(sql,val)
            data = cursor.fetchall()
            classData['class_data'] = data
        except:
            classData['class_data'] = [[0,0,0]]
        finally:
            mycon.close()
            return json.dumps(classData)
            
@app.route('/profile',methods=['POST','GET'])
def profile():
    print("welcome")
    username = session['username']
    try:
        mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
        cursor = mycon.cursor()
        sql = ("select * from login where username=%s")
        val = (username,)
        cursor.execute(sql, val)
        accounts = cursor.fetchall()
        account = accounts[0]
        name = account[3]
        category = account[2]

        if(category == "student"):
            sql = "select * from student where studentUsername=%s"
            val = (username,)
            cursor.execute(sql, val)
            accounts = cursor.fetchall()
            
            mycon.close()
            if(len(accounts) == 0):
                schoolsData = schools()
                return render_template("studentInfo.html",msg=session['msg'],user=username,name=name,schools=schoolsData)
            else:
                return render_template("profile.html",msg=session['msg'],user=username, name=name)
        elif(category == "school"):
            print("school")
            mycon.close()
            return render_template("school_dashboard.html",msg=session['msg'],user=username, name=name)
        else:
            schoolsData = schools()
            mycon.close()
            return render_template("template.html",msg=session['msg'],schools = schoolsData)
    except Exception as e:
        session['msg'] = "Error"
        print(e)
        schoolsData = schools()
        return render_template("template.html",msg=session['msg'],schools = schoolsData)
    finally:
        mycon.close()


@app.route('/student_info',methods=['POST','GET'])
def student_info():
    session['msg'] = "Error"
    print(request.get_json())
    if request.method == 'POST':
        try:
            mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
            cursor = mycon.cursor()
            usr = request.json['username']
            pusr = request.json['parentUsername']
            pas = (hashlib.sha512((request.json['password']).encode())).hexdigest()
            school = request.json['school']
            standard = request.json['standard']
            sql = ("select * from login where username=%s and password=%s and category=%s")
            val = (pusr,pas,"parent")
            cursor.execute(sql, val)
            parents = cursor.fetchall()
            print("hi")
            if(len(parents)==1):
                parent = pusr
                print("hi")
                sql = "INSERT INTO student (studentUsername,classcode,schoolUsername,parentUsername,verifiedby,verified) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (usr,standard,school,parent,school,"pending")
                cursor.execute(sql,val)
                mycon.commit()
                session['msg'] = "Information Registered"
            else:
                session['msg'] = "Incorrect Information of parent or Parent not registered"
        except Exception as e:
            print(e)
            session['msg'] = "Some error occured."
        finally: 
            data={}
            data['msg'] = session['msg']
            return json.dumps(data)

@app.route('/search',methods=['POST','GET'])
def search():
    return render_template("school_dashboard.html")


@app.route('/')
def index():
    msg = "Welcome"
    if 'username' in session:
        return redirect('/profile')
    if 'msg' not in session:
        session['msg'] = msg
    schoolsData = schools()
    return render_template('template.html',msg=session['msg'], schools=schoolsData)



if __name__ == '__main__':
    app.run(debug = True)




    # pas = (hashlib.sha512(("school01").encode())).hexdigest()
    # print(pas)

   