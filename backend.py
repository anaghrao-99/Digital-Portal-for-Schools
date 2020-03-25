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
            
@app.route('/profile')
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
            msg = "Welcome " + name
            mycon.close()
            if(len(accounts) == 0):
                return render_template("studentInfo.html",msg=msg,user=username,name=name)
            else:
                return render_template("profile.html",msg=msg,user=username, name=name)
        elif(category == "school"):
            msg = "Welcome " + name
            print("school")
            mycon.close()
            return render_template("school_dashboard.html",msg=msg,user=username, name=name)
        else:
            schoolsData = schools()
            mycon.close()
            return render_template("template.html",msg=msg,schools = schoolsData)
    except:
        msg = "Error"
        schoolsData = schools()
        return render_template("template.html",msg=msg,schools = schoolsData)
    finally:
        mycon.close()
        


def schools():
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    cursor.execute("select school.schoolUsername, school.address, login.name from school join login where school.schoolUsername = login.username")
    school = cursor.fetchall()
    count = len(school)
    schoolsData=[school,count]
    mycon.close()
    return schoolsData


@app.route('/signOut')
def signOut():
    session.pop('username',None)
    return redirect('/')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    msg = "Error in login"
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
                return redirect('/profile')
                
            else:
                msg = "Incorrect Username or Password"
                schoolsData = schools()
                return render_template("template.html",msg=msg,schools = schoolsData)

                    
        except:
            msg = "Some Error Occured. Please try again."
            session.pop('username',None)
            schoolsData = schools()
            return render_template("template.html",msg=msg,schools = schoolsData)
            
            






@app.route('/search',methods=['POST','GET'])
def search():
    school_name = request.form.get('schoolSearch')
    # print("Hello")
    print(school_name)
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
    cursor = mycon.cursor()
    
    string = "select * from school where schoolUsername=%s"
    
    val = ( school_name, )
    
    cursor.execute(string, val)
    school_info = cursor.fetchall()
    print(school_info)


    cursor = mycon.cursor()
    sql_comments = "select * from schoolComments where schoolUsername=%s"
    val = ( school_name, )
    cursor.execute(sql_comments, val)
    school_comments = cursor.fetchall()

    if(len(school_info) != 0):
        return render_template("school_dashboard.html", school_info = school_info, school_comments = school_comments)


@app.route('/')
def index():
    # while(1):
    #     if 'username' in session:
    #         session.pop('username',None)  
    #     else:
    #         break
    if 'username' in session:
        return redirect('/profile')
    schoolsData = schools()
    msg = "Welcome"
    return render_template('template.html',msg=msg, schools=schoolsData)



if __name__ == '__main__':
    
    app.run(debug = True)




    # pas = (hashlib.sha512(("school01").encode())).hexdigest()
    # print(pas)

   