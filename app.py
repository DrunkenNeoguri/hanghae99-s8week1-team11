from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient(
    "mongodb+srv://aaronkim:aa0134679@cluster0.l0k2g.mongodb.net/?retryWrites=true&w=majority")
db = client.dbsparta_plus_week4


@app.route('/')
def home():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route("/main")
def mainpage():
    sports_list = list(db.testdata.find({}, {"_id": False}))
    return render_template('main.html', sports_list=sports_list)


@app.route("/detail")
def detailpage():
    sports_list = list(db.testdata.find({}, {"_id": False}))
    return render_template('detail.html', sports_list=sports_list)


@app.route('/login', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one(
        {'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/signup/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(
        password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/signup/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/word', methods=["GET"])
def web_text_get():
    # 여러개 찾기 - _id 값은 제외하고 출력
    all_texts = list(db.dbsparta.find({}, {'_id': False}))
    print(all_texts)
    return jsonify({'text': all_texts})


@app.route('/text')
def text():
    return render_template('text.html')


@app.route('/text', methods=["POST"])
def web_text_post():
    # return render_template("text.html")

    sportname_receive = request.form['sportname_give']
    username_receive = request.form['username_give']
    select1_receive = request.form['select1_give']
    select2_receive = request.form['select2_give']
    text_receive = request.form['text_give']
    link_receive = request.form['link_give']

    doc = {
        'sportname': sportname_receive,
        'username': username_receive,
        'select1': select1_receive,
        'select2': select2_receive,
        'text': text_receive,
        'link': link_receive
    }

    db.dbsparta.insert_one(doc)

    return jsonify({'msg': '게시글 작성이 완료되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
