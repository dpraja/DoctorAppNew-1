from sqlwrapper import gensql, dbget, dbput
import json
import datetime
import time
from time import mktime
from flask import Flask, request, jsonify


def tokengeneration(request):
    try:
        d = request.json
        mob = json.loads(dbget("select count(*) as mobile from new.appointment where mobile ='"+d['mobile']+"' and business_date = '" + str(d['business_date']) + "' "))
        if mob[0]['mobile'] == 1:
            return(json.dumps({'Message': 'Token Already Generated', 'Message_Code': 'TAG', 'Status': 'Failure',},indent=4))
        doctorid = json.loads(dbget("select count(*) as doctor_id from new.doctor_profile where doctor_profile_id ='"+d['doctor_id']+"'"))
        mobile = json.loads(dbget("select count(*) as mobile from new.user_profile where mobile ='"+d['mobile']+"'"))
        businessid = json.loads(dbget("select count(*) as business_id from new.business_profile where business_id ='"+str(d['business_id'])+"'"))
        if mobile[0]['mobile'] == 1 and doctorid[0]['doctor_id'] == 1 and businessid[0]['business_id'] == 1:
                dt = datetime.datetime.strptime(d['business_date'], '%Y-%m-%d').date()  # to convert string to date format
                currenttime = datetime.datetime.now()  # to get current datetime
                todaydate = currenttime.date()
                todaytime = currenttime.strftime('%H:%M')  # to get current time
                doc_id = {k: v for k, v in d.items() if k in ('doctor_id', 'business_id')}
                docidval = doc_id.get("doctor_id")
                bus_id = doc_id.get("business_id")
                x = currenttime.strftime("%a")[:3].lower()
                b = json.loads(dbget("select end_timing from new.timing where doctor_id = '" + str(docidval)+"' and business_id = '"+str(bus_id)+"'\
                                    and day = '"+str(x)+"' and session='evening'"))
                etime = b[0]['end_timing']  # to get value from list
                if dt == todaydate and etime > todaytime:
                    a = {k: v for k, v in d.items() if k in ('doctor_id', 'business_id', 'business_date')}
                    res = json.loads(gensql('select', 'new.token_no', 'count(*)', a))
                    if res[0]['count'] == 0:
                        a['token_no'] = 0
                        gensql('insert', 'new.token_no', a)
                    token = json.loads(gensql('select', 'new.token_no', 'token_no', a))
                    if token[0]['token_no'] ==0:
                        no = 1
                    else:
                        no = token[0]['token_no'] + 1
                    d['token_no'] = no
                    d['token_time'] = currenttime
                    gensql('insert', 'new.appointment', d)
                    wt = json.loads(dbget("select average_waiting_time from new.doctorinbusiness where doctor_id = '"+str(docidval)+"' and business_id = '"+str(bus_id)+"'"))
                    waittime = wt[0]['average_waiting_time']
                    if no == 1:
                        avg_wait = 0
                    else:
                        avg_wait = (no - 1) * waittime
                    dbput("update new.token_no set token_no ='"+str(no)+"' where doctor_id='"+str(a['doctor_id'])+"' and business_id = '"+str(bus_id)+"'")
                    return (json.dumps(
                        {'Message': 'Token Generated', 'Message_Code': 'TGS', 'Status': 'success', 'Token_No': no,
                         'waiting_time': avg_wait}, indent=4))

                else:
                    return (json.dumps({"Message": "Token should be Generated only for Today Date", "Message_Code": "TGTD",
                                        "Service Status": "Failure"}, indent=4))
        else:
                return(json.dumps({'Message': 'Invalid Data', 'Message_Code': 'ID', 'Status': 'Failure'},indent=4))
    except:
        return (json.dumps({"Message": "Token Generation UnSuccessful", "Message_Code": "TGUS", "Service_Status": "Failure"},indent=4))


def selectappointment(request):
    try:
        d = request.json
        output = json.loads(dbget("select new.appointment.*,new.user_profile.* from new.appointment \
                                            join new.user_profile on new.appointment.mobile = new.user_profile.mobile where\
                                           new.appointment.doctor_id = '" + str(
            d['doctor_id']) + "' and new.appointment.business_id = '" + str(d['business_id']) + "'\
                                           and new.appointment.business_date = '" + str(
            d['business_date']) + "' order by new.appointment.token_no"))
        return (json.dumps(
            {"Message": "Appointments Selected Sucessfully", "Message_Code": "ASS", "Service_Status": "Success",
             "output": output}, indent=4))
    except:
        return (json.dumps(
            {"Message": "Appointments Selected Unsuccessful", "Message_Code": "ASUS", "Service_Status": "Failure"},
            indent=4))
def updatetoken(request):
    try:
        d = request.json
        app_id = json.loads(dbget("select count(*) as appointment_id from new.appointment where appointment_id ='"+str(d['appointment_id'])+"'"))
        if app_id[0]['appointment_id']==1:
                dbput("update new.appointment set token_status='" + str(d['token_status']) + "'  where appointment_id='" + str(d['appointment_id']) + "'")
                return (json.dumps({"Message": "Record Updated Successfully", "Message_Code": "RUS", "Service_Status": "Success"},indent=4))
        else:
              return(json.dumps({'Message': 'Invalid Data', 'Message_Code': 'ID', 'Status': 'Failure'},indent=4))
    except:
        return (json.dumps({"Message": "Appointments Updated Unsuccessful", "Message_Code": "AUUS", "Service_Status": "Failure"},indent=4))
