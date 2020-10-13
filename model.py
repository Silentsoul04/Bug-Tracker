from app import db, login_manager
from flask_login import UserMixin

class Users(UserMixin , db.Model):
    id         = db.Column(db.Integer(), primary_key = True)
    firstname  = db.Column(db.String(255))
    lastname   = db.Column(db.String(255))
    email      = db.Column(db.String(255))
    password   = db.Column(db.String(255))
    rol        = db.Column(db.Integer())

    projects = db.relationship('Projects', backref='users', lazy ='dynamic',foreign_keys = 'Projects.user_id')
    bugs = db.relationship('Bugs', backref='users', lazy ='dynamic',foreign_keys = 'Bugs.user_id')
    feature = db.relationship('Feature', backref='users', lazy ='dynamic',foreign_keys = 'Feature.user_id')


class Projects(db.Model):
    id          = db.Column(db.Integer(), primary_key = True)
    user_id     = db.Column(db.Integer(), db.ForeignKey('users.id'))
    title       = db.Column(db.String(255))
    description = db.Column(db.Text())
    start_date  = db.Column(db.DateTime)
    expected_date = db.Column(db.DateTime)
    finish_date = db.Column(db.DateTime)
    status      = db.Column(db.Integer())
    typeProject = db.Column(db.Integer())

    bugs = db.relationship('Bugs', backref='projects', lazy ='dynamic', foreign_keys = 'Bugs.project_id')
    feature = db.relationship('Feature', backref='projects', lazy ='dynamic', foreign_keys = 'Feature.project_id')

    

class Bugs(db.Model):
    id          = db.Column(db.Integer(), primary_key = True)
    user_id     = db.Column(db.Integer(), db.ForeignKey('users.id'))
    project_id  = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    title       = db.Column(db.String(255))
    description = db.Column(db.Text())
    start_date  = db.Column(db.DateTime)
    expected_date =db.Column(db.DateTime)
    finish_date = db.Column(db.DateTime)
    status      = db.Column(db.Integer())
    typeProject = db.Column(db.Integer())


class Feature(db.Model):
    id          = db.Column(db.Integer(), primary_key = True)
    user_id     = db.Column(db.Integer(), db.ForeignKey('users.id'))
    project_id  = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    title       = db.Column(db.String(255))
    description = db.Column(db.Text())
    start_date  = db.Column(db.DateTime)
    expected_date = db.Column(db.DateTime)
    finish_date = db.Column(db.DateTime)
    status      = db.Column(db.Integer())
    typeProject = db.Column(db.Integer())


class Settings(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    checkEmailOpenProject = db.Column(db.Integer())
    checkEmailModifyProject = db.Column(db.Integer())
    checkEmailOpenBug       = db.Column(db.Integer())
    checkEmailModifyBug     = db.Column(db.Integer())
    checkEmailOpenFeature   = db.Column(db.Integer())
    checkEmailModifyFeature = db.Column(db.Integer())

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))


class Role(db.Model):
    id  = db.Column(db.Integer(), primary_key = True)
    role_name = db.Column(db.String(255))


class Rights(db.Model):
    id                                    = db.Column(db.Integer(), primary_key = True)
    check_allow_add_project_super         = db.Column(db.Integer())
    check_allow_add_project_normal        = db.Column(db.Integer())
    check_allow_add_bug_super             = db.Column(db.Integer())
    check_allow_add_bug_normal            = db.Column(db.Integer())
    check_allow_add_feature_super         = db.Column(db.Integer())
    check_allow_add_feature_normal        = db.Column(db.Integer())
    check_allow_delete_project_super      = db.Column(db.Integer())
    check_allow_delete_project_normal     = db.Column(db.Integer())
    check_allow_delete_bugs_super         = db.Column(db.Integer())
    check_allow_delete_bugs_normal        = db.Column(db.Integer())
    check_allow_delete_feature_super      = db.Column(db.Integer())
    check_allow_delete_feature_normal     = db.Column(db.Integer()) 

class Email(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    server_name = db.Column(db.String(255))
    mail_port = db.Column(db.Integer())
    use_ssl = db.Column(db.Integer())
    use_tls = db.Column(db.Integer())
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

