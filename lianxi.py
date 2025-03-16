from flask import Flask, render_template, redirect, url_for, request, flash  # 修正导入
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask,render_template,redirect,url_for
#导入flask相关模块
from flask import request
#导入request相关模块
import sqlite3
#导入python内置sql相关模块
from werkzeug.security import generate_password_hash
#导入密码哈表

app = Flask(__name__)
#新建app对象
app.secret_key='you _seret_key_here'
#用于加密会话

#初始化数据库
def init_db():
    conn=sqlite3.connect('blog.db')
    c=conn.cursor()
    #创建文章表
    c.execute('''CREATE TABLE IF NOT EXISTS posts
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 content TEXT NOT NULL)''')
    #创建匿名评论表
    c.execute('''CREATE TABLE IF NOT EXISTS comments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  post_id INTEGER NOT NULL,
                  comment TEXT NOT NULL,
                  FOREIGN KEY(post_id) REFERENCES posts(id))''')
    #创建用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()
# 首页，显示所有博客文章列表
@app.route('/')
def index ():
    conn=sqlite3.connect('blog.db')
    c=conn.cursor()
    c.execute('SELECT * FROM posts')
    posts=c.fetchall()
    conn.close()
    return render_template('index.html',posts=posts)
# 发布新博客文章的页面
@app.route('/new',methods=['GET','POST'])
def new_post():
    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']
        conn=sqlite3.connect('blog.db')
        c=conn.cursor()
        c.execute('INSERT INTO posts (title, content) VALUES (?, ?)',(title,content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('new.html')
# 查看单篇博客文章详情
@app.route('/post/<int:post_id>')
def view_post(post_id):
    conn=sqlite3.connect('blog.db')
    c=conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?',(post_id,))
    post=c.fetchone()
    c.execute('SELECT * FROM comments WHERE post_id =?',(post_id,))
    comments=c.fetchall()
    conn.close()
    if post:
        return render_template('post.html',post=post,comments=comments)
    return "文章未找到"
#文章删除功能
@app.route('/delete/<int:post_id>',methods=['POST'])
def delete_post(post_id):
    conn=sqlite3.connect('blog.db')
    c=conn.cursor()
    c.execute('DELETE FROM posts WHERE id =?',(post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/post/<int:post_id>/comment',methods=['POST'])
#匿名评论功能
def add_comment(post_id):
    comment=request.form.get('comment')
    if comment:
        conn=sqlite3.connect('blog.db')
        c=conn.cursor()
        c.execute('INSERT INTO comments (post_id, comment) VALUES (?,?)',(post_id,comment))
        conn.commit()
        conn.close()
        return redirect(url_for('view_post',post_id=post_id))
#注册功能
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form["password"]
        confirm_password=request.form['confirm_password']
        if not username or not password or not confirm_password:
            flash('所有字段为必填项','error')
        elif password != confirm_password:
            flash('两次输入密码不一致','error')
        else:
            try:
                conn=sqlite3.connect('blog.db')
                c=conn.cursor()
                c.execute('SELECT * FROM users WHERE username = ?',(username,))
                if c.fetchone():
                    flash('用户名已存在','error')
                else:
                    hashed_password=generate_password_hash(password)
                    c.execute('INSERT INTO users (username, password) VALUES (?, ?)',(username,hashed_password))
                    conn.commit()
                    conn.close()
                    flash('注册成功，请登录','success')
                    return redirect(url_for('login'))
            except sqlite3.Error as e:
                flash('数据库错误: '+ str(e),'error')
            finally:
                if conn:
                    conn.close()
        return redirect(url_for('register'))

    return render_template('register.html')


#登录功能
@app.route('/login',methods=['GET','POST'])
def login ():
    if request.method == 'POST':
        username= request.form['username']
        password=request.form['password']


        try:
            conn=sqlite3.connect('blog.db')
            c=conn.cursor()
            c.execute('SELECT * FROM users WHERE username = ?',(username,))
            user=c.fetchone()
            conn.close()
        except sqlite3.Error as e:
            flash('数据库错误：' + str(e), 'error')
            return render_template('login.html')
        finally:
            if conn:
                conn.close()


        if user and check_password_hash(user[2],password):
             flash('登录成功','success')
             return redirect(url_for('index'))
        else:
            flash ('用户名或密码错误','error')
            return render_template('login.html')
    return render_template('login.html')






if __name__ =='__main__':
    init_db()
    app.run(debug=True)
