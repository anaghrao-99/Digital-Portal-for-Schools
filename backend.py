from flask import Flask, session, redirect, url_for, escape, request,render_template
import mysql.connector
import hashlib 
  
app = Flask(__name__) 
mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

cursor = mycon.cursor()


@app.route('/register',methods = ['POST', 'GET'])
def register():
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    if request.method == 'POST':
        try:
            name = request.form['name']
            usr = request.form['username']
            pas = (hashlib.sha512((request.form['pass']).encode())).hexdigest()
            cat = request.form['category']
            if(cat == "student"):
                
            # print(name)
            # print(usr)
            # print(pas)
            # print(cat)
            sql = "INSERT INTO login (username,password,category,name) VALUES (%s, %s, %s, %s)"
            val = (usr,pas,cat,name)
            cursor.execute(sql, val)
            mycon.commit()
            msg = "done"
        except:
            mycon.rollback()
            msg = "error in insert operation"
            print("error")
      
        finally:
            return render_template("template.html",msg = msg)
            mycon.close()

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
            msg = "done"
            return render_template("template.html",msg = msg)
            
        except:
            mycon.rollback()
            msg = "error in insert operation"
            return render_template("template.html",msg = msg)
            print("error")
      
        finally:
            mycon.close()



@app.route('/')
def index():
    return render_template('template.html')


if __name__ == '__main__':
    # app.run(debug = True)
    pas = (hashlib.sha512(("school01").encode())).hexdigest()
    print(pas)

   