from model import Settings, Users, Rights, Email
import datetime
import base64
class Helper():

    def getSettingsByUser(self, userId):
        settings = Settings.query.filter(Settings.user_id == userId).first()
        return settings

    def getAccessByRole(self,role_id):
        rights = Rights.query.filter(Rights.role_id == role_id).first()
        return rights

    def isSendEmailOnNewProject(self, userId):
        settings = Settings.query.filter(Settings.user_id == userId).first()
        if settings:
            if settings.checkEmailOpenProject == 0:
                return False
            else:
                return True
        else:
            return False

    def isSendEmailOnModifyProject(self, userId):
        settings = Settings.query.filter(Settings.user_id == userId).first()
        if settings:
            if settings.checkEmailModifyProject == 0:
                return False
            else:
                return True
        else:
            return False

    def isSendEmailOnNewBug(self, userId):
        settings = Settings.query.filter(Settings.user_id == userId).first()
        if settings:
            if settings.checkEmailOpenBug == 0:
                return False
            else:
                return True
        else:
            return False

    def isSendEmailOnModifyBug(self, userId):
        settings = Settings.query.filter(Settings.user_id == userId).first()
        if settings:
            if settings.checkEmailModifyBug == 0:
                return False
            else:
                return True
        else:
            return False

    def isSendEmailOnNewFeature(self, userId):
        settings = Settings.query.filter(Settings.user_id == userId).first()
        if settings:
            if settings.checkEmailOpenFeature == 0:
                return False
            else:
                return True
        else:
            return False

    
    def isSendEmailOnModifyFeature(self, userId):
        settings = Settings.query.filter(Settings.user_id == userId).first()
        if settings:
            if settings.checkEmailModifyFeature == 0:
                return False
            else:
                return True
        else:
            return False

    def canAddNewProjectSuperUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_add_project_super == 1:
                return True
            else:
                return False
        else:
            return False

    def canAddNewProjectNormalUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_add_project_normal == 1:
                return True
            else:
                return False
        else:
            return False

    def canDeleteProjectSuperUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_delete_project_super == 1:
                return True
            else:
                return False
        else:
            return False

    def canDeleteProjectNormalUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_delete_project_normal == 1:
                return True
            else:
                return False
        else:
            return False


    def canAddNewBugSuperUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_add_bug_super:
                return True
            else:
                return False
        else:
            return False

    def canAddNewBugNormalUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_add_bug_normal:
                return True
            else:
                return False
        else:
            return False

    
    def canDeleteBugSuperUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_delete_bugs_super:
                return True
            else:
                return False
        else:
            return False

    
    def canDeleteBugNormalUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_delete_bugs_normal:
                return True
            else:
                return False
        else:
            return False

    def canAddNewFeatureSuperUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_add_feature_super:
                return True
            else:
                return False
        else:
            return False

    def canAddNewFeatureNormalUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_add_feature_normal:
                return True
            else:
                return False
        else:
            return False

    def canDeleteFeatureSuperUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_delete_feature_super:
                return True
            else:
                return False
        else:
            return False

    
    def canDeleteFeatureNormalUser(self):
        rights = Rights.query.first()
        if rights:
            if rights.check_allow_delete_feature_normal:
                return True
            else:
                return False
        else:
            return False



    def getCurrentUser(self,userId):
        users = Users.query.filter(Users.id == userId).first()
        return users

    def getCurrentMonth(self,month):
        if month == 1:
            return "January"
        elif month == 2:
            return "February"
        elif month == 3:
            return "March"
        elif month == 4:
            return "April"
        elif month == 5:
            return "May"
        elif month == 6:
            return "June"
        elif month == 7:
            return "July"
        elif month == 8:
            return "August"
        elif month == 9:
            return "September"
        elif month == 10:
            return "Octomber"
        elif month == 11:
            return "November"
        elif month == 12:
            return "December"

    def last_day_of_month(self,date):
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

    def display_max_bugs_graph(self, _total_bugs_max):
        if _total_bugs_max < 100:
            return 100 
        elif _total_bugs_max > 100:
            return 1000
        elif _total_bugs_max > 1000:
            return 5000
        elif _total_bugs_max > 5000:
            return 10000
        elif _total_bugs_max > 10000:
            return 20000

    def days_cur_month(self):
        m = datetime.datetime.now().month
        y = datetime.datetime.now().year
        ndays = (datetime.date(y, m+1, 1) - datetime.date(y, m, 1)).days
        d1 = datetime.date(y, m, 1)
        d2 = datetime.date(y, m, ndays)
        delta = d2 - d1
        return [(d1 + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

    
    def get_range_month(self,current_month):
        if current_month == 1:
           list_month = [7,8,9,10,11,12]
        elif current_month == 2:
            list_month = [8,9,10,11,12,1]
        elif current_month == 3:
            list_month = [9,10,11,12,1,2]
        elif current_month == 4:
            list_month = [10,11,12,1,2,3]
        elif current_month == 5:
            list_month = [11,12,1,2,3,4]
        elif current_month == 6:
            list_month = [12,1,2,3,4,5]
        elif current_month == 7:
            list_month = [1,2,3,4,5,6]
        elif current_month == 8:
            list_month = [2,3,4,5,6,7]
        elif current_month == 9:
            list_month = [3,4,5,6,7,8]
        elif current_month == 10:
            list_month = [4,5,6,7,8,9]
        elif current_month == 11:
            list_month = [5,6,7,8,9,10]
        elif current_month == 12:
            list_month = [6,7,8,9,10,11]
        
        return list_month


    def get_range_month_name(self,list_month):
        if list_month == [7,8,9,10,11,12]:
            name_month = ["July","August", "September","October", "November","December"]
        elif list_month == [8,9,10,11,12,1]:
            name_month = ["August","September","October", "November","December", "January"]
        elif list_month == [9,10,11,12,1,2]:
            name_month = ["September","October", "November","December", "January", "February"]
        elif list_month == [10,11,12,1,2,3]:
            name_month = ["October", "November","December", "January", "February", "March"]
        elif list_month == [11,12,1,2,3,4]:
            name_month = ["November","December", "January", "February", "March","April"]
        elif list_month == [12,1,2,3,4, 5]:
            name_month = ["December", "January", "February", "March","April", "May"]
        elif list_month == [1,2,3,4,5,6]:
            name_month = ["January", "February", "March","April", "May", "June"]
        elif list_month == [2,3,4,5,6,7]:
            name_month = ["February", "March","April", "May", "June", "July"]
        elif list_month == [3,4,5,6,7,8]:
            name_month = ["March","April", "May", "June", "July", "August"]
        elif list_month == [4,5,6,7,8,9]:
            name_month = ["April", "May", "June", "July", "August", "September"]
        elif list_month == [5,6,7,8,9,10]:
            name_month = ["May", "June", "July", "August", "September","October"]
        elif list_month == [6,7,8,9,10,11]:
            name_month = ["June", "July", "August", "September","October", "November"]

        return name_month


    def get_email_details(self):
        email = Email.query.first()
        list_email = []
        if email:
            list_email.append(email.server_name)
            list_email.append(email.mail_port)
            if email.use_ssl == 0:
                list_email.append(False)
            else:
                list_email.append(True)

            if email.use_tls == 0:
                list_email.append(False)
            else:
                list_email.append(True)
            
            list_email.append(email.email)
            list_email.append(base64.b64decode(email.password).decode("utf-8"))
        else:
            list_email.append('')
            list_email.append('')
            list_email.append('')
            list_email.append('')
            list_email.append('')
            list_email.append('')
                        
        return list_email

  


        

        





