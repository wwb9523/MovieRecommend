# -*- coding:utf-8 -*-
from DB import MyDB
from flask import Flask, render_template, request, jsonify, redirect,url_for,flash
import os,pickle
from flask.ext.login import LoginManager,login_user,current_user, login_required,logout_user
from itemBasedCF import ItemBasedCF
from User import User

app = Flask(__name__)
app.secret_key = 'super secret string'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# 用户记录表
users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'}
]


# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(username):
    mydb=MyDB()
    res=mydb.getUser(username)
    if res:
        user=User(res[0],username,res[2],res[1])
        # user.userName=username
        # user.id=res[0]
        # user.realName=res[1]
        # user.password=res[2]
        return user

# 如果用户名存在则构建一个新的用户类对象，并使用用户名作为ID
# 如果不存在，必须返回None
@login_manager.user_loader
def load_user(username):
    current_user=query_user(username)
    if current_user is not None:
        return current_user

@login_manager.request_loader
def load_user_from_request(request):
    username = request.args.get('token')
    current_user = query_user(username)
    if current_user is not None:
        return current_user

@app.route('/')
@login_required
def index():
     return 'Logged in as: %s' % current_user.get_id()

@app.route('/list')
@login_required
def list():
    itemCF=ItemBasedCF()
    pkl='pkl/itemSim.pkl'
    if os.path.exists(pkl):
        input = open(pkl, 'rb')
        itemSim = pickle.load(input)
        input.close()
        itemCF.W=itemSim
    else:
        itemCF.ItemSimilarity()
    data=itemCF.Recommend(int(current_user.get_id()))
    res=[]
    mydb=MyDB()
    for id,score in data.items():
        info=mydb.getMovInfo(id)
        if info:
            res.append(info)
    return render_template('list.html',realName=current_user.get_realName(),data=res)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = query_user(username)
        # 验证表单中提交的用户名和密码
        if user is not None and request.form['password'] == user.password:
            # 通过Flask-Login的login_user方法登录用户
            login_user(username)
            # 如果请求中有next参数，则重定向到其指定的地址，
            # 没有next参数，则重定向到"index"视图
            next = request.args.get('next')
            return redirect(next or url_for('list'))
        flash('Wrong username or password!')
    # GET 请求
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'

@app.route('/recommend')
@login_required
def recommend():
    if request.method == 'POST':
        tags_id=request.form.get('tag')
        word = request.form.get('word')
        file = request.files['data']
        return jsonify(results={"tags_id":tags_id,"word":word,"file":file.filename})

if __name__=='__main__':
    app.run('0.0.0.0',80,True)
