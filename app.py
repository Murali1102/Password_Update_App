from flask import Flask, redirect, render_template,request,url_for,flash,session
import sqlite3

conn= sqlite3.connect("database1.db") 
conn.execute("create table if not exists data1(username TEXT,password TEXT);")
conn.close()

app = Flask(__name__)
app.secret_key='_privatekey_'

@app.route('/',methods=['POST','GET'])
def add_data():
    if request.method=='POST':
              
            username=request.form['username']
            password=request.form['password']
            # print(username,password)
            conn=sqlite3.connect("database1.db")
            cur=conn.cursor()
            query="SELECT username,password FROM data1 where username= '"+username+"' and password= '"+password+"'"
            cur.execute(query)
            data1=cur.fetchall()
            conn.commit()
            
            if len(data1) ==0:
                print('incorrect username or password')
            else:
                return redirect(url_for("view_record",data1=data1))            
    return render_template("index.html")
            
@app.route('/view_record')
def view_record():
    con=sqlite3.connect("database1.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM data1")
    data1=cur.fetchall()
    con.commit()
    con.close()
    return render_template('index1.html',data1=data1)


@app.route("/update_record/<string:uid>",methods=["POST","GET"] )
def update_record(uid):
    if request.method=='POST':
        try:
            
            password=request.form['password']
            conn=sqlite3.connect("database1.db")
            cur=conn.cursor()
            cur.execute("update data1 set password=? where username=? ",(password,uid))
            conn.commit()
        finally:
            return redirect(url_for("view_record"))

    con=sqlite3.connect("database1.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from data1 where username=?",(uid,))
    data1=cur.fetchone()
    con.commit()
    con.close()
    return render_template('index1.html', data1=data1)


# @app.route('/update_record/<string:id>',methods=["POST","GET"])
# def update_record(id):
    
    # con=sqlite3.connect("database1.db")
    # con.row_factory=sqlite3.Row
    # cur=con.cursor()
    # cur.execute("SELECT * FROM data1  where username=?",(id))
    # data1=cur.fetchone()
    # con.commit()
    # con.close()
    # if request.method=='POST':
    #     try:
    #         username=request.form['username']
    #         password=request.form['password']
    #         conn=sqlite3.connect("database1.db")
    #         cur=conn.cursor()
    #         cur.execute("update data1 set username=?,password=? where username=?",(username,password))
    #         conn.commit()  
    #     finally:
    #         return redirect(url_for("view_record"))
    # return render_template('update_record.html',data1=data1)

if __name__ == '__main__':
	app.run(debug=True)
 
