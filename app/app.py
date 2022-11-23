from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from config import Config

app=Flask(__name__)
app.config.from_object(Config)


@app.route("/test")
def test():
    con=sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM tasks")
    rows=cur.fetchall()
    return render_template("test.html",rows=rows)

@app.route("/")
@app.route("/index")
def index():
    con=sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM tasks")
    rows=cur.fetchall()
    return render_template("index.html",rows=rows)

@app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method=='POST':
        name=request.form['name']
        task=request.form['task']
        priority= request.form['priority']
        
        con=sql.connect("database.db")
        cur=con.cursor()
        cur.execute("insert into tasks(NAME,TASK,PRIORITY) values (?,?,?)",(name,task,priority))
        con.commit()
        flash('User Added','success')
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:uid>",methods=['POST','GET'])
def edit_user(uid):
    if request.method=='POST':
        name=request.form['name']
        task=request.form['task']
        priority= request.form['priority']
        completed: bool = bool(request.form.get('checkbox', False))
        con=sql.connect("database.db")
        cur=con.cursor()
        cur.execute("update tasks set NAME=?,TASK=?,PRIORITY=?, COMPLETED=? where UID=?",(name,task,priority,completed,uid))
        con.commit()
        flash('User Updated','success')
        return redirect(url_for("index"))
    con=sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from tasks where UID=?",(uid,))
    rows=cur.fetchone()
    return render_template("edit_user.html",rows=rows)
    
@app.route("/delete_user/<string:uid>",methods=['GET'])
def delete_user(uid):
    con=sql.connect("database.db")
    cur=con.cursor()
    cur.execute("delete from tasks where UID=?",(uid,))
    con.commit()
    flash('User Deleted','warning')
    return redirect(url_for("index"))
    
if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)