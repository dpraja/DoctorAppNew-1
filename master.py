from flask import Flask,request,jsonify

#---------userprofile--------#
from User_Profile import insertuser_profile
from User_Profile import updateuser_profile
from User_Profile import selectuser_profile
from User_Profile import deleteuser_profile

#---------appionment-------#
from Appoinment import tokengeneration
from Appoinment import selectappointment
from Appoinment import updatetoken
from Appoinment import count
from Appoinment import livefeed

#-----------------Specialization-------------------#
from Specialization import insertspecialization
from Specialization import updatespecialization
from Specialization import selectspecialization
from Specialization import deletespecialization

#------------------Services-------------------------#
from Services import insertservices
from Services import updateservices
from Services import selectservices
from Services import deleteservices

#--------------timing---------#

from Timing  import Insert_Timing
from Timing  import Select_Timing
from Timing  import Update_Timing
from Timing  import Delete_Timing

#------------feed_back---------#

from FeedBack  import Insert_FeedBack
from FeedBack  import Select_FeedBack
from FeedBack  import Update_FeedBack
from FeedBack  import Delete_FeedBack
#------Doctorprofile-------------#
from doctorprofile import insert_Doctorsprofile
from doctorprofile import insert_businessprofile
from doctorprofile import update_Businessprofile
from doctorprofile import update_doctorprofile
from doctorprofile import update_businessanddoctors
from doctorprofile import updatedocspecialization
from doctorprofile import updatedocservices

#---------country--------#
from country import Insert_Country
from country import Select_Country
from country import Update_Country
#---------------Send Email----------------#
from SendEmailAll2 import sendemailall

#------------Send SMS------------------#
from SendSMS import sendsms

#-----------select doc and bus all------
from Select_BusinessAndDoctors import Select_BusinessandDoctors


from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/")
def index():
    return "Welcome to dopctorapp"



#----------------Userprofile---------------------------
@app.route('/Insert_User_Profile',methods=['POST'])
def Insertuser_profile():
    return insertuser_profile(request)
@app.route('/Update_User_Profile',methods=['POST'])
def Update_User_profile():
    return updateuser_profile(request)
@app.route('/Select_User_Profile',methods=['POST','GET'])
def Select_User_Profile():
    return selectuser_profile(request)
@app.route('/Delete_User_Profile',methods=['POST'])
def Delete_User_Profile():
    return deleteuser_profile(request)
#-----------appoinment-------------#
@app.route('/InsertAppoinment',methods=['post'])
def appoinment():
    return tokengeneration(request)
@app.route('/SelectAppoinment',methods=['post'])
def Selectppoinment():
    return selectappointment(request)

@app.route('/UpdateAppoinment',methods=['post'])
def cancelppoinment():
    return updatetoken(request)
@app.route('/CountAppoinment',methods=['post'])
def Count():
    return count(request)
@app.route('/livefeed',methods=['post'])
def Livefeed():
    return livefeed(request)

#---------------Business And Doctors-----------------------#
@app.route('/insert_BusinessAndDoctors',methods=['post'])
def insert_BusAndDocs():
    return insert_BusinessAndDoctors(request)
@app.route('/select_BusinessAndDoctors',methods=['post'])
def Select_BusAndDocs():
    return select_BusinessAndDoctors()
@app.route('/select_BusinessAndDoctorsprofile',methods=['post'])
def Select_BusAndDocsprofile():
    return select_BusinessAndDoctorsprofile()

#--------------Specialization------------------------------#

@app.route('/Insert_Specialization',methods=['POST'])
def Insert_Specialization():
    return insertspecialization(request)
@app.route('/Update_Specialization',methods=['POST'])
def Update_Specialization():
    return updatespecialization(request)
@app.route('/Select_Specialization',methods=['POST'])
def Select_Specialization():
    return selectspecialization(request)
@app.route('/Delete_Specialization',methods=['POST'])
def Delete_Specialization():
    return deletespecialization(request)

#-------------------Services----------------------------#
@app.route('/Insert_Services',methods=['post'])
def Insert_Services():
    return insertservices(request)

@app.route('/Update_Services',methods=['post'])
def Update_Services():
    return updateservices(request)

@app.route('/Select_Services',methods=['post'])
def Select_Services():
    return selectservices(request)

@app.route('/Delete_Services',methods=['post'])
def Delete_Services():
    return deleteservices(request)

#------------------timing----------------------------#
@app.route('/Insert_Timing',methods=['post'])
def inserttiming():
    return Insert_Timing(request)

@app.route('/Select_Timing',methods=['post'])
def selecttiming():
    return Select_Timing(request)

@app.route('/Update_Timing',methods=['post'])
def updatetiming():
    return Update_Timing(request)

@app.route('/Delete_Timing',methods=['post'])
def deletetiming():
    return Delete_Timing(request)

#--------------------feed_back-----------------------#

@app.route('/Insert_FeedBack',methods=['post'])
def insertfeedback():
    return Insert_FeedBack(request)


@app.route('/Select_FeedBack',methods=['post'])
def selectfeedback():
    return Select_FeedBack(request)

@app.route('/Update_FeedBack',methods=['post'])
def updatefeedback():
    return Update_FeedBack(request)

@app.route('/Delete_FeedBack',methods=['post'])
def deletefeedback():
    return Delete_FeedBack(request)

#------------------doctorprofile-------#
@app.route('/Insert_Doctor_profile',methods=['post'])
def Insert_Doctorsprofile():
    return insert_Doctorsprofile(request)

@app.route('/Insert_Business_profile',methods=['post'])
def Insert_Businessprofile():
    return insert_businessprofile(request)
@app.route('/update_Business_profile',methods=['post'])
def Update_Businessprofile():
    return update_Businessprofile(request)
@app.route('/update_doctor_profile',methods=['post'])
def Update_doctorprofile():
    return update_doctorprofile(request)
@app.route('/update_BusinessAndDoctors',methods=['post'])
def Update_BusinessAndDoctors():
    return update_businessanddoctors(request)
@app.route('/Update_Doc_Specialization',methods=['POST'])
def Update_Doc_Specialization():
    return updatedocspecialization(request)
@app.route('/Update_Doc_Services',methods=['post'])
def Update_Doc_Services():
    return updatedocservices(request)
#-------------------country------------------#

@app.route('/Insert_Country',methods=['post'])
def insertcountry():
    return Insert_Country(request)
@app.route('/Select_Country',methods=['post'])
def selectcountry():
    return Select_Country(request)
@app.route('/Update_Country',methods=['post'])
def updatecountry():
    return Update_Country(request)



#-----------------Send Email-----------------#
@app.route('/SendEmailall',methods=['post'])
def Sendemailall():
    return sendemailall(request)

#-------------------Send SMS------------------#
@app.route('/SendSMS',methods=['GET'])
def Sendsms():
    return sendsms(request)

#-----------select doc and bus all------
@app.route('/Select_BusinessandDoctors',methods=['POST'])
def Select_BusinessDoctors():
    return Select_BusinessandDoctors(request)






if __name__ == '__main__':
   app.run(host="192.168.1.2",port=5000)

