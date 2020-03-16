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

@app.route('/register',methods = ['GET','POST'])
def register():
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    msg = "Some error occured. Please Try again"
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

                msg = "Student registered"
                
            elif(cat == "parent"):
                cont = request.form['contact1']
                add = request.form['address1']
                email = request.form['email1']
                sql = "INSERT INTO parent (parentUsername,contact,address,email) VALUES (%s, %s, %s, %s)"
                val = (usr,cont,add,email)
                cursor.execute(sql, val)
                msg ="Registration Complete"
            else:
                cont = request.form['contact']
                add = request.form['address']
                email = request.form['email']
                scl = request.form['school']
                sql = "INSERT INTO teacher (teacherUsername,schoolUsername,contact,address,email,verifiedby,verified) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (usr,scl,cont,add,email,scl,"pending")
                cursor.execute(sql, val)
                msg = "Registration Complete"
            mycon.commit()
            
        except:
            mycon.rollback()
            print("error")
      
        finally:
            mycon.close()
            data = {}
            data['msg'] = msg
            return json.dumps(data)
            

@app.route('/login',methods = ['POST', 'GET'])
def login():
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    if request.method == 'POST':
        try:
            usr = request.form['username']
            pas = (hashlib.sha512((request.form['password']).encode())).hexdigest()
            
            sql = "select * from login where username=%s and password=%s"
            val = (usr,pas)
            cursor.execute(sql, val)
            
            accounts = cursor.fetchall()
            account = accounts[0]

            if(len(accounts)==1):
                username = usr
                name = account[3]
                category = account[2]

                if(category == "student"):
                    sql = "select * from student where username=%s"
                    val = (username)
                    cursor.execute(sql, val)
                    
                    accounts = cursor.fetchall()
                    return render_template("profile.html",user=username, name=name)
                elif(category == "school"):
                    return render_template("school_dashboard.html",user=username, name=name)
            msg = "done"
            return render_template("template.html",msg = msg)
            
        except:
            mycon.rollback()
            msg = "error in insert operation"
            return render_template("template.html",msg = msg)
            
      
        finally:
            mycon.close()

@app.route('/search',methods=['POST','GET'])
def search():
    return render_template("school_dashboard.html")



@app.route('/')
def index():
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    cursor.execute("select school.schoolUsername, school.address, login.name from school join login where school.schoolUsername = login.username")
    schools = cursor.fetchall()
    count = len(schools)
    return render_template('template.html', schools=schools, count=count)


if __name__ == '__main__':
    app.run(debug = True)
    # pas = (hashlib.sha512(("school01").encode())).hexdigest()
    # print(pas)

   