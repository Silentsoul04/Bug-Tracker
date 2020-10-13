from flask_wtf import FlaskForm # pentru a transforma registerul in flask form
from wtforms import StringField, PasswordField, FileField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length
from model import Users, Projects, Role

def return_all_users():
    user = Users.query.all()
    return user

def return_all_open_projects():
    projects = Projects.query.filter(Projects.status != 3).all()
    return projects

def return_all_projects():
    projects = Projects.query.all()
    return projects

def return_all_role():
    role = Role.query.all()
    return role

def return_all_projects():
    projects = Projects.query.all()
    return projects



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Username-ul este camp obligatioriu!'), Length(max=100, message='Username-ul nu poate avea mai mult de 100 de caractere!')])
    password = PasswordField('Password', validators=[InputRequired('Parola este camp obligatoriu!')])
    remember = BooleanField('Remember Me')

#pentru formul de register
class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired('Numele este camp obligatoriu! '), Length(max=100, message='Numele nu poate avea mai mult de 100 de caractere')])
    last_name = StringField('Last Name', validators=[InputRequired('Prenumele este camp obligatoriu! '), Length(max=100, message='Prenumele nu poate avea mai mult de 100 de caractere')])
    email = StringField('email', validators=[InputRequired('Email-ul este camp obligatioriu!'), Length(max=100, message='Username-ul nu poate avea mai mult de 100 de caractere!')])
    password = PasswordField('Password', validators=[InputRequired('Parola este camp obligatoriu!')])
    confirm_password = PasswordField('Password', validators=[InputRequired('Parola este camp obligatoriu!')])


class ResetPasswordForm(FlaskForm):
    email = StringField('email', validators=[InputRequired('Email-ul este camp obligatioriu!'), Length(max=100, message='Username-ul nu poate avea mai mult de 100 de caractere!')])


class RestorePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired('Parola este camp obligatoriu!')])
    confirm_password = PasswordField('Password', validators=[InputRequired('Parola este camp obligatoriu!')])

class AddProjectForm(FlaskForm):
    project_title = StringField('Title', validators=[InputRequired('Project Title is required')])
    project_description = TextAreaField('Description',validators=[InputRequired('Description is required')])
    start_date = StringField('Start Date', validators=[InputRequired('Start date is required')])
    expected_date = StringField('Expected Date', validators=[InputRequired('Expected date is required')])
    finish_date = StringField('Finish Date', validators=[InputRequired('Finish Date is required')])
    user        = QuerySelectField('User',validators=[InputRequired('Select a user')], query_factory=return_all_users, get_label='email')
    status      =  SelectField('Status', choices=[('1', 'Open'), ('2', 'In Development'), ('3' , 'Closed')])
    priority    =  SelectField('Priority', choices=[('1', 'Normal'), ('2', 'Alert'), ('3' , 'Critical')])


class EditProjectForm(FlaskForm):
    project_title = StringField('Title', validators=[InputRequired('Project Title is required')])
    project_description = TextAreaField('Description',validators=[InputRequired('Description is required')])
    start_date = StringField('Start Date', validators=[InputRequired('Start date is required')])
    expected_date = StringField('Expected Date', validators=[InputRequired('Expected date is required')])
    finish_date = StringField('Finish Date', validators=[InputRequired('Finish Date is required')])
    user        = QuerySelectField('User',validators=[InputRequired('Select a user')], query_factory=return_all_users, get_label='email')
    status      =  SelectField('Status', choices=[('1', 'Open'), ('2', 'In Development'), ('3' , 'Closed')])
    priority    =  SelectField('Priority', choices=[('1', 'Normal'), ('2', 'Alert'), ('3' , 'Critical')])


