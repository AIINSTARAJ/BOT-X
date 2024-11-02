from flask import *

from flask_sqlalchemy import SQLAlchemy #type:ignore

from flask_mail import Mail, Message

from sqlalchemy.sql import func #type:ignore

from werkzeug.security import *

from random import *

import os

import time

import jwt

from dotenv import load_dotenv

from chat import bot

from bot import *

app = Flask(__name__,
            template_folder="assets/templates",
            static_folder="assets/static"
            )

load_dotenv('.env')

basedir = os.path.abspath(os.path.dirname(__file__))

secret_key = os.getenv('secret-key')

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir,'user.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = secret_key
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('mail')
app.config['MAIL_PASSWORD'] = os.getenv('pwd')
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
    token = db.Column(db.String(100),nullable = False)
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

def generate_token(name,mail,pwd):
    data = jwt.encode({'name': name,'mail':mail,'pwd':pwd},secret_key,algorithm='HS256')
    return data

def verify_token(token):
    try:
        data = jwt.decode(token,secret_key,algorithms=['HS256'])
        return data['name']
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

@app.before_request
def check_user():
    if request.path  in  ['/login','/signup','/code','/favicon.ico'] or request.path.startswith('/static/'):
        pass
    else:
        if 'token' not in session:
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
        d = session['token']
        if a and b and c and d:
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
            print('----- User Exists -----')
            flash("Username or e-mail address already exists. Please choose another username or e-mail!.","error")
            return redirect(url_for('login'))
        else:
            token = generate_token(name,mail,pwd)
            session['name'] = name
            session['mail'] = mail
            session['pwd'] = pwd
            session['token'] = token
            flash("Signup Sucessful!.","sucess")
            print('----- Signup Successful -----')
            global secret_code
            secret_code = randint(100000,999999)
            send_code(mail_=mail,code=secret_code,name=name)
            return redirect(url_for('verify'))
    return render_template('signup.html')


@app.route('/verify', methods = ['GET','POST'])
def verify():
    if request.method == 'POST':
        name = session['name']
        mail = session['mail']
        pwd = session['pwd']
        token = session['token']
        if name and mail and pwd and token:
            code = request.form['code']
            global secret
            if int(code) == secret_code:
                new_user = user(username = name, mail = mail, password = pwd, token = token)
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
                session.pop('token')
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
    d = session.get("token")
    if a and b and c and d:
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
                session['token'] = User.token
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
    return render_template('chat.html')

@app.errorhandler(404)
def not_found(error):
    return 'Page not Found'

@app.errorhandler(500)
def server_error(error):
    return 'Error in Server. Try Again Later'
    
@app.route('/bot-api', methods=['POST'])
def bot_api():
    auth = session.get('token')
    id = verify_token(auth)
    if id:
        data = request.get_json()
        message = data['message']
        response = bot(message) 
        return jsonify({ 'response': response ,'name': id})
    else:
        return jsonify({'error':'Unauthorized'})

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