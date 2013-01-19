#-----------------------------------------------------------------------------
# Name: getBruinSchedule.py
# Purpose: contains functions to retrieve class information from the UCLA registrar website
#
# Author: <Samping Chuang>
# Email : sampingchuang@gmail.com
#
# Created: 2013/01/18
# Copyright: (c) 2013
# Licence: <your licence>
#-----------------------------------------------------------------------------


import urllib2
from BeautifulSoup import BeautifulSoup
import json


#return the avaliable ucla terms and majors
def get_terms_majors():
    #initialize
    result = {}
    result['terms'] = {}
    result['majors'] = {}
    
    #retrieve page
    url = "http://www.registrar.ucla.edu/schedule/schedulehome.aspx"
    webPage = urllib2.urlopen(url).read()
    soup = BeautifulSoup(webPage)

    #parse terms
    terms = soup.find("select", {"id":"ctl00_BodyContentPlaceHolder_SOCmain_lstTermDisp"}).findChildren()
    for term in terms:
        result['terms'][term['value']] = term.contents[0]

    #parse class
    majors = soup.find("select", {"id":"ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea"}).findChildren()
    for major in majors:
        result['majors'][major['value']] = major.contents[0]
    #return json.dumps(result, indent=4)
    return result




#returns the classes avaliable given the terms and majors
def get_major_classes(term, major):
    result = {}
    result['term_sel'] = term
    result['major_sel'] = major
    result['classes'] = {}
    #retrieve page
    url = 'http://www.registrar.ucla.edu/schedule/crsredir.aspx?'+'termsel='+term+'&subareasel='+major
    #print url
    webPage = urllib2.urlopen(url).read()
    soup = BeautifulSoup(webPage)

	#get classes
    resClasses = soup.find("select", {"id":"ctl00_BodyContentPlaceHolder_crsredir1_lstCourseNormal"})
    if resClasses is None:
        result['has_class']='false';
    else:
        result['has_class']='true';
        resClasses = resClasses.findChildren()
        for resClass in resClasses:
            result['classes'][resClass['value']] = resClass.contents[0]
    #return json.dumps(result, indent=4)
    return result





