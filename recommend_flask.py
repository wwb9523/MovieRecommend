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
# users = [
#     {'username': 'Tom', 'password': '111111'},
#     {'username': 'Michael', 'password': '123456'}
# ]


# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(userId):
    mydb=MyDB()
    res=mydb.getUser(userId)
    if res:
        user=User(res[0],res[1],res[3],res[2])
        # user.userName=username
        # user.id=res[0]
        # user.realName=res[1]
        # user.password=res[2]
        return user

# 如果用户名存在则构建一个新的用户类对象，并使用用户名作为ID
# 如果不存在，必须返回None
@login_manager.user_loader
def loaduser(username):
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
    print('list')
    itemCF=ItemBasedCF()
    pkl='pkl/itemSim.pkl'
    if os.path.exists(pkl):
        input = open(pkl, 'rb')
        itemSim = pickle.load(input)
        input.close()
        itemCF=itemSim
    else:
        itemCF.ItemSimilarity()
    data=itemCF.Recommend(int(current_user.get_userId()))
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
            login_user(user,True)
            print(user.get_id())
            # 如果请求中有next参数，则重定向到其指定的地址，
            # 没有next参数，则重定向到"index"视图
            #next = request.args.get('next')
            return redirect(url_for('list'))
        flash('Wrong username or password!')
    # GET 请求
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/canvas')
def canvas():
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    type=request.args.get('type')
    res=[]
    if not type:
        res=sse_sil()
    elif type=='1':
        res=sse_sil()
    elif type=='2':
        res=k_sil()
    elif type=='3':
        k=request.args.get('k')
        if k:
            res=label_count(k)
            return render_template('canvas.html', labelData=res, num=1000, center=4)
        else:
            return 'No K value!'
    return render_template('canvas.html',data=res,num=1000,center=4)
            # fname = os.path.splitext(f)
            # new = fname[0] + 'b' + fname[1]
            # os.rename(os.path.join(rt, f), os.path.join(rt, new))

def sse_sil(dir = './pkl/'):
    list = os.listdir(dir)
    res = []
    for i in range(0, len(list)):
        path = os.path.join(dir, list[i])
        if os.path.isfile(path):
            datas = list[i].split('_')
            if len(datas) == 4:
                if int(datas[0][3:]) == 1000 and int(datas[1]) == 4:
                    point = []
                    point.append(datas[2])
                    point.append(datas[3][:-4])
                    res.append(point)
    sorted(res)
    return res

def k_sil(dir = './pkl/'):
    list = os.listdir(dir)
    res = []
    d={}
    num={}
    for i in range(0, len(list)):
        path = os.path.join(dir, list[i])
        if os.path.isfile(path):
            datas = list[i].split('_')
            if len(datas) == 4:
                if int(datas[0][3:]) == 1000:
                    k=int(datas[1])
                    d.setdefault(k,0)
                    num.setdefault(k,0)
                    d[k]=d[k]+float(datas[3][:-4])
                    num[k]=num[k]+1
    for key,value in d.items():
        p=[]
        p.append(key)
        p.append(value/num[key])
        res.append(p)
    return res

def label_count(k,dir = './pkl/'):
    list = os.listdir(dir)
    res = []
    max=0
    file=''
    for i in range(0, len(list)):
        path = os.path.join(dir, list[i])
        if os.path.isfile(path):
            datas = list[i].split('_')
            if len(datas) == 4:
                if int(datas[1])==k and int(datas[0][3:]) == 1000:
                    if int(datas[3][-4])>max:
                        file=path
    input = open(file, 'rb')
    mk = pickle.load(input)
    input.close()
    label = mk._labels
    for i in range(mk._k):
        p=[]
        p.append(i+1)
        p.append(len(label==i+1))
        res.append(p)
    return res

if __name__=='__main__':
    app.run('0.0.0.0',80,True)
