import re
from django.shortcuts import render
from flask import Flask,render_template,request,session,url_for,redirect
import smtplib,random,string
import mysql.connector
app=Flask(__name__)

db=mysql.connector.connect(database="library",user="",password="")
c=db.cursor()


@app.route("/")    #mapping  or decorator
def myroot():
	return render_template("index.html")

@app.route("/adminLogin")
def adminLogin():
        return render_template("adminLogin.html")

@app.route("/userLogin")
def userLogin():
        return render_template("userLogin.html")

@app.route("/Register")
def Register():
        return render_template("Register.html")

@app.route("/addBooks")    
def addBooks():
	return render_template("addBooks.html")

@app.route("/MyBooks")
def MyBooks():
        c.execute("select * from hire")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("MyBooks.html",d=data)

@app.route("/userViewBooks")    
def userViewBooks():
        c.execute("select * from books")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("userViewBooks.html",d=data)

@app.route("/viewBooks")    
def viewBooks():
        c.execute("select * from books")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("viewBooks.html",d=data)

@app.route("/updateBook",methods=['POST'])    
def updateBooks():
        id=request.form['bid']
        c.execute("select * from books where bookid="+id)
        data=c.fetchall()
        #data is tuples in a list
        return render_template("updateBook.html",d=data)


@app.route('/choice',methods=['POST'])
def submit():
                characters = list(string.ascii_letters + string.digits + "!@#$%^&*")
                random.shuffle(characters)
                p=[]
                for i in range(7):
                        p.append(random.choice(characters))

                s1="".join(p)
                e=request.form['email']
                s=smtplib.SMTP('smtp.gmail.com',587)
                s.starttls()
                s.login("your email","your email app password")#if you dont no about apppassword you can search in google how to generate app password

                s.sendmail('',e,s1)
                s.quit()
                i=request.form['id1']
                n=request.form['name']
                e=request.form['email']
                p=request.form['phone']
                pd=s1
                sql="insert into users values("+str(i)+",'"+n+"','"+e+"','"+p+"','"+pd+"')"
                c.execute(sql)
                db.commit()
                return render_template("userLogin.html") 
@app.route('/UserProfile')
def UserProfile():
        i=session['uid']
     
        sql="SELECT * FROM `users` WHERE id1="+str(i)
       
        c.execute(sql)
        data=c.fetchall()
        return render_template('UserProfile.html',d=data)

@app.route("/updateuser",methods=['POST'])    
def updateuser():
        id=session['uid']
        c.execute("select * from users where id1="+str(id))
        data=c.fetchall()
        #data is tuples in a list
        return render_template("updateuser.html",d=data)

@app.route("/HireBook",methods=['POST'])    
def HireBook():
        userid=session['uid']
        uname=session['uname']
        bid=request.form['bid']
        bname=request.form['bookname']
       
        sql="insert into hire(bookid,userid,bookname,username) values('"+str(bid)+"','"+str(userid)+"','"+bname+"','"+uname+"')"
        c.execute(sql)
        db.commit()
        return render_template("UserHomePage.html")

@app.route("/admindb",methods=['POST'])
def admindb():
        un=request.form['uname']
        pwd=request.form['pwd']

        if un=='admin' and pwd=='admin':
                return render_template("admin.html")
        else:
                return render_template("adminLogin.html",result='Invalid login or password. Please try again')
        
        
@app.route("/UserLoginDB",methods=['POST'])    
def UserLoginDB():
        em=request.form['email']
        pwd=request.form['password']
        sql="SELECT * FROM `users` WHERE email='"+em+"' and password='"+pwd+"'"
        c.execute(sql)
        d=c.fetchall()
        if len(d)>0:
                session['uid']=d[0][0]
                session['uname']=d[0][1]
                return render_template("UserHomePage.html")
        else:
                return render_template("userLogin.html",result='Invalid login or password. Please try again')     

@app.route("/addBooksDB",methods=['POST'])    
def addBooksDB():
        bid=request.form['t1']
        bname=request.form['t2']
        aname=request.form['t3']
        dop=request.form['t4']
        cost=request.form['t5']

        sql="insert into books values("+str(bid)+",'"+bname+"','"+aname+"','"+dop+"',"+str(cost)+")"
        c.execute(sql)
        db.commit()
        return render_template("addBooks.html",res="successfully added")


@app.route("/updateuserdb",methods=['POST'])    
def updateuserdb():
        id1=request.form['id1']
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        pwd=request.form['password']

        
        sql = "update users set name=%s,email=%s,phone=%s,password=%s where id1 = %s"
        data = (name,email,phone,pwd,id1)
        c.execute(sql,data)
 

        db.commit()
        
        c.execute("select * from users WHERE id1='" + id1 + "'")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("userProfile.html",d=data)





@app.route("/updateBooksDB",methods=['POST'])    
def updateBooksDB():
        bid=request.form['t1']
        bname=request.form['t2']
        aname=request.form['t3']
        dop=request.form['t4']
        cost=request.form['t5']

        sql="update books set bookname='"+bname+"',authorname='"+aname+"',dateofpublishing='"+dop+"',bookcost="+str(cost)+" where bookid="+bid
        print(sql)
        c.execute(sql)
        db.commit()
        
        c.execute("select * from books")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("viewBooks.html",d=data)


@app.route("/deleteBook",methods=['POST'])    
def delete():
        bid=request.form['bid']
        
        sql="delete from books where bookid="+bid
        print(sql)
        c.execute(sql)
        db.commit()
        
        c.execute("select * from books")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("viewBooks.html",d=data)


@app.route("/deleteuserbook",methods=['POST'])    
def deleteuserbook():
        bid=request.form['id']
        
        sql="delete from hire where id="+bid
        c.execute(sql)
        db.commit()
        
        c.execute("select * from hire")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("MyBooks.html",d=data)


@app.route("/hello")    #mapping  or decorator
def myhello():
	return "welcome to heaven"
if __name__=='__main__':
        app.secret_key='1234'
        app.run(port=9123,debug=True)
