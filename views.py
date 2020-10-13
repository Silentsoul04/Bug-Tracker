#Status in db :     1 - Open,   2 - In development, 3 - Closed
#Priority in db :   1- Normal , 2- Alert ,          3 - Critic
#Users in db 1- Admin , 2 - SuperUser , 3 - Normal User
from app import app, db, mail, scheduler
from model import Users, Projects, Bugs, Feature, Settings, Rights, Email
from flask import  render_template, redirect, url_for,request, abort, flash
from forms import RegisterForm, LoginForm, ResetPasswordForm, RestorePasswordForm, AddProjectForm, EditProjectForm, AddBugsForm, EditBugForm, AddFeatureForm,EditFeatureForm, AddUserForm, EditUserForm, SettingsForm, RightsForm, EmailForm, GenerateTopUsersBugs, GenerateTopUsersFeature, GenerateTopUsersClosingProjects, GenerateTopProjectsBugs, GenerateTopProjectsBugsDetailed
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from helper import Helper
import datetime
import random
import datetime
from sqlalchemy import desc
import base64
import sys
import json
from sqlalchemy import or_
from sqlalchemy import text
# task-uri de rulat

#de puse pe fiecare email valoarea din baza de date  acolo unde se trimite email
# in sender se pune email-ul care trimite adica se face select din baza de date

def task_expire():
    with app.app_context():
        date_now = datetime.datetime.now()
        projects = Projects.query.join(Users, Users.id == Projects.user_id, isouter = True).filter(Projects.finish_date < date_now, Projects.status != 3).all()
        bugs = Bugs.query.join(Users, Users.id == Bugs.user_id, isouter = True).filter(Bugs.finish_date < date_now, Bugs.status != 3).all()
        features = Feature.query.join(Users, Users.id == Feature.user_id, isouter = True).filter(Feature.finish_date < date_now, Feature.status != 3).all()
        #trimite email ca nu a fost indeplinit termenul pentru proiect
        if projects:
            for project in projects:
                msg = Message('Critical Alert', recipients=[project.users.email])
                msg.body = 'Delivery date for a project with title: {} has been exceeded'.format(project.title)
                try:
                    mail.send(msg)
                except:
                    pass

        # trimite email ca nu a fost indeplinit termenul pentru bug
        if bugs:
            for bug in bugs:
                msg = Message('Critical Alert', recipients=[bug.users.email])
                msg.body = 'Delivery date for a bug with title: {} has been exceeded'.format(bug.title)
                try:
                    mail.send(msg)
                except:
                    pass

        if features:
            for feature in features:
                msg = Message('Critical Alert', recipients=[feature.users.email])
                msg.body = 'Delivery date for a feature with title: {} has been exceeded'.format(feature.title)
                try:
                    mail.send(msg)
                except:
                    pass
# sfarsit task-uri
 
@app.route('/')
@login_required
def index():
    helper = Helper()
    total_users              = Users.query.count()
    total_opened_projects    = Projects.query.filter(or_(Projects.status == 1, Projects.status == 2)).count() 
    total_opened_feature     = Feature.query.filter(or_(Feature.status == 1, Feature.status == 2)).count()
    total_opened_bugs        = Bugs.query.filter(or_(Bugs.status == 1, Bugs.status == 2)).count()
    total_opened             = total_opened_projects + total_opened_feature + total_opened_bugs 

    total_closed_projects    = Projects.query.filter(Projects.status == 3).count() 
    total_closed_feature     = Feature.query.filter(Feature.status == 3).count()
    total_closed_bugs        = Bugs.query.filter(Bugs.status == 3).count()
    total_closed             = total_closed_projects +  total_closed_feature + total_closed_bugs

    total_expired_projects    = Projects.query.filter(Projects.finish_date < datetime.datetime.now()).count() 
    total_expired_feature     = Feature.query.filter(Feature.finish_date < datetime.datetime.now()).count()
    total_expired_bugs        = Bugs.query.filter(Bugs.finish_date < datetime.datetime.now()).count()

    total_expired = total_expired_projects +  total_expired_feature + total_expired_bugs

    _currentMonth = datetime.datetime.now().month
    currentMonth = helper.getCurrentMonth(_currentMonth)

    given_date = datetime.datetime.today().date()
    
    _last_day = helper.last_day_of_month(given_date)
    last_day = _last_day.day
    month = _last_day.month
    year  = _last_day.year

    first_day = datetime.date(year,month,1)
    current_day = datetime.datetime.today().day

    label_month_list = []
    
    for day in range(0,current_day):
        label_month_list.append(str(day + 1) + " {}".format(currentMonth))

    
    _total_bugs_max = Bugs.query.count()
    #pentru axa oy
    total_bugs_max = helper.display_max_bugs_graph(_total_bugs_max)
    
    #inceput pentru a aduce bugurile pe zile pana la ziua curenta
    today = datetime.datetime.today()
    days_cur_month = helper.days_cur_month()
    # intoarce data si rezultatul aici
    #_total_bugs_data = db.session.query(Bugs,db.func.count(Bugs.id), Bugs.start_date).filter(Bugs.start_date >= first_day, Bugs.start_date <= today).group_by(Bugs.start_date).all()
    list_total_data = []

    for day in range(1,current_day + 1):
        #apelam de fiecare data cu ziua curenta si dam ca parametru ca sa putem face countul de buguri pe fiecare luna
        date_current = datetime.datetime(year,month,day,0,0,0,0)
        _total_bugs_data = db.session.query(Bugs,db.func.count(Bugs.id)).filter(Bugs.start_date == date_current).first()
        list_total_data.append(_total_bugs_data[1])


    #inceput pentru a aduce datele in grafic in ultimele 6 luni cate proiecte sunt
    range_month = helper.get_range_month(month)
    label_month_name = helper.get_range_month_name(range_month)
    list_project_data = []
    for month_item in range_month:
        date_format_first_day = datetime.datetime(year,month_item,1,0,0,0,0)
        date_format_last_day  = helper.last_day_of_month(date_format_first_day)
        _list_project_data = db.session.query(Projects,db.func.count(Projects.id)).filter(Projects.start_date >= date_format_first_day, Projects.start_date <= date_format_last_day).first()
        list_project_data.append(_list_project_data[1])

    #inceput top useri 
    total_projects_closed = db.session.query(db.func.count(Projects.user_id)).filter(Projects.user_id == Users.id, Projects.status == 3).label('total_projects_closed')
    total_bugs_closed     = db.session.query(db.func.count(Bugs.user_id)).filter(Bugs.user_id == Users.id, Bugs.status == 3).label('total_bugs_closed')
    total_feature_closed  = db.session.query(db.func.count(Feature.user_id)).filter(Feature.user_id == Users.id, Bugs.status == 3).label('total_feature_closed')

    
 
    all_users = db.session.query(Users, total_projects_closed, total_bugs_closed,total_feature_closed, ((total_projects_closed + total_bugs_closed + total_feature_closed)).label('average')).group_by('average', Users.email).order_by(desc('average')).all()

    return render_template('index.html', current_user = current_user, 
                            total_users = total_users, total_opened = total_opened, 
                            total_closed = total_closed, total_expired = total_expired, currentMonth = currentMonth, 
                            label_month_list = label_month_list, current_day = current_day,total_bugs_max = total_bugs_max,
                            list_total_data = list_total_data, label_month_name = label_month_name, list_project_data = list_project_data,
                            all_users = all_users)