#returns the class information
def get_class_info(term, major, crs):
    #initialize
    result = {}
    result['term_sel'] = term
    result['major_sel'] = major
    result['idxcrs']= crs
    result['lectures'] = []
    #retrieve page
    url = 'http://www.registrar.ucla.edu/schedule/detselect.aspx?'+'termsel='+term+'&subareasel='+major+'&idxcrs='+crs
 
    webPage = urllib2.urlopen(url).read()
    soup = BeautifulSoup(webPage)
    #problem with find on div using element id (when nested too many levels, the content are lost)
	#see http://stackoverflow.com/questions/2136267/beautiful-soup-and-extracting-a-div-and-its-contents-by-id
	#break down wrapper by wrapper
	#<body> -> <form> -> <center> -> <div> -> <center> -> <table> -> <tbody> -> 2nd tr -> 2nd td -> div
    sec = soup.find('body').find('form').find('center').find('div').find('center').findChildren('table')
    
    if len(sec) == 1:
        result['has_class']='false';
    else:
        result['has_class']='true';
        #the fist element in test is bs
        tables = sec[1:]
        
        # structure Rules (example: cs32)
        # <table class = "tblClassListingBody">
        # 	- Class Information/Notes
        # <table class = "dgdTemplateGrid" id ="dgdCourseHeaderCOM SCI0032">
        #	- Course Header (pretty much just the title)
        # <table class = "dgdTemplateGrid" id ="dgdDeptURLsCOM SCI0032">
        #	- Catalog / Definition Links
        #
        # --------The following repeats when there are more than 1 lecture
        #
        # <table class = "dgdTemplateGrid" id ="dgdLectureHeaderCOM SCI0032">
        #	- Lecture 1 Nachenberg
        # <table class = "dgdTemplateGrid" id ="dgdClassURLHeaderCOM SCI0032">
        #	- Course Webpage   Library Reserves   Textbooks  
        # <table class = "dgdTemplateGrid"> 
        #	- Actual Enrollment 
        
        
        for t in tables:
            t_id = t.get('id') 
            t_class = t.get('class')    
            
            new_sec = {}
            
            #for actual enrollment
            if t_id is None and t_class == "dgdTemplateGrid":
                t_tr = t.findAll('tr')
                lecture_td = t_tr[1].findAll('td')
                
                #grab lecture information
                for i in range(0, len(lecture_td)):
                    td_class = lecture_td[i].get('class')
                    td_val   = lecture_td[i].find('span',{'class':'bold'})
                    if td_val is not None:
                       td_val = td_val.string
                    if td_class == "dgdClassDataColumnIDNumber":
                       new_sec['ID']= td_val
                    elif td_class == "dgdClassDataActType":
                       new_sec['type']= td_val
                    elif td_class == "dgdClassDataSectionNumber":
                       new_sec['sec']= td_val
                    elif td_class == "dgdClassDataDays":
                       new_sec['days']= td_val
                    elif td_class == "dgdClassDataTimeStart":
                       new_sec['time_start']= td_val
                    elif td_class == "dgdClassDataTimeEnd":
                       new_sec['time_end']= td_val
                    elif td_class == "dgdClassDataBuilding":
                       new_sec['building']= td_val
                    elif td_class == "dgdClassDataRoom":
                       new_sec['room']= td_val;
                    elif td_class == "dgdClassDataRestrict":
                       new_sec['restrict']= td_val
                    elif td_class == "dgdClassDataEnrollTotal":
                       new_sec['enroll_total']= td_val
                    elif td_class == "dgdClassDataEnrollCap":
                       new_sec['enroll_cap']= td_val
                    elif td_class == "dgdClassDataWaitListTotal":
                       new_sec['waitl_total']= td_val
                    elif td_class == "dgdClassDataWaitListCap":
                       new_sec['waitl_cap']= td_val
                    elif td_class == "dgdClassDataStatus":
                       new_sec['status']= td_val	
                #grab secion information
                #sec_num = 0 
                if len(t_tr) <=2:
                    new_sec['has_section'] = False
                else:
                    new_sec['has_section'] = True
                    sections = []
                    for i in range(2, len(t_tr)):
                        
                        sec_td = t_tr[i].findAll('td')
                        s = {}
                      
                        #grab lecture information
                        for j in range(0, len(sec_td)):
                            
                            td_class = sec_td[j].get('class')
                            
                            td_val   = sec_td[j].find('span')
                            if td_val is not None:
                               td_val = td_val.string
                            
                            if td_class == "dgdClassDataColumnIDNumber":
                               s['ID']= td_val
                            elif td_class == "dgdClassDataActType":
                               s['type']= td_val
                            elif td_class == "dgdClassDataSectionNumber":
                               s['sec']= td_val
                            elif td_class == "dgdClassDataDays":
                               s['days']= td_val
                            elif td_class == "dgdClassDataTimeStart":
                               s['time_start']= td_val
                            elif td_class == "dgdClassDataTimeEnd":
                               s['time_end']= td_val
                            elif td_class == "dgdClassDataBuilding":
                               s['building']= td_val
                            elif td_class == "dgdClassDataRoom":
                               s['room']= td_val;
                            elif td_class == "dgdClassDataRestrict":
                               s['restrict']= td_val
                            elif td_class == "dgdClassDataEnrollTotal":
                               s['enroll_total']= td_val
                            elif td_class == "dgdClassDataEnrollCap":
                               s['enroll_cap']= td_val
                            elif td_class == "dgdClassDataWaitListTotal":
                               s['waitl_total']= td_val
                            elif td_class == "dgdClassDataWaitListCap":
                               s['waitl_cap']= td_val
                            elif td_class == "dgdClassDataStatus":
                               s['status']= td_val	
                        sections.append(s)
                            #sec_num+=1
                    if sections:
                        new_sec['class_sections'] = sections
            if new_sec:
                result['lectures'].append(new_sec)   
    #return in json form
    #return json.dumps(result, indent=4)
    return result
    

