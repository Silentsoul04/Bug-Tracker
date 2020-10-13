from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_mail import Mail, Message
from flask_migrate import Migrate, MigrateCommand, Manager
from flask_apscheduler import APScheduler
from datetime import datetime


app = Flask(__name__)
scheduler = APScheduler()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugtracker.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'THISISASECRET'

#parte de email
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USE_SSL'] = False

app.config['MAIL_USERNAME'] = 'costinvlad2@gmail.com'   
app.config['MAIL_PASSWORD'] = 'sudbucuresti'
app.config['MAIL_DEFAULT_SENDER'] = ('Bug Tracker','costinvlad2@gmail.com') # pentru a trimite mai multe emailuri de pe mai multe adrese de email se trece in tupple ('adresa@gmail.com')
app.config['MAIL_MAX_EMAILS'] = None

#app.config.from_json('config.json')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# parte de view-uri unde sunt controllere
from views import *
#app.config.from_json("config.json")


#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    
    #job ce trimite un email celor care nu au inchise buguri, proiecte, etc
    scheduler.add_job(id = 'Scheduled Project Exceeded', func = task_expire, trigger = 'interval', seconds = 86400)
    scheduler.start()
    
    app.run(use_reloader=False)

    #manager.run()