#aici se face login-ul propriu zis
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.username.data).first()
        if not user:
            return render_template('login.html', form = form, message = 'Login Failed')

        # exista utilizatorul acum verificam parola
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', form = form, message = 'Login Failed')
    else:
        return render_template('login.html', form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            return render_template('register.html', form = form, message = 'Register Failed! Passwords does not correspond') 
        
        new_user = Users(firstname=form.first_name.data, lastname = form.last_name.data , email=form.email.data, password = generate_password_hash(form.password.data), rol = 3)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
        
    return render_template('register.html', form = form)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #verific daca exista utilizatorul 
        user = Users.query.filter_by(email=form.email.data).first() 
        if not user:
            return render_template('password.html', form = form, message='The email does not exist in database!')
        
        sent_date = datetime.datetime.now().strftime('%H%M%S')
        msg = Message('Password Reset', recipients=[user.email])
        msg.body = 'Password Reset Link 127.0.0.1:5000/reset_password/{}/{}'.format(user.password, sent_date)
        try:
            mail.send(msg)
            return render_template('password.html', form = form, message = "Email has been sent succesfully! Check your email")
        except:
            return render_template('password.html', form = form, message = "Error in sending email!")


    return render_template('password.html', form = form)


@app.route('/reset_password/<token>/<expire>', methods=['GET', 'POST'])
def reset_password(token,expire):

    form = RestorePasswordForm()
    user = Users.query.filter_by(password=token).first()
    
    #verific daca token-ul este bun
    if not user:
        abort(404)

    #se expira linkul din email
    enter_date = datetime.datetime.now().strftime('%H%M%S')

    expire_token = datetime.datetime.strptime(enter_date, "%H%M%S") - datetime.datetime.strptime(expire, "%H%M%S")

    expire_token = expire_token.seconds / 60
    
    #daca au trecut 60 de minute primeste pe notfound deci nu mai are access la pagina
    if expire_token > 60:
        return redirect(url_for('notfound'))
        
    
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            return render_template('reset_password.html', form = form, token = token, expire = expire ,message = 'Register Failed! Password does not correspond') 
        
         
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        return redirect(url_for('login')) 

    return render_template('reset_password.html', form = form, token = token, expire = expire)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/users')
@login_required
def users():
    auth_user = current_user

    users = Users.query.filter(Users.id == auth_user.id, Users.rol == 1).first() 
    # verific daca pot sa am drepturi
    if not users:
        return redirect(url_for('unauthorized'))
    
    total_projects_opened = db.session.query(db.func.count(Projects.user_id)).filter(Projects.user_id == Users.id, Projects.status != 3).label('total_projects_opened')
    total_bugs_opened = db.session.query(db.func.count(Bugs.user_id)).filter(Bugs.user_id == Users.id, Bugs.status != 3).label('total_bugs_opened')
    total_projects_closed = db.session.query(db.func.count(Projects.user_id)).filter(Projects.user_id == Users.id, Projects.status == 3).label('total_projects_closed')
    total_bugs_closed = db.session.query(db.func.count(Bugs.user_id)).filter(Bugs.user_id == Users.id, Bugs.status == 3).label('total_bugs_closed')
    all_users = db.session.query(Users,total_projects_opened, total_bugs_opened, total_projects_closed, total_bugs_closed).group_by(Users.id).all()
    

    return render_template('user.html', all_users = all_users)


@app.route('/add_users', methods=['GET', 'POST'])
@login_required
def add_users():
    form = AddUserForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            return render_template('add_user.html', form = form, message = 'Failed! Passwords does not correspond') 
        
        new_user = Users(firstname=form.first_name.data, lastname = form.last_name.data , email=form.email.data, password = generate_password_hash(form.password.data), rol = form.role.data)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('users'))
        
    return render_template('add_user.html', form = form)


@app.route('/delete_users/<int:id>')
@login_required
def delete_users(id):
    deleted_users = Users.query.filter_by(id = id).first()
    db.session.delete(deleted_users)
    db.session.commit()
    #dupa stergere se face redirect catre users
    return redirect(url_for('users'))