class AddBugsForm(FlaskForm):
    bug_title = StringField('Title', validators=[InputRequired('Bug Title is required')])
    bug_description = TextAreaField('Description',validators=[InputRequired('Description is required')])
    start_date = StringField('Start Date', validators=[InputRequired('Start date is required')])
    expected_date = StringField('Expected Date', validators=[InputRequired('Expected date is required')])
    finish_date = StringField('Finish Date', validators=[InputRequired('Finish Date is required')])
    user        = QuerySelectField('User',validators=[InputRequired('Select a user')], query_factory=return_all_users, get_label='email')
    projects    = QuerySelectField('Projects',validators=[InputRequired('Select a project')], query_factory=return_all_open_projects, get_label='title')
    status      =  SelectField('Status', choices=[('1', 'Open'), ('2', 'In Development'), ('3' , 'Closed')])
    priority    =  SelectField('Priority', choices=[('1', 'Normal'), ('2', 'Alert'), ('3' , 'Critical')])


class EditBugForm(FlaskForm):
    bug_title = StringField('Title', validators=[InputRequired('Bug Title is required')])
    bug_description = TextAreaField('Description',validators=[InputRequired('Description is required')])
    start_date = StringField('Start Date', validators=[InputRequired('Start date is required')])
    expected_date = StringField('Expected Date', validators=[InputRequired('Expected date is required')])
    finish_date = StringField('Finish Date', validators=[InputRequired('Finish Date is required')])
    user        = QuerySelectField('User',validators=[InputRequired('Select a user')], query_factory=return_all_users, get_label='email')
    projects    = QuerySelectField('Projects',validators=[InputRequired('Select a project')], query_factory=return_all_open_projects, get_label='title')
    status      =  SelectField('Status', choices=[('1', 'Open'), ('2', 'In Development'), ('3' , 'Closed')])
    priority    =  SelectField('Priority', choices=[('1', 'Normal'), ('2', 'Alert'), ('3' , 'Critical')])


class AddFeatureForm(FlaskForm):
    feature_title = StringField('Title', validators=[InputRequired('Feature Title is required')])
    feature_description = TextAreaField('Description',validators=[InputRequired('Description is required')])
    start_date = StringField('Start Date', validators=[InputRequired('Start date is required')])
    expected_date = StringField('Expected Date', validators=[InputRequired('Expected date is required')])
    finish_date = StringField('Finish Date', validators=[InputRequired('Finish Date is required')])
    user        = QuerySelectField('User',validators=[InputRequired('Select a user')], query_factory=return_all_users, get_label='email')
    projects    = QuerySelectField('Projects',validators=[InputRequired('Select a project')], query_factory=return_all_open_projects, get_label='title')
    status      =  SelectField('Status', choices=[('1', 'Open'), ('2', 'In Development'), ('3' , 'Closed')])
    priority    =  SelectField('Priority', choices=[('1', 'Normal'), ('2', 'Alert'), ('3' , 'Critical')])

class EditFeatureForm(FlaskForm):
    feature_title = StringField('Title', validators=[InputRequired('Feature Title is required')])
    feature_description = TextAreaField('Description',validators=[InputRequired('Description is required')])
    start_date = StringField('Start Date', validators=[InputRequired('Start date is required')])
    expected_date = StringField('Expected Date', validators=[InputRequired('Expected date is required')])
    finish_date = StringField('Finish Date', validators=[InputRequired('Finish Date is required')])
    user        = QuerySelectField('User',validators=[InputRequired('Select a user')], query_factory=return_all_users, get_label='email')
    projects    = QuerySelectField('Projects',validators=[InputRequired('Select a project')], query_factory=return_all_open_projects, get_label='title')
    status      =  SelectField('Status', choices=[('1', 'Open'), ('2', 'In Development'), ('3' , 'Closed')])
    priority    =  SelectField('Priority', choices=[('1', 'Normal'), ('2', 'Alert'), ('3' , 'Critical')])


class AddUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired('Numele este camp obligatoriu! '), Length(max=100, message='Numele nu poate avea mai mult de 100 de caractere')])
    last_name = StringField('Last Name', validators=[InputRequired('Prenumele este camp obligatoriu! '), Length(max=100, message='Prenumele nu poate avea mai mult de 100 de caractere')])
    email = StringField('email', validators=[InputRequired('Email-ul este camp obligatioriu!'), Length(max=100, message='Username-ul nu poate avea mai mult de 100 de caractere!')])
    password = PasswordField('Password', validators=[InputRequired('Parola este camp obligatoriu!')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired('Parola este camp obligatoriu!')])
    role = SelectField('Rol', choices=[('1', 'Administrator'), ('2','Super User'), ('3' ,'User')])


class EditUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired('Numele este camp obligatoriu! '), Length(max=100, message='Numele nu poate avea mai mult de 100 de caractere')])
    last_name = StringField('Last Name', validators=[InputRequired('Prenumele este camp obligatoriu! '), Length(max=100, message='Prenumele nu poate avea mai mult de 100 de caractere')])
    email = StringField('email', validators=[InputRequired('Email-ul este camp obligatioriu!'), Length(max=100, message='Username-ul nu poate avea mai mult de 100 de caractere!')])
    password = PasswordField('Password', validators=[InputRequired('Parola este camp obligatoriu!')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired('Parola este camp obligatoriu!')])
    role = SelectField('Rol', choices=[('1', 'Administrator'), ('2','Super User'), ('3' ,'User')])

class SettingsForm(FlaskForm):
    checkEmailOpenProject       = BooleanField('Send email alert when open a project')
    checkEmailModifyProject     = BooleanField('Send email alert when modify a project')
    checkEmailOpenBug           = BooleanField('Send email alert when open a bug')
    checkEmailModifyBug         = BooleanField('Send email alert when modify a bug')
    checkEmailOpenFeature       = BooleanField('Send email alert when open a feature')
    checkEmailModifyFeature     = BooleanField('Send email alert when modify a feature')


class RightsForm(FlaskForm):
    check_add_new_project_super      = BooleanField('Allow super user to add a new project')
    check_add_new_project_normal     = BooleanField('Allow normal user to add a new project')
    check_add_new_bug_super          = BooleanField('Allow super user to add a new bug')
    check_add_new_bug_normal         = BooleanField('Allow normal user to add a new bug')
    check_add_new_feature_super      = BooleanField('Allow super user to add a new feature')
    check_add_new_feature_normal     = BooleanField('Allow normal user to add a new feature')
    check_delete_project_super       = BooleanField('Allow super user to delete a project')
    check_delete_project_normal      = BooleanField('Allow normal user to delete a project')
    check_delete_bug_super           = BooleanField('Allow super user to delete a bug')
    check_delete_bug_normal          = BooleanField('Allow normal user to delete a bug')
    check_delete_feature_super       = BooleanField('Allow super user to delete a feature')
    check_delete_feature_normal      = BooleanField('Allow normal user to delete a feature')

class EmailForm(FlaskForm):
    server_name   =  StringField('Server Name', validators=[InputRequired('Server name is required'), Length(max=200, message='Server name cannot be bigger than 200 characters')])
    mail_port     = IntegerField('Mail Port')
    use_tls       = BooleanField('Use TLS')
    use_ssl       = BooleanField('Use SSL')
    email         = StringField('Email', validators=[InputRequired('Email is required'), Length(max=200, message='Email cannot be bigger than 200 characters')])
    mail_password = PasswordField('Mail Password', validators=[InputRequired('Mail Password is required')])


class GenerateTopUsersBugs(FlaskForm):
    start_date = StringField('Start Date', validators=[InputRequired('Start date is required')])
    finish_date = StringField('Finish Date', validators=[InputRequired('Finish Date is required')])

class GenerateTopUsersFeature(FlaskForm):
    start_date = StringField('Start Date', validators=[InputRequired('Start date is required')])
    finish_date = StringField('Finish Date', validators=[InputRequired('Finish Date is required')])

class GenerateTopUsersClosingProjects(FlaskForm):
    start_date = StringField('Start Date', validators=[InputRequired('Start date is required')])
    finish_date = StringField('Finish Date', validators=[InputRequired('Finish Date is required')])


class GenerateTopProjectsBugs(FlaskForm):
    start_date  = StringField('Start Date', validators=[InputRequired('Start date is required')])
    finish_date = StringField('Finish Date', validators=[InputRequired('Finish Date is required')])

class GenerateTopProjectsBugsDetailed(FlaskForm):
    projects = QuerySelectField('Projects',validators=[InputRequired('Select a project')], query_factory=return_all_projects, get_label='title')




