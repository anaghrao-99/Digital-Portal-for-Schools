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

def studentdata(username):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
    cursor = mycon.cursor()
    sql = "select * from student where studentUsername=%s"
    val = (username,)
    cursor.execute(sql, val)
    accounts = cursor.fetchall()
    studentinfo = list(accounts[0])
    class1 = classFromCode(studentinfo[1])
    studentinfo[1] = class1
    studentinfo[2] = getName(studentinfo[2])
    studentinfo[0] = getName(studentinfo[0])
    verified = studentinfo[5]
    sql = "select * from notes where studentUsername=%s"
    val = (username,)
    cursor.execute(sql, val)
    table = list(cursor.fetchall())
    notes=[]
    notes.append(0)
    for note in table:
        note1 = list(note)
        note1[1] = getName(note1[1])
        notes.append(note1)
    notes[0] = len(notes) 
    mycon.close()
    return [studentinfo,verified,notes]

def updateNotes(id):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
    cursor = mycon.cursor()
    sql = "update notes set signature='Signed' where id=%s"
    val = (int(id),)
    cursor.execute(sql, val)
    mycon.commit()
    mycon.close()
    

def schools():
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    cursor.execute("select school.schoolUsername, school.address, login.name from school join login where school.schoolUsername = login.username")
    schools = cursor.fetchall()
    
    count = len(schools)
    schoolsData=[schools,count]
    mycon.close()
    return schoolsData

def schoolInformation(username):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
    cursor = mycon.cursor()

    string = "select * from school where schoolUsername=%s"
    
    val = ( username, )
    
    cursor.execute(string, val)
    table = cursor.fetchall()
    school_info = []
    school = list(table[0])
    school.append(getName(school[0]))
    school_info.append(school)
    cursor = mycon.cursor()
    sql_comments = "select * from schoolComments where schoolUsername=%s"
    val = ( username, )
    cursor.execute(sql_comments, val)
    table = list(cursor.fetchall())
    school_comments =[]
    for row in table:
        comment = list(row)
        comment.append(getCategory(comment[3]))
        comment[3] = getName(comment[3])
        

        if 'username' in session:
            if session['username'] == username:
                # print("hi")
                comment.append(2)                   #cannot like or dislike
            else:
                sql_comments = "select * from likes where id=%s and user=%s"
                val = ( comment[0],session['username'])
                cursor.execute(sql_comments, val)
                table=cursor.fetchall()
                if(len(table) == 0):
                    comment.append(0)
                else:
                    comment.append(table[0][2])
        else:
            comment.append(2)
        school_comments.append(comment)       
        
    count = len(school_comments)
    comments = [school_comments, count]
    data = [school_info, comments]
    return data

def approval(username):
    approvals=[]
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
    cursor = mycon.cursor()
    teachers = []
    sql = "select * from teacher where verifiedby=%s and verified=%s"
    val=(username,"pending")
    cursor.execute(sql,val)
    table = cursor.fetchall()
    for row in table:
        t = list(row)
        t.append(getName(t[0]))
        teachers.append(t)
    students =[]
    sql = "select * from student where verifiedby=%s and verified=%s"
    val=(username,"pending")
    cursor.execute(sql,val)
    table = cursor.fetchall()
    for row in table:
        s = list(row)
        s[1] = classFromCode(s[1])
        s[3] = getName(s[3])
        s.append(getName(s[0]))
        students.append(s)
    approvals = [teachers,len(teachers),students,len(students)]
    mycon.close()
    return approvals

def structure(username):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
    cursor = mycon.cursor()

    sql = "select * from teaches where classcode in ( select classcode from classStructure where schoolUsername=%s)"
    val=(username,)
    cursor.execute(sql,val)
    structure = cursor.fetchall()
    struct = [structure,len(structure)]

    mycon.close()
    return struct