@app.route('/edit_users/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_users(id):
    form = EditUserForm()
    edited_users = Users.query.filter_by(id = id).first()
    if request.method == 'GET':
        form.first_name.data = edited_users.firstname
        form.last_name.data  = edited_users.lastname
        form.email.data      = edited_users.email
        form.role.default    = edited_users.rol
        form.role.process_data(str(edited_users.rol))


    if request.method == 'POST':
        if form.validate_on_submit():
            if form.password.data != form.confirm_password.data:
                return render_template('edit_user.html', form = form, edited_users = edited_users ,message = 'Failed! Passwords does not correspond') 
            
            edited_users.firstname = form.first_name.data
            edited_users.lastname = form.last_name.data
            edited_users.email    = form.email.data
            edited_users.password = generate_password_hash(form.password.data)
            edited_users.rol      = form.role.data

            db.session.commit()

            return redirect(url_for('users'))

    return render_template('edit_user.html', form = form, edited_users = edited_users)

@app.route('/projects')
@login_required
def projects():
    users = Users.query.all()
    projects = Projects.query.join(Users, Users.id == Projects.user_id).order_by(Projects.start_date.desc()).all()

    auth_user = current_user 
    

    return render_template('projects.html', projects = projects, users = users)

@app.route('/add_project',  methods=['GET', 'POST'])
@login_required
def add_project():
    form = AddProjectForm()
    form.start_date.data = datetime.datetime.now().strftime('%d/%m/%Y')
    # se verifica daca utilizatorul prin rolul lui are dreptul sa adauge un proiect
    helper = Helper()

    canAddNewProjectSuperUser = helper.canAddNewProjectSuperUser()
    canAddNewProjectNormalUser = helper.canAddNewProjectNormalUser()
    
    users_current = helper.getCurrentUser(current_user.id)

    if users_current.rol == 2:
        if not canAddNewProjectSuperUser:
            return redirect(url_for('unauthorized'))

    if users_current.rol == 3:
        if not canAddNewProjectNormalUser:
            return redirect(url_for('unauthorized'))

    #
    
    if form.validate_on_submit():

        project_title = form.project_title.data
        project_description = form.project_description.data
        start_date = form.start_date.data
        expected_date = form.expected_date.data
        finish_date = form.finish_date.data
        user_id = form.user.data.id
        status = form.status.data
        priority = form.priority.data

        start_date_formated = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        expected_date_format = datetime.datetime.strptime(expected_date, '%d/%m/%Y') 
        finish_date_format = datetime.datetime.strptime(finish_date, '%d/%m/%Y') 

        if (start_date_formated > expected_date_format) or (start_date_formated > finish_date_format):
            return render_template('add_project.html', form = form, message = 'Start Date cannot be smaller than Finnish Date or Expected Date')

        # sa nu las sa treaca nimic la expected date si finnish date
        

        new_project = Projects(user_id=user_id, title = project_title, description = project_description,
                               start_date = start_date_formated, expected_date= expected_date_format, finish_date = finish_date_format,
                               status = status, typeProject = priority)
        
        db.session.add(new_project)
        db.session.commit()

        #trimitem email utilizatorului care are atribuit proiectul
        isAllow = helper.isSendEmailOnNewProject(user_id)
        if isAllow:
            msg = Message('Project assigned', recipients=[form.user.data.email])
            msg.body = 'A new project with title {} has been assigned to you'.format(project_title)
            try:
                mail.send(msg)
            except:
                pass
        #sfarsit functie de trimis email
        

        return redirect(url_for('projects'))


    return render_template('add_project.html', form = form)


@app.route('/delete_project/<int:id>')
@login_required
def delete_Project(id):
    #se verifica daca se utilizatorul are dreptul sa stearga un proiect
    helper = Helper()
    canDeleteProjectSuperUser = helper.canDeleteProjectSuperUser()
    canDeleteProjectNormalUser = helper.canDeleteProjectNormalUser()
    
    users_current = helper.getCurrentUser(current_user.id)

    if users_current.rol == 2:
        if not canDeleteProjectSuperUser:
            return redirect(url_for('unauthorized'))

    if users_current.rol == 3:
        if not canDeleteProjectNormalUser:
            return redirect(url_for('unauthorized'))
    
    # se selecteaza id-ul
    deleted_project = Projects.query.filter_by(id = id).first()

    db.session.delete(deleted_project)
    db.session.commit()
    #dupa stergere se face redirect catre projects
    return redirect(url_for('projects'))


@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    form = EditProjectForm()
    #.join(Users, Users.id == Projects.user_id,isouter=True)
    projects = Projects.query.filter_by(id = id).first()
    if request.method == 'GET':
        
        form.project_description.data = projects.description
        
        #bucata asta pune pe default in select field valoarea din baza de date 
        form.user.default = projects.user_id
        form.user.process_formdata(str(projects.user_id))
        
        form.status.default = projects.status
        form.status.process_formdata(str(projects.status))

        form.priority.default = projects.typeProject
        form.priority.process_formdata(str(projects.typeProject))
        
    if request.method == 'POST':
        if form.validate_on_submit():
            projects.title = form.project_title.data
            projects.description = form.project_description.data
            
            start_date = form.start_date.data
            stard_date_formated = datetime.datetime.strptime(start_date, '%d/%m/%Y') 
            projects.start_date = stard_date_formated

            expected_date = form.expected_date.data
            expected_date_formated = datetime.datetime.strptime(expected_date, '%d/%m/%Y') 
            projects.expected_date = expected_date_formated

            finish_date = form.finish_date.data
            finish_date_formated = datetime.datetime.strptime(finish_date, '%d/%m/%Y') 
            projects.finish_date = finish_date_formated

            

            projects.user_id = form.user.data.id
            projects.status = form.status.data
            projects.typeProject = form.priority.data

            #validare ca sa nu se pune o data anterioara
            if (stard_date_formated > expected_date_formated) or (stard_date_formated > finish_date_formated):
                return render_template('edit_project.html', form = form, projects = projects ,message = 'Start Date cannot be smaller than Finnish Date or Expected Date')

            db.session.commit()
                    
            #trimitem email utilizatorului care are atribuit proiectul
            helper = Helper()
            isAllow = helper.isSendEmailOnModifyProject(projects.user_id)
            if isAllow:
                msg = Message('Project updated' ,recipients=[form.user.data.email])
                msg.body = 'A new project with title {} has been updated'.format(form.project_title.data)
                try:
                    mail.send(msg)
                except:
                    pass
            #sfarsit functie de trimis email

            return redirect(url_for('projects'))  

    return render_template('edit_project.html', form = form, projects = projects)           



@app.route('/bugs')
@login_required
def bugs():
    users = Users.query.all()
    
    projects = Projects.query.filter(Projects.status != 3).all()

    bugs = Bugs.query.join(Users, Users.id == Bugs.user_id).join(Projects, Projects.id == Bugs.project_id).order_by(Bugs.start_date.desc()).all()

    auth_user = current_user  
    
    return render_template('bugs.html', bugs = bugs, projects = projects, users = users)


@app.route('/add_bugs', methods=['GET', 'POST'])
@login_required
def add_bugs():
    form = AddBugsForm()
    projects = Projects.query.filter(Projects.status != 3).all()
    if not projects:
        return redirect(url_for('error'))

    form.start_date.data = datetime.datetime.now().strftime('%d/%m/%Y')


    # se verifica daca utilizatorul prin rolul lui are dreptul sa adauge un proiect
    helper = Helper()

    canAddNewBugSuperUser = helper.canAddNewBugSuperUser()
    canAddNewBugNormalUser = helper.canAddNewBugNormalUser()
    
    users_current = helper.getCurrentUser(current_user.id)

    if users_current.rol == 2:
        if not canAddNewBugSuperUser:
            return redirect(url_for('unauthorized'))

    if users_current.rol == 3:
        if not canAddNewBugNormalUser:
            return redirect(url_for('unauthorized'))


    if form.validate_on_submit():
                
        bug_title = form.bug_title.data
        bug_description = form.bug_description.data
        start_date = form.start_date.data
        expected_date = form.expected_date.data
        finish_date = form.finish_date.data
        user_id = form.user.data.id
        project_id = form.projects.data.id
        status = form.status.data
        priority = form.priority.data

        start_date_formated = datetime.datetime.strptime(start_date, '%d/%m/%Y') 
        expected_date_format = datetime.datetime.strptime(expected_date, '%d/%m/%Y') 
        finish_date_format = datetime.datetime.strptime(finish_date, '%d/%m/%Y') 

        if (start_date_formated > expected_date_format) or (start_date_formated > finish_date_format):
            return render_template('add_bug.html', form = form, message = 'Start Date cannot be smaller than Finnish Date or Expected Date')

        new_bug = Bugs(user_id=user_id, project_id = project_id , title = bug_title, description = bug_description,
                               start_date = start_date_formated, expected_date= expected_date_format, finish_date = finish_date_format,
                               status = status, typeProject = priority)
        
        db.session.add(new_bug)
        db.session.commit()

        #trimitem email utilizatorului care are atribuit proiectul
        isAllow = helper.isSendEmailOnNewBug(user_id)
        if isAllow:
            msg = Message('Bug assigned', recipients=[form.user.data.email])
            msg.body = 'A new bug with title {} for project {} has been assigned'.format(form.bug_title.data, form.projects.data.title)
            try:
                mail.send(msg)
            except:
                pass
            #sfarsit functie de trimis email
        
        return redirect(url_for('bugs'))


    return render_template('add_bug.html', form = form)


@app.route('/delete_bug/<int:id>')
@login_required
def delete_Bug(id):
    helper = Helper()
    canDeleteBugSuperUser = helper.canDeleteBugSuperUser()
    canDeleteBugNormalUser = helper.canDeleteBugNormalUser()
    users_current = helper.getCurrentUser(current_user.id)

    if users_current.rol == 2:
        if not canDeleteBugSuperUser:
            return redirect(url_for('unauthorized'))

    if users_current.rol == 3:
        if not canDeleteBugNormalUser:
            return redirect(url_for('unauthorized'))

    # se selecteaza id-ul
    deleted_bug = Bugs.query.filter_by(id = id).first()

    db.session.delete(deleted_bug)
    db.session.commit()
    #dupa stergere se face redirect catre projects
    return redirect(url_for('bugs'))


@app.route('/edit_bug/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_bug(id):
    
    form = EditBugForm()
    bugs = Bugs.query.filter_by(id = id).first()
    if request.method == 'GET':
        form.bug_title.data = bugs.description
        
        #bucata asta pune pe default in select field valoarea din baza de date 
        form.projects.default = bugs.project_id
        form.projects.process_formdata(str(bugs.project_id))
        
        form.bug_description.data = bugs.description
        
        form.user.default = bugs.user_id
        form.user.process_formdata(str(bugs.user_id))
        
        form.status.default = bugs.status
        form.status.process_formdata(str(bugs.status))

        form.priority.default = bugs.typeProject
        form.priority.process_formdata(str(bugs.typeProject))
        
    if request.method == 'POST':
        if form.validate_on_submit():
            bugs.title = form.bug_title.data
            bugs.description = form.bug_description.data
            
            start_date = form.start_date.data
            stard_date_formated = datetime.datetime.strptime(start_date, '%d/%m/%Y') 
            bugs.start_date = stard_date_formated

            expected_date = form.expected_date.data
            expected_date_formated = datetime.datetime.strptime(expected_date, '%d/%m/%Y') 
            bugs.expected_date = expected_date_formated

            finish_date = form.finish_date.data
            finish_date_formated = datetime.datetime.strptime(finish_date, '%d/%m/%Y') 
            bugs.finish_date = finish_date_formated

            bugs.project_id = form.projects.data.id
            bugs.user_id = form.user.data.id
            bugs.status = form.status.data
            bugs.typeProject = form.priority.data
            
            if (stard_date_formated > expected_date_formated) or (stard_date_formated > finish_date_formated):
                return render_template('edit_bug.html', form = form, bugs = bugs ,message = 'Start Date cannot be smaller than Finnish Date or Expected Date')


            db.session.commit()
                    
            #trimitem email utilizatorului care are atribuit proiectul
            helper = Helper()
            isAllow = helper.isSendEmailOnModifyBug(bugs.user_id)
            if isAllow: 
                msg = Message('Bug updated', recipients=[form.user.data.email])
                msg.body = 'A new bug with title {} for project {} has been updated'.format(form.bug_title.data, form.projects.data.title)
                try:
                    mail.send(msg)
                except:
                    pass
            #sfarsit functie de trimis email

            return redirect(url_for('bugs')) 

    return render_template('edit_bug.html',form = form, bugs = bugs)


@app.route('/features')
@login_required
def features():    
    users = Users.query.all()
    
    projects = Projects.query.filter(Projects.status != 3).all()

    features = Feature.query.join(Users, Users.id == Feature.user_id).join(Projects, Projects.id == Feature.project_id).order_by(Feature.start_date.desc()).all()
    
    auth_user = current_user
    
    return render_template('features.html', users = users , projects = projects, features = features)


@app.route('/add_feature', methods=['GET', 'POST'])
@login_required
def add_feature():
    form = AddFeatureForm()
    projects = Projects.query.filter(Projects.status != 3).all()
    if not projects:
        return redirect(url_for('error'))

    
    # se verifica daca utilizatorul prin rolul lui are dreptul sa adauge un proiect
    helper = Helper()

    canAddNewFeatureSuperUser = helper.canAddNewFeatureSuperUser()
    canAddNewFeatureNormalUser = helper.canAddNewFeatureNormalUser()
    
    users_current = helper.getCurrentUser(current_user.id)

    if users_current.rol == 2:
        if not canAddNewFeatureSuperUser:
            return redirect(url_for('unauthorized'))

    if users_current.rol == 3:
        if not canAddNewFeatureNormalUser:
            return redirect(url_for('unauthorized'))

    

    form.start_date.data = datetime.datetime.now().strftime('%d/%m/%Y')
    if form.validate_on_submit():
                
        feature_title = form.feature_title.data
        feature_description = form.feature_description.data
        start_date = form.start_date.data
        expected_date = form.expected_date.data
        finish_date = form.finish_date.data
        user_id = form.user.data.id
        project_id = form.projects.data.id
        status = form.status.data
        priority = form.priority.data

        start_date_formated = datetime.datetime.strptime(start_date, '%d/%m/%Y') 
        expected_date_format = datetime.datetime.strptime(expected_date, '%d/%m/%Y') 
        finish_date_format = datetime.datetime.strptime(finish_date, '%d/%m/%Y')

        if (start_date_formated > expected_date_format) or (start_date_formated > finish_date_format):
            return render_template('add_feature.html', form = form, message = 'Start Date cannot be smaller than Finnish Date or Expected Date') 

        new_feature = Feature(user_id=user_id, project_id = project_id , title = feature_title, description = feature_description,
                               start_date = start_date_formated, expected_date= expected_date_format, finish_date = finish_date_format,
                               status = status, typeProject = priority)
        
        db.session.add(new_feature)
        db.session.commit()

        #trimitem email utilizatorului care are atribuit proiectul
        isAllow = helper.isSendEmailOnNewFeature(user_id)
        if isAllow:
            msg = Message('Feature assigned', recipients=[form.user.data.email])
            msg.body = 'A new feature with title {} for project {} has been assigned'.format(form.feature_title.data, form.projects.data.title)
            try:
                mail.send(msg)
            except:
                pass
        #sfarsit functie de trimis email
        
        return redirect(url_for('features'))

    
    return render_template('add_feature.html', form = form)


@app.route('/delete_feature/<int:id>')
@login_required
def delete_feature(id):
    
    helper = Helper()
    canDeleteFeatureSuperUser = helper.canDeleteFeatureSuperUser()
    canDeleteFeatureNormalUser = helper.canDeleteFeatureNormalUser()
    users_current = helper.getCurrentUser(current_user.id)

    if users_current.rol == 2:
        if not canDeleteFeatureSuperUser:
            return redirect(url_for('unauthorized'))

    if users_current.rol == 3:
        if not canDeleteFeatureNormalUser:
            return redirect(url_for('unauthorized'))
    # se selecteaza id-ul
    deleted_feature = Feature.query.filter_by(id = id).first()

    db.session.delete(deleted_feature)
    db.session.commit()
    #dupa stergere se face redirect catre projects
    return redirect(url_for('features'))



@app.route('/edit_feature/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_feature(id):
    
    form = EditFeatureForm()
    feature = Feature.query.filter_by(id = id).first()
    if request.method == 'GET':
        form.feature_title.data = feature.description
        
        #bucata asta pune pe default in select field valoarea din baza de date 
        form.projects.default = feature.project_id
        form.projects.process_formdata(str(feature.project_id))
        
        form.feature_description.data = feature.description
        
        form.user.default = feature.user_id
        form.user.process_formdata(str(feature.user_id))
        
        form.status.default = feature.status
        form.status.process_formdata(str(feature.status))

        form.priority.default = feature.typeProject
        form.priority.process_formdata(str(feature.typeProject))
        
    if request.method == 'POST':
        if form.validate_on_submit():
            feature.title = form.feature_title.data
            feature.description = form.feature_description.data
            
            start_date = form.start_date.data
            start_date_formated = datetime.datetime.strptime(start_date, '%d/%m/%Y') 
            feature.start_date = start_date_formated

            expected_date = form.expected_date.data
            expected_date_formated = datetime.datetime.strptime(expected_date, '%d/%m/%Y') 
            feature.expected_date = expected_date_formated

            finish_date = form.finish_date.data
            finish_date_formated = datetime.datetime.strptime(finish_date, '%d/%m/%Y') 
            feature.finish_date = finish_date_formated

            feature.project_id = form.projects.data.id
            feature.user_id = form.user.data.id
            feature.status = form.status.data
            feature.typeProject = form.priority.data

            if (start_date_formated > expected_date_formated) or (start_date_formated > finish_date_formated):
                return render_template('edit_feature.html', form = form, feature = feature ,message = 'Start Date cannot be smaller than Finnish Date or Expected Date')

            db.session.commit()
                    
            #trimitem email utilizatorului care are atribuit proiectul
            helper = Helper()
            isAllow = helper.isSendEmailOnModifyFeature(feature.user_id)
            if isAllow:
                msg = Message('Feature updated', recipients=[form.user.data.email])
                msg.body = 'A new feature with title {} for project {} has been updated'.format(form.feature_title.data, form.projects.data.title)
                try:
                    mail.send(msg)
                except:
                    pass
            #sfarsit functie de trimis email

            return redirect(url_for('features'))

    return render_template('edit_feature.html', form = form , feature = feature)


@app.route('/error')
@login_required
def error():
    return render_template('500.html', message = 'There is no open project. Please open a project to add a bug')


@app.route('/unauthorized')
@login_required
def unauthorized():
    return render_template('401.html')

@app.route('/notfound')
def notfound():
    return render_template('404.html')

@app.route('/settings',methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    auth_user = current_user
    helper = Helper()
    settings = helper.getSettingsByUser(auth_user.id)
    if request.method == 'GET':
        if not settings:
            form.checkEmailModifyBug.data = 0
            form.checkEmailModifyFeature.data = 0
            form.checkEmailModifyProject.data = 0
            form.checkEmailOpenBug.data = 0
            form.checkEmailOpenFeature.data = 0
            form.checkEmailOpenProject.data = 0
        else:
            form.checkEmailModifyBug.data = settings.checkEmailModifyBug
            form.checkEmailModifyFeature.data = settings.checkEmailModifyFeature
            form.checkEmailModifyProject.data = settings.checkEmailModifyProject
            form.checkEmailOpenBug.data = settings.checkEmailOpenBug
            form.checkEmailOpenFeature.data = settings.checkEmailOpenFeature
            form.checkEmailOpenProject.data = settings.checkEmailOpenProject
        

    if request.method == 'POST':
        if form.validate_on_submit:
            if not settings:
                new_Settings = Settings(checkEmailModifyBug = form.checkEmailModifyBug.data,checkEmailModifyFeature = form.checkEmailModifyFeature.data,  checkEmailModifyProject = form.checkEmailModifyProject.data,
                                    checkEmailOpenBug = form.checkEmailOpenBug.data,  checkEmailOpenFeature = form.checkEmailOpenFeature.data, checkEmailOpenProject = form.checkEmailOpenProject.data,
                                    user_id = auth_user.id)

                db.session.add(new_Settings)
                db.session.commit()
            
            else:
                settings.checkEmailModifyBug = form.checkEmailModifyBug.data  
                settings.checkEmailModifyFeature = form.checkEmailModifyFeature.data
                settings.checkEmailModifyProject = form.checkEmailModifyProject.data  
                settings.checkEmailOpenBug = form.checkEmailOpenBug.data 
                settings.checkEmailOpenFeature = form.checkEmailOpenFeature.data 
                settings.checkEmailOpenProject = form.checkEmailOpenProject.data 

                db.session.commit() 

            
            
            return redirect(url_for('index'))
    
    
    return render_template('settings.html', form = form)


@app.route('/rights',methods=['GET', 'POST'])
@login_required
def rights():
    form = RightsForm()
    auth_user = current_user
    users = Users.query.filter(Users.id == auth_user.id, Users.rol == 1).first() 
    # verific daca pot sa am drepturi
    if not users:
        return redirect(url_for('unauthorized'))

    rights = Rights.query.first()
    
    if request.method == 'GET':
        if not rights:
            form.check_add_new_bug_normal.data = 0
            form.check_add_new_bug_super.data  = 0
            form.check_add_new_feature_normal.data = 0
            form.check_add_new_feature_super.data = 0
            form.check_add_new_project_normal.data = 0
            form.check_add_new_project_super.data = 0
            form.check_delete_bug_normal.data = 0 
            form.check_delete_bug_super.data = 0
            form.check_delete_project_normal.data = 0
            form.check_delete_project_super.data = 0
            form.check_delete_feature_normal.data = 0
            form.check_delete_feature_super.data = 0
        else:
            form.check_add_new_bug_normal.data = rights.check_allow_add_bug_normal
            form.check_add_new_bug_super.data  = rights.check_allow_add_bug_super
            form.check_add_new_feature_normal.data = rights.check_allow_add_feature_normal
            form.check_add_new_feature_super.data = rights.check_allow_add_feature_super
            form.check_add_new_project_normal.data = rights.check_allow_add_project_normal
            form.check_add_new_project_super.data = rights.check_allow_add_project_super
            form.check_delete_bug_normal.data = rights.check_allow_delete_bugs_normal 
            form.check_delete_bug_super.data = rights.check_allow_delete_bugs_super
            form.check_delete_project_normal.data = rights.check_allow_delete_project_normal
            form.check_delete_project_super.data = rights.check_allow_delete_bugs_super
            form.check_delete_feature_normal.data = rights.check_allow_delete_feature_normal
            form.check_delete_feature_super.data = rights.check_allow_delete_feature_super

    if request.method == 'POST':
        if form.validate_on_submit():
            if not rights:
                new_rights = Rights(check_allow_add_bug_normal = form.check_add_new_bug_normal.data, check_allow_add_bug_super = form.check_add_new_bug_super.data
                                        , check_allow_add_feature_normal = form.check_add_new_feature_normal.data,  check_allow_add_feature_super = form.check_add_new_feature_super.data
                                        , check_allow_add_project_normal = form.check_add_new_project_normal.data, check_allow_add_project_super = form.check_add_new_project_super.data
                                        , check_allow_delete_bugs_normal = form.check_delete_bug_normal.data, check_allow_delete_bugs_super = form.check_delete_bug_super.data
                                        , check_allow_delete_project_normal = form.check_delete_project_normal.data, check_allow_delete_project_super = form.check_delete_project_super.data
                                        , check_allow_delete_feature_normal = form.check_delete_feature_normal.data, check_allow_delete_feature_super = form.check_delete_feature_super.data)

                db.session.add(new_rights)
                db.session.commit()

            else:
                rights.check_allow_add_bug_normal =  form.check_add_new_bug_normal.data 
                rights.check_allow_add_bug_super = form.check_add_new_bug_super.data 
                rights.check_allow_add_feature_normal = form.check_add_new_feature_normal.data  
                rights.check_allow_add_feature_super = form.check_add_new_feature_super.data 
                rights.check_allow_add_project_normal = form.check_add_new_project_normal.data 
                rights.check_allow_add_project_super = form.check_add_new_project_super.data
                rights.check_allow_delete_bugs_normal  = form.check_delete_bug_normal.data 
                rights.check_allow_delete_bugs_super = form.check_delete_bug_super.data 
                rights.check_allow_delete_project_normal = form.check_delete_project_normal.data 
                rights.check_allow_delete_project_super = form.check_delete_project_super.data  
                rights.check_allow_delete_feature_normal = form.check_delete_feature_normal.data 
                rights.check_allow_delete_feature_super = form.check_delete_feature_super.data 

                db.session.commit()

                
            return redirect(url_for('index'))

        
    return render_template('rights.html', form = form)


@app.route('/charts')
@login_required
def charts():
    # grafic projects/feature/bugs
    total_projects    = Projects.query.count() 
    total_feature     = Feature.query.count()
    total_bugs        = Bugs.query.count()
    now               = datetime.datetime.now()
    time_update       = now.strftime("%H:%M")

    #grafic bugs/month
    helper = Helper()
    given_date = datetime.datetime.today().date()

    _total_bugs_max = Bugs.query.count()
    #pentru axa oy
    total_bugs_max = helper.display_max_bugs_graph(_total_bugs_max)
    
    _last_day = helper.last_day_of_month(given_date)
    last_day = _last_day.day
    month = _last_day.month
    year  = _last_day.year

    range_month = helper.get_range_month(month)
    label_month_name = helper.get_range_month_name(range_month)
    list_bugs_data_6m = []
    for month_item in range_month:
        date_format_first_day = datetime.datetime(year,month_item,1,0,0,0,0)
        date_format_last_day  = helper.last_day_of_month(date_format_first_day)
        _list_bugs_data = db.session.query(Bugs,db.func.count(Bugs.id)).filter(Bugs.start_date >= date_format_first_day, Bugs.start_date <= date_format_last_day).first()
        list_bugs_data_6m.append(_list_bugs_data[1])

    # grafic Project/Status
    total_project_open   = Projects.query.filter(Projects.status == 1).count()
    total_project_in_dev = Projects.query.filter(Projects.status == 2).count()
    total_project_closed = Projects.query.filter(Projects.status == 3).count()

    total_bugs_open = Bugs.query.filter(Bugs.status == 1).count()
    total_bugs_in_dev = Bugs.query.filter(Bugs.status == 2).count()
    total_bugs_closed = Bugs.query.filter(Bugs.status == 3).count()

    total_feature_open = Feature.query.filter(Feature.status == 1).count()
    total_feature_in_dev = Feature.query.filter(Feature.status == 2).count()
    total_feature_closed = Feature.query.filter(Feature.status == 3).count()
    
    #grafic feature/day
    _currentMonth = datetime.datetime.now().month
    currentMonth = helper.getCurrentMonth(_currentMonth)
    
    first_day = datetime.date(year,month,1)
    current_day = datetime.datetime.today().day
    label_month_list = []
    # apelam pana la ziua curenta si bagam intr-o lista
    for day in range(0,current_day):
        label_month_list.append(str(day + 1) + " {}".format(currentMonth))

    _total_feature_max = Feature.query.count()
    #pentru axa oy
    total_feature_max = helper.display_max_bugs_graph(_total_bugs_max)
    
    #inceput pentru a aduce feature pe zile pana la ziua curenta
    today = datetime.datetime.today()
    days_cur_month = helper.days_cur_month()
    # intoarce data si rezultatul aici
    
    list_total_feature_data = []

    for day in range(1,current_day + 1):
        #apelam de fiecare data cu ziua curenta si dam ca parametru ca sa putem face countul de feature pe fiecare luna
        date_current = datetime.datetime(year,month,day,0,0,0,0)
        _total_feature_data = db.session.query(Feature,db.func.count(Feature.id)).filter(Feature.start_date == date_current).first()
        list_total_feature_data.append(_total_feature_data[1])
    
    
    return render_template('charts.html', total_projects = total_projects, total_feature = total_feature, total_bugs = total_bugs
                        , time_update = time_update, label_month_name = label_month_name, list_bugs_data_6m = list_bugs_data_6m, total_bugs_max = total_bugs_max
                        , total_project_open =total_project_open ,total_project_in_dev = total_project_in_dev,total_project_closed = total_project_closed
                        , total_bugs_open = total_bugs_open, total_bugs_in_dev = total_bugs_in_dev, total_bugs_closed = total_bugs_closed
                        , total_feature_open = total_feature_open, total_feature_in_dev = total_feature_in_dev, total_feature_closed = total_feature_closed
                        , total_feature_max = total_feature_max,list_total_feature_data = list_total_feature_data, label_month_list = label_month_list)

@app.route('/opened')
@login_required
def opened():
    project_open   = Projects.query.join(Users, Users.id == Projects.user_id, isouter = True).filter(or_(Projects.status == 1, Projects.status == 2)).all()
    bugs_open      = Bugs.query.join(Users, Users.id == Bugs.user_id, isouter = True).join(Projects, Projects.id == Bugs.project_id).filter(or_(Bugs.status == 1, Bugs.status == 2)).all()
    feature_open   = Feature.query.join(Users, Users.id == Feature.user_id, isouter = True).join(Projects, Projects.id == Feature.project_id).filter(or_(Feature.status == 1, Feature.status == 2)).all()
    
    
    return render_template('opened.html', project_open = project_open, bugs_open = bugs_open, feature_open = feature_open)



@app.route('/closed')
@login_required
def closed():
    project_closed   = Projects.query.join(Users, Users.id == Projects.user_id, isouter = True).filter(Projects.status == 3).all()
    bugs_closed      = Bugs.query.join(Users, Users.id == Bugs.user_id, isouter = True).join(Projects, Projects.id == Bugs.project_id).filter(Bugs.status == 3).all()
    feature_closed   = Feature.query.join(Users, Users.id == Feature.user_id, isouter = True).join(Projects, Projects.id == Feature.project_id).filter(Feature.status == 3).all()


    return render_template('closed.html',project_closed = project_closed, bugs_closed = bugs_closed, feature_closed = feature_closed)



@app.route('/expired')
@login_required
def expired():
    now = datetime.datetime.now()
    project_expired = Projects.query.join(Users, Users.id == Projects.user_id, isouter = True).filter(Projects.finish_date < now).all()
    bugs_expired = Bugs.query.join(Users, Users.id == Bugs.user_id, isouter = True).join(Projects, Projects.id == Bugs.project_id).filter(Bugs.finish_date < now).all()
    feature_expired = Feature.query.join(Users, Users.id == Feature.user_id, isouter = True).join(Projects, Projects.id == Feature.project_id).filter(Feature.finish_date < now).all() 


    return render_template('expired.html', project_expired = project_expired, bugs_expired = bugs_expired, feature_expired = feature_expired)


# pentru fiecare trebuie facuta form la fiecare raport
@app.route('/reports', methods = ['GET', 'POST'])
@login_required
def reports():
    form = GenerateTopUsersBugs()
    formTopFeature = GenerateTopUsersFeature()
    formCloseProjects = GenerateTopUsersClosingProjects()
    formProjectsBug = GenerateTopProjectsBugs()
    formProjectBugsDetailed = GenerateTopProjectsBugsDetailed()
    formID = request.args.get('formID', 1, type=int)
    if request.method == 'POST':
        # sunt pe primul form
        if form.validate_on_submit() and formID == 1:
            start_date = datetime.datetime.strptime(form.start_date.data,'%d/%m/%Y')
            finish_date = datetime.datetime.strptime(form.finish_date.data, '%d/%m/%Y')
            format_start_date = start_date.strftime('%d%m%Y')
            format_finish_date = finish_date.strftime('%d%m%Y')
            
            return redirect(url_for('generate_top_user_bug', format_start_date = format_start_date, format_finish_date = format_finish_date))

        #sunt pe al doilea form
        if formTopFeature.validate_on_submit() and formID == 2:
            start_date = datetime.datetime.strptime(formTopFeature.start_date.data,'%d/%m/%Y')
            finish_date = datetime.datetime.strptime(formTopFeature.finish_date.data, '%d/%m/%Y')
            format_start_date = start_date.strftime('%d%m%Y')
            format_finish_date = finish_date.strftime('%d%m%Y')

            return redirect(url_for('generate_top_user_feature', format_start_date = format_start_date, format_finish_date = format_finish_date))

        #sunt pe al treilea form
        if formCloseProjects.validate_on_submit() and formID == 3:
            start_date = datetime.datetime.strptime(formCloseProjects.start_date.data,'%d/%m/%Y')
            finish_date = datetime.datetime.strptime(formCloseProjects.finish_date.data, '%d/%m/%Y')
            format_start_date = start_date.strftime('%d%m%Y')
            format_finish_date = finish_date.strftime('%d%m%Y')

            return redirect(url_for('generate_top_user_projects', format_start_date = format_start_date, format_finish_date = format_finish_date))


        #sunt pe al patrulea form\
        if formProjectsBug.validate_on_submit() and formID == 4:
            start_date = datetime.datetime.strptime(formProjectsBug.start_date.data,'%d/%m/%Y')
            finish_date = datetime.datetime.strptime(formProjectsBug.finish_date.data, '%d/%m/%Y')
            format_start_date = start_date.strftime('%d%m%Y')
            format_finish_date = finish_date.strftime('%d%m%Y')

            return redirect(url_for('projects_bugs', format_start_date = format_start_date, format_finish_date = format_finish_date))

        if formProjectBugsDetailed.validate_on_submit() and formID == 5:
            id_project = formProjectBugsDetailed.projects.data.id

            return redirect(url_for('projects_bugs_all', id = id_project))

    
    return render_template('reports.html', form = form, formTopFeature = formTopFeature, 
                            formCloseProjects = formCloseProjects, 
                            formProjectsBug = formProjectsBug, formProjectBugsDetailed = formProjectBugsDetailed)


@app.route('/generate_top_user_bug/<format_start_date>/<format_finish_date>')
@login_required
def generate_top_user_bug(format_start_date, format_finish_date):
    #aici arat raportul
    start_date = datetime.datetime.strptime(format_start_date,'%d%m%Y')
    finish_date = datetime.datetime.strptime(format_finish_date, '%d%m%Y')

    format_start_date = start_date.strftime('%d/%m/%Y')
    format_finish_date = finish_date.strftime('%d/%m/%Y')
    
    total_bugs_closed     = db.session.query(db.func.count(Bugs.user_id)).filter(Bugs.user_id == Users.id, Bugs.status == 3, Bugs.finish_date >= start_date, Bugs.finish_date <= finish_date).label('total_bugs_closed')
    all_users             = db.session.query(Users, total_bugs_closed).group_by('total_bugs_closed', Users.email).order_by(desc('total_bugs_closed')).all()
    
    return render_template('generate_top_user_bug.html', format_start_date = format_start_date, format_finish_date = format_finish_date, all_users = all_users)


@app.route('/generate_top_user_feature/<format_start_date>/<format_finish_date>')
@login_required
def generate_top_user_feature(format_start_date, format_finish_date):
    
    start_date = datetime.datetime.strptime(format_start_date,'%d%m%Y')
    finish_date = datetime.datetime.strptime(format_finish_date, '%d%m%Y')

    format_start_date = start_date.strftime('%d/%m/%Y')
    format_finish_date = finish_date.strftime('%d/%m/%Y')

    total_feature_closed     = db.session.query(db.func.count(Feature.user_id)).filter(Feature.user_id == Users.id, Feature.status == 3, Feature.finish_date >= start_date, Feature.finish_date <= finish_date).label('total_feature_closed')
    all_users                = db.session.query(Users, total_feature_closed).group_by('total_feature_closed', Users.email).order_by(desc('total_feature_closed')).all()


    return render_template('generate_top_user_feature.html', format_start_date = format_start_date, format_finish_date = format_finish_date, all_users = all_users)



@app.route('/generate_top_user_projects/<format_start_date>/<format_finish_date>')
@login_required
def generate_top_user_projects(format_start_date, format_finish_date):
    start_date = datetime.datetime.strptime(format_start_date,'%d%m%Y')
    finish_date = datetime.datetime.strptime(format_finish_date, '%d%m%Y')

    format_start_date = start_date.strftime('%d/%m/%Y')
    format_finish_date = finish_date.strftime('%d/%m/%Y')

    total_projects_closed    = db.session.query(db.func.count(Projects.user_id)).filter(Projects.user_id == Users.id, Projects.status == 3, Projects.finish_date >= start_date, Projects.finish_date <= finish_date).label('total_projects_closed')
    all_users                = db.session.query(Users, total_projects_closed).group_by('total_projects_closed', Users.email).order_by(desc('total_projects_closed')).all()

    return render_template('generate_top_user_close_projects.html', format_start_date = format_start_date, format_finish_date = format_finish_date, all_users = all_users)


#asta este bug-uri pe proiecte per day cumulate
@app.route('/projects_bugs/<format_start_date>/<format_finish_date>')
@login_required
def projects_bugs(format_start_date, format_finish_date):
    start_date = datetime.datetime.strptime(format_start_date,'%d%m%Y')
    finish_date = datetime.datetime.strptime(format_finish_date, '%d%m%Y')

    format_start_date = start_date.strftime('%d/%m/%Y')
    format_finish_date = finish_date.strftime('%d/%m/%Y')

    total_projects_bugs = db.session.query(db.func.count(Bugs.project_id)).filter(Bugs.project_id == Projects.id, Bugs.start_date >= start_date, Bugs.start_date <= finish_date).label('total_projects_bugs')
    all_bugs_project = db.session.query(Projects,total_projects_bugs).group_by('total_projects_bugs', Projects.title).order_by(desc('total_projects_bugs')).all()
    
    return render_template('project_bugs_interval.html', format_start_date = format_start_date, format_finish_date = format_finish_date, all_bugs_project = all_bugs_project)


#asta este toate proiectele si bugurile si se poate selecta dintr-un combo
@app.route('/projects_bugs_all/<int:id>')
@login_required
def projects_bugs_all(id):
    project_id = id
    all_bugs_per_project = Bugs.query.filter(Bugs.project_id == project_id).all()
    project_selected = Projects.query.filter(Projects.id == project_id).first()
    if project_selected.status == 1:
        label_status = 'Open'
    elif project_selected.status == 2:
        label_status = 'In development'
    else:
        label_status = 'Closed'

    if project_selected.typeProject == 1:
        label_priority = 'Normal'
    elif project_selected.typeProject == 2:
        label_priority = 'Alert'
    else:
        label_priority = 'Critic'
    
    return render_template('projects_bugs_detailed.html', all_bugs_per_project = all_bugs_per_project, project_selected = project_selected, label_status = label_status, label_priority = label_priority)

#asta este pentru per day cumulate
@app.route('/projects_features')
@login_required
def projects_features():
    pass

#asta este cu selectie dintr-un combo
@app.route('/projects_features_all')
@login_required
def projects_features_all():
    pass



@app.route('/top_priority')
@login_required
def top_priority():
    pass
                

    



    