from flask import *

from bot import *

from flask_sqlalchemy import SQLAlchemy #type:ignore

from flask_mail import *

from sqlalchemy.sql import func #type:ignore

from werkzeug.security import *

from random import *

import os

import time

app = Flask(__name__,
            template_folder="assets/templates",
            static_folder="assets/static"
            )


basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir,'data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.getenv("secret-key")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'tomiwakuteyi@gmail.com'
app.config['MAIL_PASSWORD'] = 'cdps zkto bwcj psqs'
app.config['MAIL_DEFAULT_SENDER'] = 'Ayotomiwa Joel Kuteyi <tomiwakuteyi@gmail.com>'
app.config['MAIL_DEBUG'] = False
app.config['MAIL_TIMEOUT'] = 600

db = SQLAlchemy(app)

mail = Mail(app)

class user(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(12),nullable = False)
    password = db.Column(db.String(128),nullable = False)
    mail = db.Column(db.String(48),nullable = False)
    auth_date = db.Column(db.DateTime(timezone=True), server_default = func.now())

    def __repr__(self):
        return f'<user {self.username}>'
    
print('-------- A.I Instaraj BOT-X Project ------')


def send_code(mail_,code,name):
    msg = Message('BOT-X Verification Code',
                  recipients=[mail_],
                  )
    code_temp = render_template('code.html',code = code,name=name)
    msg.html = code_temp
    try:
        if mail.send(msg) is True:
            print(f'Mail Successfully Sent to {mail_} ----')
    except Exception as E:
        print(f'----- Failed to send code-----{E}')
    return 'Email Succesfully Send'


@app.before_request
def check_user():
    if request.path not in  ['/login','/signup','/static/css/styles.css','/static/js/app.js','/static/data/bg-main.jpg','/static/css/login.css','/static/css/signup.css']:
        if 'name' not in session:
           return redirect(url_for('signup'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/signup',methods = ['GET','POST'])
def signup():
    try:
        a = session["name"]
        b = session["mail"]
        c = session['pwd']
        if a and b and c:
            return redirect(url_for('chat'))
    except Exception as E:
        print('----- User Session Not Found ----')
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        pwd = request.form['pwd']
        print('---- Form Inputs Successfully Sent ----')
        pwd = generate_password_hash(pwd,'scrypt')
        exist_user = user.query.filter_by(username = name).first()
        exist_mail = user.query.filter_by(mail=mail).first()
        if exist_user or exist_mail:
            print('----- User Exists ----')
            flash("Username or e-mail address already exists. Please choose another username or e-mail!.","error")
            return redirect(url_for('login'))
        else:
            session['name'] = name
            session['mail'] = mail
            session['pwd'] = pwd
            flash("Signup Sucessful!.","sucess")
            print('----- Signup Successful -----')
            global secret
            secret = randint(100000,999999)
            send_code(mail_=mail,code=secret,name=name)
            return redirect(url_for('verify'))
            
    return render_template('signup.html')

@app.route('/verify', methods = ['GET','POST'])
def verify():
    if request.method == 'POST':
        name = session['name']
        mail = session['mail']
        pwd = session['pwd']
        if name and mail and pwd:
            code = request.form['code']
            global secret
            if int(code) == secret:
                new_user = user(username = name, mail = mail, password = pwd)
                db.session.add(new_user)
                db.session.commit() 
                print(f'--- Verification Completed --- {name}')
                flash("Verification Successful",'sucess')
                return redirect(url_for('login'))
            else:
                print(f' Wrong Code Input by User -- {name} -- ')
                session.pop('name')
                session.pop('mail')
                session.pop('pwd')
                return redirect(url_for('signup'))
        else:
            print('--- Error in getting Sessions ----')
            return redirect(url_for('signup'))
    return render_template('verify.html')

@app.route('/login',methods = ["GET","POST"])
def login():
    a = session.get("name")
    b = session.get("mail")
    c = session.get("pwd")
    if a and b and c:
        try:
            return redirect(url_for('chat'))
        except Exception as E:
            print('------- Error in accessing Chat Routes ------')
    else:
        if request.method == "post":
            mail = request.form['mail']
            pwd = request.form['pwd']
            User = user.query.filter_by(mail = mail).first()
            p = check_password_hash(User.password,pwd)
            if user and p:
                flash('Login Successful!','sucess')
                session['name'] = User.username
                session['mail'] = User.mail
                session['pwd'] = User.password
                try:
                    return redirect(url_for("chat"))
                except Exception as E:
                    print('----- Failed to Access Chat Routes-----')
            else:
                print(f'---- Password Incorrect --- {User.username}')
                flash('Invalid Username or Password', 'error')
                return redirect(url_for("login"))
            
        return render_template('login.html')
    
@app.route('/chat',methods = ['GET','POST'])
def chat():
    return render_template('signin.html')

@app.route('/bot-response', methods=['POST'])
def bot_response():
    data = request.get_json()
    message = data['message']
    response = chat_bot(message)
    return jsonify({ 'response': response })

def chat_bot(msg):
    knowledge_base: dict = load_knowledge_base('assets/static/data/knowledge_base.json')

    user_input: str = msg

    best_match = find_best_match(user_input, [q["QUESTION"] for q in knowledge_base["RESPONSES"]])

    if best_match:
        answer: str = get_answer_for_question(best_match, knowledge_base)
        return answer
    else:
        return None
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')