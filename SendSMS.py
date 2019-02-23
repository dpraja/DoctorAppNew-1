import urllib.request
import time
import json
import psycopg2
from flask import Flask, request, jsonify


def sendsms(request):
    #try:

        count = []
        message = request.json['message']

        con = psycopg2.connect(user='xcymzcxxbjjeew',
                               password='f431978a86d99ceaf4b114885091d9cc100c9d4ce12d1f6eb5efa80b8e868581',
                               host='ec2-54-75-231-3.eu-west-1.compute.amazonaws.com', port='5432',
                               database='d95ji8upkp95ss')
        cur = con.cursor()
        d = request.json
        if len(d) == 3:
            sql = "select mobile  from new.appointment where business_id='" + str(
                d['business_id']) + "' and doctor_id='" + d['doctor_id'] + "'"
        else:
            business_date = request.json['business_date']
            business_id = request.json['business_id']
            token_status = request.json['token_status']
            doctor_id = request.json['doctor_id']
            sql = "select mobile  from new.appointment where business_id='" + str(
                business_id) + "' and doctor_id='" + doctor_id + "'\
                   and business_date= '" + business_date + "' and token_status='" + token_status + "'"
        cur.execute(sql)

        results = cur.fetchall()
        for result in results:
            for i in result:
                count.append(i)

        for mobile in count:
            print(mobile)
            time.sleep(2)
            url = "https://control.msg91.com/api/sendhttp.php?authkey=195833ANU0xiap5a708d1f&mobiles=" + mobile + "&message=" + message + "&sender=Infoit&route=4&country=91"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
                the_page = the_page[1:]
                print(the_page)
                the_page = str(the_page)
        con.close()

        return (json.dumps({"Message": "Sms Sent Successfully", "Message_Code": "SSS", "Service_Status": "Success"},
                           indent=2))

    #except:
       # return (json.dumps({"Message": "Sms Sent UnSuccessfully", "Message_Code": "SSUS", "Service_Status": "Failure"},
                           #indent=2))

def Sendmessge(request):
         print("hiiiii")
         
         if request.method=='POST':
                
                 mobile = request.json['mobile']
                 message = request.json['message']
                 code =  request.json['code']
                 print(mobile, message, code)
         else:
                mobile = request.args['mobile']
                message = request.args['message']
                code =  request.args['code']
                print(mobile, message, code)
                
         url = "https://control.msg91.com/api/sendhttp.php?authkey=195833ANU0xiap5a708d1f&mobiles="+mobile+"&message="+message+"&sender=Infoit&route=4&country="+code+""
         req = urllib.request.Request(url)
         with urllib.request.urlopen(req) as response:
            the_page = response.read()
            the_page = the_page[1:]
            print(the_page)
            the_page = str(the_page)
         return(json.dumps({"Message":"SMS Sent Sucessfully","Key":the_page},indent =2))
        #return("hi")    