def votes(id,user,vote):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
    cursor = mycon.cursor()
    sql_comments = "select * from likes where id=%s and user=%s"
    val = ( id,user)
    cursor.execute(sql_comments, val)
    table=cursor.fetchall()
    if(len(table) == 0):
        sql_comments = "insert into likes(id,user,vote) values(%s,%s,%s)"
        val = ( id,user,vote )
        cursor.execute(sql_comments, val)
        if vote == 1:
            sql_comments = "update schoolComments set upvote=upvote+%s where id=%s"
            val = ( 1,id )
            cursor.execute(sql_comments, val)
        else:
            sql_comments = "update schoolComments set downvote=downvote+%s where id=%s"
            val = (1, id )
            cursor.execute(sql_comments, val)
    else:
        vote1 = table[0][2]
        if vote1 != vote:
            sql_comments = "update likes set vote=%s where id=%s and user=%s"
            val = ( int(vote),id,user )
            cursor.execute(sql_comments, val)
            sql_comments = "update schoolComments set upvote=upvote+%s, downvote=downvote-%s where id=%s"
            val = ( int(vote),int(vote),id )
            cursor.execute(sql_comments, val)
        else:
            sql_comments = "delete from likes where id=%s and user=%s"
            val = ( id,user )
            cursor.execute(sql_comments, val)
            if vote == 1:
                sql_comments = "update schoolComments set upvote=upvote-%s where id=%s"
                val = ( 1,id )
                cursor.execute(sql_comments, val)
            else:
                sql_comments = "update schoolComments set downvote=downvote-%s where id=%s"
                val = (1, id )
                cursor.execute(sql_comments, val)

    mycon.commit()
    return

def classFromCode(class1):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
    cursor = mycon.cursor()
    
    string = "select * from classStructure where classcode=%s"
    
    val = ( class1, )
    
    cursor.execute(string, val)
    class_info = cursor.fetchall()
    class1 = "" + class_info[0][2] + " " + class_info[0][3]
    return class1

def studentList(username):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    sql = "select * from student where parentUsername=%s"
    val = (username,)
    cursor.execute(sql,val)
    table = cursor.fetchall()
    usernameList = []
    for user in table:
        sql = "select * from login where username=%s"
        val = (user[0],)
        cursor.execute(sql, val)
        accounts = cursor.fetchall()
        namec = accounts[0][3]
        usernameList.append([user[0],namec])
        # print(usernameList)
    count = len(usernameList)
    return [usernameList,count]

def getName(username):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    sql = "select * from login where username=%s"
    val = (username,)
    cursor.execute(sql,val)
    table = cursor.fetchall()
    return table[0][3]

def getCategory(username):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()
    sql = "select * from login where username=%s"
    val = (username,)
    cursor.execute(sql,val)
    table = cursor.fetchall()
    # print(table)
    return table[0][2]


def isAssociated(school):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )

    cursor = mycon.cursor()

    sql = "select * from login where username=%s"
    val=(session['username'],)
    cursor.execute(sql,val)
    accounts = cursor.fetchall()
    account=accounts[0]
    if account[2] == 'school':
        return "N"
    elif account[2] == 'student':
        sql = "select * from student where studentUsername=%s and verified=%s"
        val=(session['username'],"verified")
        cursor.execute(sql,val)
        accounts = cursor.fetchall()
        student=accounts[0]
        if student[2] == school:
            return "Y"
        else:
            return "N"
    elif account[2] == 'parent':
        sql = "select * from student where parentUsername=%s and verified=%s"
        val=(session['username'],"verified")
        cursor.execute(sql,val)
        table = cursor.fetchall()
        if len(table) == 0:
            return "N"
        else:
            for row in table:
                if row[2] == school:
                    return "Y"
            return "N"
    else:
        sql = "select * from teacher where teacherUsername=%s and schoolUsername=%s and verified=%s"
        val=(session['username'],school,"verified")
        cursor.execute(sql,val)
        table = cursor.fetchall()
        if len(table)>0:
            return "Y"
        else:
            return "N"

    
def insertComment(commenter, comment, school):
    mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
    cursor = mycon.cursor()
    
    sql = "insert into schoolComments (schoolUsername,comment,commenter,upvote,downvote) values (%s ,%s ,%s, %s, %s)"
    val = (school, comment,commenter ,int(0) ,int(0))
    cursor.execute(sql,val)
    mycon.commit()
    mycon.close()
    return
            


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

