from sqlwrapper import gensql,dbget,dbput
import json
from datetime import datetime
import time
from flask import Flask,request,jsonify

def Select_BusinessandDoctors(request):
  #try:
    st_time = time.time()
    d = request.json
    # Get all business profile from db dpends on county and city
    business = json.loads(dbget("SELECT * FROM new.business_profile where country='"+d['country']+"'"
                                " and city='"+d['city']+"' "))
    #print(business)
    specialist_type = list(set(bus['specialist'] for bus in business))
    print(specialist_type)
    specialist = []
    doc_only_specialist = {}
    #This loop segregate business based on specialist
    for bus in business:
      #print(bus)
      typeofspecialist = bus['specialist']
      index_no = specialist_type.index(typeofspecialist)
      try:
         #image 
         bus['cli_img'] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgVP5mZIHuzWfgDlzcJzDmNqpLl1ARDgnVA8OXgUszKk31sqTcXA"
         #image
         bus.update({"cli_subimages1":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRF-K-m966PMU0Mn1Inf7OilRSfn6QDYUaiVCIvCGtMqrIUN0J5Ow","cli_subimages2":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSu6K0HVZTagXvi3banJF6kFV0R1Z9jrie0UQk4dp7A88_dWtXv0A","cli_subimages3":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSO7GQ74BRcJty89sPDhPwo1S_UyLFrVSMy9APw0sfZrUjdIRbJ"})
         bus['cli_feedback'] = json.loads(dbget("select count(*) from new.feedback where "
                                                "business_id='"+str(bus['business_id'])+"'"))[0]['count']
         bus['cli_doc_count'] = json.loads(dbget("select count(*) from new.doctorinbusiness where "
                                                 "business_id='"+str(bus['business_id'])+"'"))[0]['count']
         specialist[index_no].append(bus)
      except:
          #image
          bus['cli_img'] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgVP5mZIHuzWfgDlzcJzDmNqpLl1ARDgnVA8OXgUszKk31sqTcXA"
          #image
          bus.update({"cli_subimages1": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRF-K-m966PMU0Mn1Inf7OilRSfn6QDYUaiVCIvCGtMqrIUN0J5Ow", "cli_subimages2": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSu6K0HVZTagXvi3banJF6kFV0R1Z9jrie0UQk4dp7A88_dWtXv0A", "cli_subimages3": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSO7GQ74BRcJty89sPDhPwo1S_UyLFrVSMy9APw0sfZrUjdIRbJ"})
          bus['cli_feedback'] = json.loads(dbget("select count(*) from new.feedback where "
                                                 "business_id='"+str(bus['business_id'])+"'"))[0]['count']
          bus['cli_doc_count'] = json.loads(dbget("select count(*) from new.doctorinbusiness "
                                                  "where business_id='"+str(bus['business_id'])+ "'"))[0]['count']
          specialist.append([bus])

    #print("sp",specialist)
    # Main  loop
    for i in specialist:
        #print("listofspecial",i)
        for a in i:
          #print("a",a)
          b_id = a['business_id']
          #print("id",b_id)
          new_dict = {k:v for k,v in a.items()
                       if k in ('business_name', 'area','address','location_lat','location_long')}
          # Get the timing based on business
          timing = json.loads(dbget("select day,start_timing,end_timing from new.timing "
                                                        "where business_id='"+str(a['business_id'])+"'"
                                                        "and doctor_id='0' "))
          #print("timing",timing)
          # Loop for format timing of business profile
          for t in timing:
              timing[timing.index(t)] = {'day':t['day'],
                                         'timing':""+datetime.strptime(t['start_timing'], "%H:%M").strftime("%I:%M %p")+"-"
                                                ""+datetime.strptime(t['start_timing'], "%H:%M").strftime("%I:%M %p")+""}
                                                #,'evening':''}
          #image    
          new_dict['clinic_images'] = [{"img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBJm3R3lzyCGykNGsJQgOel1pu7JIAGW4Lga8Edt_24ONfXa2r"},{"img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQae0MXFfNe1aL7oCl-yEtW1Mat_cxE7fIvv6qsDvmv5SK-HWd6Qg"},{"img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTprOKWBWD4SOvmvaz7C7lGLdHm1Kr8NKPLluV3NQEeYSq19zwP"}]
          new_dict['clinic_timings'] = timing
          doctorinbusiness = json.loads(dbget("select * from new.doctor_profile where "
                                              "doctor_profile_id in (select doctor_id from "
                                              "new.doctorinbusiness where business_id='"+str(b_id)+"')"))

          # Doctor details inside the business details
          for docinbus in doctorinbusiness:
              #image
              docinbus['doc_img'] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSa_RWfFQvBdKuh09_xc1FIiINdbaevnMgECXuPTliIOXKcdLc3lw"
              docinbus['doc_available_date'] = "Fri,13 Dec"
              docinbus['doc_available_location'] = ""
              docinbus['doc_hospital'] = ""
              docinbus['doc_feedback'] = ""

              docinbus['doctor_details'] = [docinbus.copy()]
              doc_timing = json.loads(dbget("select day,start_timing,end_timing from new.timing "
                                        " where business_id='"+str(a['business_id'])+"'"
                                        " and doctor_id='"+docinbus['doctor_profile_id']+"' "))
              #print("doc timing", doc_timing)
              # Loop for format timing of doctor profile
              for t in doc_timing:
                  #print("t",t,type(t))
                  doc_timing[doc_timing.index(t)] = {'day': t['day'],
                                                 'morning': ""+datetime.strptime(t['start_timing'], "%H:%M").strftime("%I:%M %p")+"-"
                                                 ""+datetime.strptime(t['start_timing'],"%H:%M").strftime("%I:%M %p")+""
                                                 ,'evening':''}
                  #print("doc_timing", doc_timing,type(doc_timing))
              docinbus['doctor_details'][0]['doctorstimings'] = doc_timing

              docinbus['doctor_details'][0]['doctor_clinic'] = json.loads(dbget("select * from new.business_profile where "
                                                                                " business_id in (SELECT business_id FROM new.doctorinbusiness "
                                                                                " where doctor_id='"+docinbus['doctor_profile_id']+"')"))
              for docbus in docinbus['doctor_details'][0]['doctor_clinic']:
                  docbus['clinic_rating'] = ''
                  docbus['clinic_kms'] = ''

              docinbus['doctor_details'][0]['doctor_feedback'] = json.loads(dbget("select new.feedback.*,new.user_profile.user_name from new.feedback "
                                                                                  " join new.user_profile on feedback.mobile=user_profile.mobile "
                                                                                  " where business_id='"+str(a['business_id'])+"'"
                                                                                  " and doctor_id='"+docinbus['doctor_profile_id']+"'"))
              #print("cus_feedback",docinbus['doctor_details'][0]['doctor_feedback'])
              for fe in docinbus['doctor_details'][0]['doctor_feedback']:
                  fe['visited'] = '1 month ago'

              #image 
              docinbus['doctor_details'][0]['doctor_clinic_img'] = [{"img":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNBmYOXOSuTes0Xpc7GPICQeg4KijVB5JzhA9Xay68lk9gs96cnw"},{"img":"http://www.chapelhillfamilydoctors.com.au/images/doctor-img2.png"},{"img":"http://healthstaff.co.za/wp-content/uploads/2017/07/doctor.png"}]
              docinbus['doctor_details'][0]['doctor_specialization'] = json.loads(dbget("SELECT new.specialization.* "
                                                                                        " FROM new.doctor_profile join new.doctor_specialization on"
                                                                                        " doctor_profile.doctor_profile_id = doctor_specialization.doctor_id"
                                                                                        " join new.specialization on doctor_specialization.specialization_id = "
                                                                                        " specialization.specialization_id"
                                                                                        " where doctor_profile.doctor_profile_id='"+docinbus['doctor_profile_id']+"'"))

              docinbus['doctor_details'][0]['doctor_services'] = json.loads(dbget("SELECT new.services.* "
                                                                                  " FROM new.doctor_profile join new.doctor_services on"
                                                                                  " doctor_profile.doctor_profile_id = doctor_services.doctor_id"
                                                                                  " join new.services on doctor_services.service_id = services.service_id"
                                                                                  " where doctor_profile.doctor_profile_id='"+docinbus['doctor_profile_id']+"'"))
          new_dict['clinic_doctor_list'] = doctorinbusiness

          for doc in doctorinbusiness:
              #if doc['specialist'] not in doc_only_specialist:
              #    doc_only.append(doc)
              try:

                 #print(doc_only_specialist[''+doc['specialist']+''])
                 doc_only_specialist[''+doc['specialist']+''].append(doc)
                 #print("try")
              except:
                  #print("except")
                  doc_only_specialist[''+doc['specialist']+''] = [doc]

          # Get service data for business profile
          bus_service = json.loads(dbget("select new.services.* from new.doctor_services"  
                                                         " join new.services"
                                                         " on doctor_services.service_id = services.service_id where" 
                                                         " new.doctor_services.doctor_id" 
                                                         " in (select doctor_id from new.doctorinbusiness" 
                                                         " where business_id='"+str(b_id)+"') "))
          service = []
          service_set = set()
          # Loop for format service datas for business  profile
          for b_ser in bus_service:
              if b_ser['service_name'] not in service_set:
                  service.append({"service":b_ser['service_name']})
                  service_set.add(b_ser['service_name'])

          new_dict['clinic_services'] = service
          new_dict['clinic_open'] = "Open Today"
          a["clinic_details"] = [new_dict]

        #print("doc_only_specialist",doc_only_specialist)

        if i[0]['specialist'] in doc_only_specialist:
            doc_list = doc_only_specialist[""+i[0]['specialist']+""]
        else:
            doc_list = []
        specialist[specialist.index(i)] = {"name":i[0]['specialist'],"icon":"","Listofdoctors":[{"clinics":i,
                                           "Doctors":doc_list}]}
        #print("sm_sp",specialist)
    ed_time=time.time()
    full_time = ed_time - st_time
    #print("spcialist", specialist)
    print("Time Taken",full_time)
    return (json.dumps(
        {"Message": "Records Selected Sucessfully", "MessageCode": "RSS",
         "Service Status": "Success","specialist":specialist}, indent=4))