def count(request):
    try:
        d = request.json
        doctorid = json.loads(dbget("select count(*) as doctor_id from new.doctor_profile where doctor_profile_id ='"+d['doctor_id']+"'"))
        businessid = json.loads(dbget("select count(*) as business_id from new.business_profile where business_id ='"+str(d['business_id'])+"'"))
        if doctorid[0]['doctor_id'] == 1 and businessid[0]['business_id'] == 1:
                b_count = json.loads(dbget("select count(*) as bo_count from new.appointment \
                                              where token_status='Booked' and doctor_id='" + str(
                    d['doctor_id']) + "' and business_id = '" + str(d['business_id']) + "'\
                                               and new.appointment.business_date = '" + str(d['business_date']) + "'"))
                booked_count = b_count[0]['bo_count']
                c_count = json.loads(dbget("select count(*) as can_count from new.appointment \
                                              where token_status='Cancel' and doctor_id='" + str(
                    d['doctor_id']) + "' and business_id = '" + str(d['business_id']) + "'\
                                               and new.appointment.business_date = '" + str(d['business_date']) + "'"))
                canceled_count = c_count[0]['can_count']
                co_count = json.loads(dbget("select count(*) as checkout_count from new.appointment \
                                              where token_status='Checkout' and doctor_id='" + str(d['doctor_id']) + "' and business_id = '" + str(d['business_id']) + "' \
                                              and new.appointment.business_date = '" + str(d['business_date']) + "'"))
                cheout_count = co_count[0]['checkout_count']
                return (json.dumps(
                    {"Message": "Token number Counted  Sucessfully", "Message_Code": "TNS", "Service_Status": "Success"
                        , "booked_count": booked_count, "canceled_count": canceled_count, "Checked_out": cheout_count},
                    indent=4))
        else:
              return(json.dumps({'Message': 'Invalid Data', 'Messag_Code': 'ID', 'Status': 'Failure'},indent=4))  
    except:
        return (json.dumps(
            {"Message": "Token number Counted Unsuccessful", "Message_Code": "TNUS", "Service_Status": "Failure"},indent=4))


def livefeed(request):
    try:
        d = request.json
        doctorid = json.loads(dbget("select count(*) as doctor_id from new.doctor_profile where doctor_profile_id ='"+d['doctor_id']+"'"))
        businessid = json.loads(dbget("select count(*) as business_id from new.business_profile where business_id ='"+str(d['business_id'])+"'"))
        if doctorid[0]['doctor_id'] == 1 and businessid[0]['business_id'] == 1:
            output = json.loads(dbget("select new.appointment.*,new.user_profile.* from new.appointment \
                                join new.user_profile on new.appointment.mobile = new.user_profile.mobile \
                                where token_status in ('Cancel','Checkout')\
                                and doctor_id='" + str(d['doctor_id']) + "' order by token_no "))
            return (json.dumps({"message": "livefeed Successful", "Message_Code": "LS",'Status': 'Sucess', "output": output},indent=4))
        else:
              return(json.dumps({'Message': 'Invalid Data', 'Message_Code': 'ID', 'Status': 'Failure'},indent=4))
    except:
       return (json.dumps({"Message": "Livefeed Unsuccessful", "Message_Code": "LUS", "Service_Status": "Failure"},indent=4))


def average_waiting_time(request):
    try:
        d = request.json
        doctorid = json.loads(dbget("select count(*) as doctor_id from new.doctor_profile where doctor_profile_id ='"+d['doctor_id']+"'"))
        businessid = json.loads(dbget("select count(*) as business_id from new.business_profile where business_id ='"+str(d['business_id'])+"'"))
        if doctorid[0]['doctor_id'] == 1 and businessid[0]['business_id'] == 1:
                wt = json.loads(dbget("select average_waiting_time from new.doctorinbusiness where doctor_id = '" + str(
                    d['doctor_id']) + "' and business_id = '" + str(d['business_id']) + "'"))
                waittime = wt[0]['average_waiting_time']
                tk_time = json.loads(dbget("select token_time from new.appointment where doctor_id = '" + str(
                    d['doctor_id']) + "' and business_id = '" + str(d['business_id']) + "'\
                                          and mobile = '" + str(d['mobile']) + "'and business_date = '" + str(
                    d['business_date']) + "'"))
                token_time = tk_time[0]['token_time']
                count = json.loads(
                    dbget("select count(*) as count from new.appointment where  token_time <'" + str(token_time) + "' and\
                                         business_id = '" + str(d['business_id']) + "' and business_date = '" + str(d['business_date']) + "'\
                                         and token_status = 'Booked'"))
                avg_wait = count[0]['count'] * waittime
                return (json.dumps(
                    {"message": "Average Waittime Calculated Sucessfully ", "Message_Code": "AWCS","Service_Status": "Sucess", "Wait_time": avg_wait},indent=4))
        else:
              return(json.dumps({'Message': 'Invalid Data', 'Message_Code': 'ID', 'Status': 'Failure'},indent=4))
    except:
        return (json.dumps({"Message": "Average Waittime Calculated  Unsuccessful", "Message_Code": "AWCUS","Service_Status": "Failure"}, indent=4))