@app.route('/profile',methods=['POST','GET'])
def profile():
       
    # try:
        username = session['username']
        mycon = mysql.connector.connect( host="localhost", user="root", passwd="123456789", db="digischool" )
        cursor = mycon.cursor()
        sql = ("select * from login where username=%s")
        val = (username,)
        cursor.execute(sql, val)
        accounts = cursor.fetchall()
        account = accounts[0]
        name = account[3]
        category = account[2]
        session['msg'] = "Welcome user"
        if(category == "student"):
            sql = "select * from student where studentUsername=%s"
            val = (username,)
            cursor.execute(sql, val)
            accounts = cursor.fetchall()
            if(len(accounts) == 0):
                schoolsData = schools()
                return render_template("studentInfo.html",msg=session['msg'],user=username,name=name,schools=schoolsData)
            else:
                data = studentdata(username)
                studentinfo = data[0]
                verified = data[1]
                schoolsData = schools()
                if(verified == 'pending'):
                    mycon.close()
                    return render_template("pendingStudent.html",msg=session['msg'],user=username,name=name)
                else:
                    notes = data[2]
                    mycon.close()
                    return render_template("profile.html",notes=notes,msg=session['msg'],user=username, name=name,studentInfo=studentinfo,schools=schoolsData,category="student")
        elif(category == "parent"):
            schoolsData = schools()
            children = studentList(username)
            usernameList = children[0]
            count=children[1]
            return render_template("parent.html",name=name,user=username,msg=session['msg'],count=count,schools = schoolsData, children = usernameList,category="parent")
        
        elif(category == "school"):
            data = schoolInformation(username)
            school_info = data[0]
            comments = data[1]
            schoolsData = schools()
            approvals = approval(username)
            struct = structure(username)
            print(approvals[1])
            mycon.close()
            return render_template("dashboard.html",editAllowed="N",approvals=approvals,structure=struct,schools=schoolsData,user = username,name=name, school_info = school_info, school_comments = comments,category="school")
            
        else:
            schoolsData = schools()
            mycon.close()
            return render_template("template.html",msg=session['msg'],schools = schoolsData,category="teacher")
    
    
    
    # except Exception as e:
    #     session['msg'] = "Error"
    #     print(e)
    #     schoolsData = schools()
    #     return render_template("template.html",msg=session['msg'],schools = schoolsData,category="")
    # finally:
        mycon.close()



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


@app.route('/vote', methods=['POST','GET'])
def vote():
    if request.method == 'POST':
        data = {}
        try:
            i = request.json['id']
            vote = request.json['vote']
            username = session['username']
            votes(i,username,vote)
            msg="done"
        except Exception as e:
            msg = "Issue"
            print(e)
        finally:
            data['msg'] = msg
            return data


@app.route('/child',methods=['POST','GET'])
def child():
    if(request.method=='POST'):
        try:
            susername = request.form['susername']
            username = request.form['username']
            name = request.form['name']
            
            children = studentList(username)
            usernameList = children[0]
            count=children[1]
            data = studentdata(susername)
            studentinfo = data[0]
            verified = data[1]
            schoolsData = schools()
            print(verified)
            if(verified == 'pending'):
                session['msg'] = "Verification of your child is pending"
                print("hi")
                return render_template("pending.html",child=child,msg=session['msg'],user=username,name=name,studentInfo=studentinfo,schools=schoolsData,category="parent",children=usernameList,count=count)
            else:
                notes = data[2]
                return render_template("childProfile.html",child=child,notes=notes,studentInfo=studentinfo,msg=session['msg'],user=username, name=name,schools=schoolsData,category="parent",children=usernameList,count=count)
        except Exception as e:
            print(e)
            return redirect('/profile')

@app.route('/signNote', methods=['POST','GET'])
def signNote():
    if request.method == 'POST':
        data={}
        try:
            index = request.get_data()
            updateNotes(index)
            print("Signed")
            data['msg'] = "Signed"
        except:
            print("issue")
            data['msg'] = "Issue"
        finally:
            return data

@app.route('/comment', methods=['POST','GET'])
def comment():
    if request.method=='POST':
        try:
            usr = session['username']
            comment = request.form['comment']
            school = request.form['school']
            insertComment(usr,comment,school)
            print("done")

        except Exception as e:
            print("err ", e)
        finally:
            return redirect('/school')
        

@app.route('/student_info',methods=['POST','GET'])
def student_info():
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
    school_name = request.form.get('schoolSearch')
    session['search'] = school_name
    return redirect('/school')

@app.route('/school',methods=['POST','GET'])
def school():
    school_name = session['search']
    data = schoolInformation(school_name)
    school_info = data[0]
    comments = data[1]
    schoolsData = schools()
    user = ""
    name = ""
    editAllowed = "N"
    if 'username' in session:
        user = session['username']
        cursor.execute(("select category from login where username=%s"),(session['username'],))
        table = cursor.fetchall()
        editAllowed = isAssociated(school_name)
        name = getName(user)
    if(len(school_info) != 0):
        return render_template("dashboard.html",editAllowed=editAllowed,schools=schoolsData,user = user, name=name, school_info = school_info, school_comments = comments,category="viewer")


@app.route('/')
def index():
    msg = "Welcome"
    if 'username' in session:
        return redirect('/profile')
    session['msg'] = msg
    schoolsData = schools()
    return render_template('template.html',msg=session['msg'], schools=schoolsData,category="")



if __name__ == '__main__':
    app.run(debug = True)




    # pas = (hashlib.sha512(("school01").encode())).hexdigest()
    # print(pas)

   