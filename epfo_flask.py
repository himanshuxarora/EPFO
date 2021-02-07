from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
# browser = webdriver.Firefox(executable_path=r'C:\Users\Zebronics\Desktop\jupyter_program\geckodriver.exe')
# browser.get('https://unifiedportal-emp.epfindia.gov.in/epfo/')
import requests
import json
from datetime import datetime
import csv
import time
from excel2json import convert_from_file
import openpyxl 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as cond

global dict_drivers
dict_drivers={}



# logs function for EPFO 
tokenfinal=""

def myprint(emp_id,status):
    global tokenfinal
    datalog = {"emp_id":emp_id,"log_text":status} 
    headers = {'Authorization': tokenfinal}
    url="http://52.15.230.9/api/Employee/addlogepfo"
    response = requests.post(url, data=datalog, headers=headers)
    a=json.loads(response.text)
    print(" RESPONSE FOR LOGS",a)
    print("Log status ",datalog)


def register_individual_no(ddict,browser):
    global tokenfinal
    print('selecting Title')
    mr_dict = {1:'Mr.',2:'Ms.',3:'Mrs.'}
    mr_text = ddict['Title']
    for key in mr_dict:
        if(mr_dict[key] == mr_text):
            mr = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/form/div[2]/div[2]/div[2]/div[1]/select/option['+str(key)+']').click()
    m_name = browser.find_element_by_id('memberName').send_keys(ddict['Name'])
    epfo_name= ddict['Name']
    dob=ddict['DOB'].split('/')
    d=dob[0]
    m=dob[1]
    y=dob[2]
    if(len(d)==1 or len(m)==1):
        if(int(d)<10):
            d='0'+d
        if(int(m)<10):
            m='0'+m
            dob=d+'/'+m+'/'+y
    else:
        dob=d+'/'+m+'/'+y
    print(" Date of Birth",dob)
    m_date= browser.find_element_by_id('dob').send_keys(dob)
    m_name = browser.find_element_by_id('memberName').click()
    time.sleep(2)
    g_val = ddict['Gender']
    gen_dict = {1:'Male' , 2:'Female' , 3:'Transgender'}
    for gkey in gen_dict:
        if(gen_dict[gkey].upper() == g_val.upper()):
            gen = browser.find_element_by_id('currentDetails.genderCode'+str(gkey))
            gen.click()
    nation = Select(browser.find_element_by_id('nationality'))
    nation_text = str(ddict['Nationality'])
    if(nation_text.upper() !="INDIAN"):
        for n in nation.options:
            if(n.text == nation_text):
                x = n.get_attribute('value')
                nation.select_by_value(x)
                time.sleep(2)
    saveLocation = "./Images_epfo/Yes"+str(ddict['Name'])+".png"
    browser.save_screenshot(saveLocation)
    f_h_name =browser.find_element_by_id('fatherHusbandName').send_keys(ddict['Father Husband Name'])

    rel_dict = {'F':'Father' , 'H':'Husband'}
    relation = Select(browser.find_element_by_id('relation'))
    rel_text = ddict['Relation']
    for f in relation.options:
        if(f.text.strip() == rel_text.strip() ):
            fh= f.get_attribute('value')
            relation.select_by_value(fh)
            time.sleep(2)
    m_dict = {'M':'MARRIED' , 'U':'UN-MARRIED' , 'W':'WIDOW/WIDOWER', 'D':'DIVORCEE' }
    m_status = Select(browser.find_element_by_id('maritalStatus'))
    m_text = ddict['Marital Status'].upper()
    print("going to fill Marital stATUS")
    for ms in m_status.options:
        if(ms.text == m_text ):
            mh= ms.get_attribute('value')
            m_status.select_by_value(mh)
            time.sleep(2)      
    print("going to fill mobile number")
    mb=int(ddict['Mobile'])
    mobile = browser.find_element_by_id('mobileNo').send_keys(mb)
    print("going to fill email")
    email = browser.find_element_by_id('emailId').send_keys(ddict['Email'])

    q_dict = {1:'ILLITERATE' , 3: 'NON-MATRIC', 4:'MATRIC', 
              5:'SENIOR-SECONDARY', 6:'GRADUATE', 7:'POST-GRADUATE', 
              8:'DOCTORATE', 9:'TECHNICAL (PROFESSIONAL)'}
    print("Going to fill qualification")
    qualification = Select(browser.find_element_by_id('qualification'))
    q_text = ddict['Qualification'].upper()
    for q in qualification.options:
        if(q.text == q_text ):
            gh= q.get_attribute('value')
            qualification.select_by_value(gh)
            time.sleep(2)
    doj=ddict['Date of joining'].split('/')
    dj=doj[0]
    mj=doj[1]
    yj=doj[2]
    if(len(dj)==1 or len(mj)==1):
        if(int(dj)<10):
            dj='0'+dj
        if(int(mj)<10):
            mj='0'+mj
            doj=dj+'/'+mj+'/'+yj
    else:
        doj=dj+'/'+mj+'/'+yj
    print(" DATE OF JOINING ",doj)
    d_join = browser.find_element_by_id('doj').send_keys(doj)
    wag = browser.find_element_by_id('wages').click()
    time.sleep(2)
    if(ddict['Wages']):
        wage = browser.find_element_by_id('wages').send_keys(int(ddict['Wages']))
    inter_text = ddict['International Worker'].upper()
    if(inter_text == 'YES'):
        inter_worker = browser.find_element_by_id('isInternationalWorker').click()
        natcon = Select(browser.find_element_by_id('countryOfOrigin'))
        n_text = ddict['Country Of Origin']
        for nc in natcon.options:
            if(nc.text == n_text):
                x = nc.get_attribute('value')
                natcon.select_by_value(x)
                time.sleep(2)
        passvaild = browser.find_element_by_id('passportValidFrom').send_keys(ddict['Passport Valid From'])
        passport = browser.find_element_by_id('passportNumber').click()
        time.sleep(2)
        passvaildupto = browser.find_element_by_id('passportValidTill').send_keys(ddict['Passport Valid Till'])
        #passportt = browser.find_element_by_id('passportNumber').click()
        passporttt = browser.find_element_by_id('passportNumber').send_keys(ddict['Passport Number'])

        time.sleep(2)
    diff_text = ddict['Differently Abled'].upper()
    if(diff_text == 'YES'):
        disablity = browser.find_element_by_id('isPhisicalHandicap').click()
        dis = browser.find_element_by_id('tdphisicalHandicapType')
        dis2 = dis.find_elements_by_class_name('col-sm-12')
        d_text = ddict['Disability Type']
        for d in dis2:
            d_t = d.text
            d_t = d_t.lstrip()
            if(d_t == d_text):
                d_k = browser.find_element_by_id('physicalHandicap'+str(d_t)).click()

    #Add adhar doc
    time.sleep(2)
    adhr = browser.find_element_by_id('chkDocTypeId_2').click()
    adhrdoc = browser.find_element_by_id('docNo2').send_keys(int(ddict['Aadhaar Number']))
    time.sleep(2)
    saveLocation = "./Images_epfo/register data.png"
    browser.save_screenshot(saveLocation)
    adhrname = browser.find_element_by_id('nameOnDoc2').send_keys(ddict['Name'])
    inpts=browser.find_elements_by_tag_name('input')
    for inpt in inpts:
        if(inpt.get_attribute('name')=='save'):
            print('found save button')
            inpt.click()
            break
    time.sleep(2)    
    try:
        error_text=''
        browser.switch_to.alert.accept()
        time.sleep(5)
        timeout = 180
        #driver.set_page_load_timeout(30)
        #driver.manage().timeouts().pageLoadTimeout(50, TimeUnit.SECONDS);
        element_present = EC.presence_of_element_located((By.ID, 'memberName'))
        WebDriverWait(browser, timeout).until(element_present)
        p_tag = browser.find_elements_by_tag_name("p")
        for p in p_tag:
            if(p.get_attribute("style") == "color:red;"):
                myprint( str(ddict["Id"]),"Error "+ p.text)
                error_text=str(p.text)
        # find div for class form-group to get error message into KYC detail
        tags_div = browser.find_elements_by_class_name("error")
        for t_d in tags_div:
            time.sleep(2)
            print("Error in KYC detail for "+ ddict['Name']+ t_d.text)
            myprint(str(ddict["Id"]),"Error in KYC detail for "+str(ddict['Name'])+ " ** "+ str(t_d.text))
            error_text=str(t_d.text)
        time.sleep(2)
        try:
            emp_id= str(ddict["Id"])
            dataep = {"emp_id":emp_id,"reason":error_text} 
            headers = {'Authorization': tokenfinal}
            url="http://52.15.230.9/api/Employee/error_employee_epfo"
            response = requests.post(url, data=dataep, headers=headers)
            a=json.loads(response.text)
            print(a)
        except:
            print(" error in error_employee_epfo")
        if(error_text):
            print("error")
        else:
            myprint(str(ddict["Id"]),"Data Save Successfully")
        
    except Exception as e:
        print('155')
        print(e)
    
    
        

def dashboard(ddict,browser,username):
    global tokenfinal
    time.sleep(5)
    dash = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[5]/a').click()
    time.sleep(2)
    active_memeber = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[5]/ul/li[2]/a').click()
    time.sleep(2)
    print("UAN-",ddict['UAN'])
    try:
        uan = int(ddict['UAN'])
    except:
        uan = ''
    
    if(uan): # if uan present 
        uan_v = browser.find_element_by_id('uan').send_keys(uan)
        button = browser.find_elements_by_tag_name('button')
        for sr in button:
            if(sr.get_attribute('type') == 'submit'):
                btn = sr.click()
                break


    else: # uan is not present
        name_a = browser.find_element_by_id('name').send_keys(ddict['Name'])
        button = browser.find_elements_by_tag_name('button')
        for sr in button:
            if(sr.get_attribute('type') == 'submit'):
                btn = sr.click()
                break
    time.sleep(2)
    saveLocation = "./Images_epfo/Yes"+str(ddict['Name'])+".png"
    browser.save_screenshot(saveLocation)
    member= browser.find_element_by_id('gview_activeMembers')
    time.sleep(2)
    member2 = member.find_elements_by_tag_name('div')
    list_table = []
    list_total_no=[]

    for d in member2:
        if(d.get_attribute('class') == "ui-state-default ui-jqgrid-hdiv ui-corner-top"):
            th_tag = d.find_elements_by_tag_name('th')
            for t in th_tag:
                list_table.append(t.get_attribute('id'))
        if(d.get_attribute('class') == 'ui-jqgrid-bdiv'):
            tr_tag = d.find_elements_by_tag_name('tr')
            for t in tr_tag:
                tr_prs = t.get_attribute('id')
                dict_td={}
                try:
                    td_find = t.find_elements_by_tag_name('td')
                    for t_d in range(0,len(td_find)):
                        dict_td[list_table[t_d]] = td_find[t_d].get_attribute('title')
                    list_total_no.append(dict_td)
                except:
                    print("")
    del list_total_no[0]   
    # compare dict values to find match
    time.sleep(2)
    find_UAN = ''
    Find_member_id = ''
    member_name= ddict['Name']
    for l_tot in range(0,len(list_total_no)):
        dict_t = list_total_no[l_tot]
        #name = ddict['Title'] +' '+ ddict['Name'] # change name according to table
        t_name = dict_t['activeMembers_name']
        t_name =t_name.replace("Mr. ","")
        t_name =t_name.replace("Mrs. ","")
        t_name =t_name.replace("Ms. ","")
        name = ddict['Name']
        if(name.strip() == t_name.strip()):
            # change date according to table info
            try:
                dob=ddict['DOB'].split('/')
            except:
                dob=ddict['DOB'].split('-')
            d=dob[0]
            m=dob[1]
            y=dob[2]
            if(len(d)==1 or len(m)==1):
                if(int(d)<10):
                    d='0'+d
                if(int(m)<10):
                    m='0'+m
                    dob=d+'/'+m+'/'+y
            else:
                dob=d+'/'+m+'/'+y
            print("Date of Birth",dob)
            dt_obj = datetime.strptime(dob,'%d/%m/%Y')
            dt_str = datetime.strftime(dt_obj,"%d-%b-%Y")
            dt_str = dt_str.upper()
            if(dt_str == dict_t['activeMembers_dob']):
                #if(ddict['Father Husband Name'].strip() == dict_t['activeMembers_fatherOrHusbandName'].strip()):
                #if(ddict['Relation'] == dict_t['activeMembers_relation']):
                #if(ddict['Mobile'] == dict_t['activeMembers_mobile']):
                member_name = dict_t['activeMembers_name']
                find_UAN = dict_t['activeMembers_uan']
                Find_member_id = dict_t['activeMembers_memberId']
        else:
            print("name not found in table")
    list_member =[]
    dict_member={ "UAN":find_UAN ,"Name":member_name, "MEMBER ID":Find_member_id}
    list_member.append(dict_member)
    row = [find_UAN ,member_name , Find_member_id ]
    # if uan have value then send this else that
    if find_UAN:
        member_id=str(Find_member_id)
        uan_no=str(find_UAN)
        emp_id =str(ddict["Id"])
        datauan = {"emp_id":emp_id,"emp_member_id":member_id,"emp_uan_no":uan_no} 
        headers = {'Authorization': tokenfinal}
        url="http://52.15.230.9/api/Employee/update_employee_epfo"
        response = requests.post(url, data=datauan, headers=headers)
        a=json.loads(response.text)
        print(" RESPONSE FOR update_employee",a)
        myprint(str(ddict["Id"]),"Member "+ str(member_name)+ " found UAN = "+ str(find_UAN)+", member_id = "+str(Find_member_id))
    else:
        myprint(str(ddict["Id"])," Not found UAN and member_id for Member "+ str(member_name))
    
def accept_alert(ddict,browser):
    time.sleep(3)
    print("inside alert accept")
    #browser.switch_to.alert.accept()
    WebDriverWait(browser,40).until(cond.alert_is_present())
    obj = browser.switch_to.alert
    msg=obj.text
    print ("Alert shows following message: "+ msg )
    time.sleep(3)
    myprint(str(ddict["Id"]),"Alert shows following message: "+str(msg))
    obj.accept()
    time.sleep(4)
    
def alert_found(ddict,browser , username):
    global tokenfinal
    time.sleep(5)
    alert_text=''
    tags= browser.find_elements_by_tag_name('div')
    alert_message=''
    time.sleep(3)
    for i in tags:
        if(i.get_attribute('role')== 'alert'):
            alert_message = i.text
            myprint(str(ddict["Id"]),str(alert_message))
            alert_text=str(alert_message)
        elif(i.get_attribute('class')=='alert alert-danger'):
            alert_message = i.text
            myprint(str(ddict["Id"]),str(alert_message))
            print(alert_message)
            alert_text=str(alert_message)
        else:
            pass
            
    time.sleep(3)
    alert_message = alert_message.strip()
    myprint(str(ddict["Id"]),"Alert for"+ str(ddict["Name"]) + " ** "+ str(alert_message))
    alert_text=str(alert_message)
    try:
        if(alert_message == 'Member details matched'):
            saveLocation = "./Images_epfo/Alert"+str(username)+".png"
            browser.save_screenshot(saveLocation)
            btn = browser.find_elements_by_tag_name('button')
            for b in btn:
                if(b.text == 'Ok'):
                    print("click ok")
                    b.click()
                    break
            time.sleep(15)
            print("wages",ddict['Wages'])
            if(ddict['Wages']):
                wage = browser.find_element_by_id('wages').send_keys(int(ddict['Wages']))
            doj=ddict['Date of joining'].split('/')
            print(doj)
            d=doj[0]
            m=doj[1]
            y=doj[2]
            if(len(d)==1 or len(m)==1):
                if(int(d)<10):
                    d='0'+d
                if(int(m)<10):
                    m='0'+m
                    doj=d+'/'+m+'/'+y
            else:
                doj=d+'/'+m+'/'+y
            print("date of Birth",doj)
            myprint(str(ddict["Id"])," Save successfully")
            d_join = browser.find_element_by_id('doj').send_keys(doj)
            print("after date of join")
            wag = browser.find_element_by_id('wages').click()
            time.sleep(2)
            print("after wages")
            element = browser.find_element_by_name('save').click()
            time.sleep(10)
            
            try:
                accept_alert(browser)
                time.sleep(2)
                try:
                    accept_alert(ddict,browser)
                except:
                    accept_alert(ddict,browser)
            except:
                timeout = 60
                element_present = EC.presence_of_element_located((By.ID, 'memberName'))
                WebDriverWait(browser, timeout).until(element_present)
                print(" alert accet exception")
        elif(alert_message == 'Member AADHAAR mismatch.'):
            time.sleep(3)
            saveLocation = "./Images_epfo/Alert"+str(username)+".png"
            browser.save_screenshot(saveLocation)
            btn = browser.find_elements_by_tag_name('button')
            for b in btn:
                if(b.text == 'Close'):
                    b.click()
                    break
                                
        elif(alert_message == 'UAN details not found.'):
            saveLocation = "./Images_epfo/Alert"+str(username)+".png"
            browser.save_screenshot(saveLocation)
            time.sleep(3)
            btn = browser.find_elements_by_tag_name('button')
            for b in btn:
                if(b.text == 'Close'):
                    b.click()
                    break
            try:
                time.sleep(10)
                drop = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a')
                drop.click()
                time.sleep(2)
                rgstr_in = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[2]/a')
                rgstr_in.click()
                uan_no=''
                print("Register individual going ")
                register_individual(ddict,browser , username,uan_no)
            except:
                time.sleep(10)
                drop = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a')
                drop.click()
                time.sleep(2)
                rgstr_in = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[2]/a')
                rgstr_in.click()
                uan_no=''
                print("Register individual going ")
                register_individual(ddict,browser , username,uan_no)
                
            
            
        elif(alert_message == 'Member DOB mismatch.'):
            saveLocation = "./Images_epfo/Alert"+str(username)+".png"
            browser.save_screenshot(saveLocation)
            time.sleep(3)
            btn = browser.find_elements_by_tag_name('button')
            for b in btn:
                if(b.text == 'Close'):
                    b.click()
                    break
            
        else:
            try:
                saveLocation = "./Images_epfo/Alert"+str(username)+".png"
                browser.save_screenshot(saveLocation)
                btn = browser.find_elements_by_tag_name('button')
                for b in btn:
                    if(b.text == 'Close'):
                        b.click()
                        break
            except:
                btn = browser.find_elements_by_tag_name('button')
                for b in btn:
                    if(b.text == 'Ok'):
                        print("click ok")
                        b.click()
                        break
    except:
        
        btn = browser.find_elements_by_tag_name('button')
        saveLocation = "./Images_epfo/Alert"+str(username)+".png"
        browser.save_screenshot(saveLocation)
        for b in btn:
            if(b.text == 'Ok'):
                print("click ok")
                b.click()
                break
            if(b.text == 'Close'):
                b.click()
                break
        #browser.switch_to.alert.accept()
        obj = browser.switch_to.alert
        msg=obj.text
        print ("Alert shows following message: "+ msg )
        time.sleep(3)
        myprint(str(ddict["Id"]),"Alert shows following message: "+str(msg))
        obj.accept()
        alert_text=str(msg)
        time.sleep(3)
        timeout = 120
        element_present = EC.presence_of_element_located((By.ID, 'memberName'))
        WebDriverWait(browser, timeout).until(element_present)
    try:
        emp_id= str(ddict["Id"])
        dataep = {"emp_id":emp_id,"reason":alert_text} 
        headers = {'Authorization': tokenfinal}
        url="http://52.15.230.9/api/Employee/error_employee_epfo"
        response = requests.post(url, data=dataep, headers=headers)
        a=json.loads(response.text)
        print(a)
    except:
        print(" error in error_employee_epfo al.ert")
    
                

def register_individual(ddict,browser , username,uan_no):
    # name
    time.sleep(5)
    prev_emp = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/form/div[2]/div[2]/div[1]')
    prevno = prev_emp.find_elements_by_class_name('data-label')
    if(uan_no):
        myprint(str(ddict["Id"]),str(username)+" Select Yes- user is  a previous employee")
        radio_button = prevno[1].find_element_by_id('previousEmployementYes')  
        radio_button.click()
        time.sleep(10)
        print("check value uan ",type(ddict['UAN']))
        una_val = browser.find_element_by_id('uan').send_keys(ddict['UAN'])
        time.sleep(3)
        aadhaar = browser.find_element_by_id('aadharVerify').send_keys(ddict['Aadhaar Number'])
        #mamber = browser.find_element_by_id('isNorthEastMember')
        saveLocation = "./Images_epfo/Yes"+str(username)+".png"
        browser.save_screenshot(saveLocation)
        #driver.execute_script("arguments[0].setAttribute('class','vote-link up voted')", mamber)
        name = browser.find_element_by_xpath('//*[@id="nameVerify"]').send_keys(ddict['Name'])
        try:
            dob=ddict['DOB'].split('/')
        except:
            dob=ddict['DOB'].split('-')
        d=dob[0]
        m=dob[1]
        y=dob[2]
        if(len(d)==1 or len(m)==1):
            if(int(d)<10):
                d='0'+d
            if(int(m)<10):
                m='0'+m
                dob=d+'/'+m+'/'+y
        else:
            dob=d+'/'+m+'/'+y
        print("date of birth",dob)
        date = browser.find_element_by_xpath('//*[@id="dobVerify"]').send_keys(dob)
        time.sleep(3)
        button = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/form/div[2]/div[2]/div[2]/div[2]/div[1]/input[1]').click()
        time.sleep(12)
        try:
            alert_found(ddict , browser ,username)
        except Exception as e:
            time.sleep(12)
    else:
        myprint(str(ddict["Id"]),str(username)+" Select No- user not  a previous employee")
        radio_button = prevno[0].find_element_by_id('previousEmployementNo')  
        #radio_button.click() 
        time.sleep(5)
        saveLocation = "./Images_epfo/No"+str(username)+".png"
        browser.save_screenshot(saveLocation)
        register_individual_no(ddict, browser) # functon call when select no
        print('done now')

def database(username,pwd):
    global tokenfinal
    data = {'email':'super.admin@workz.in','password':'Admin@Workz19'} 
    response = requests.post('http://52.15.230.9/api/Authentication/Login', data) 
    login = json.loads(response.text)
    token = login["Token"]
    tokenfinal = token
    # epfo api call
    dataesic = {"username":str(username),"password":str(pwd)} 
    headers = {'Authorization': token}
    url="http://52.15.230.9/api/Employee/DataForEPFO"
    response = requests.post(url, data=dataesic, headers=headers)
    a=json.loads(response.text)
    # response result key
    try:   
        datastore = a["Result"]
        lent=len(datastore)
        for i in range(0,lent):
            try:
                excel_date=int(datastore[i]["DOB"])
                dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date - 2)
                dt1=dt.strftime('%d-%m-%Y')
                datastore[i]["DOB"]=dt1
            except:
                pass
            try:
                excel_date_j=int(datastore[i]["Date of joining"])
                dtt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date_j - 2)
                dt2=dtt.strftime('%d-%m-%Y')
                datastore[i]["Date of joining"]=dt2
            except Exception as e:
                pass
    except:
        datastore=[]
        pass
    return datastore

def approvals(browser,username):
    drop = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a')
    drop.click()
    #time.sleep(5)
    approve_in = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[6]/a')
    approve_in.click()
    time.sleep(5)
    saveLocation = "./Images_epfo/approves.png"
    browser.save_screenshot(saveLocation)
    
    try:
        a=browser.find_element_by_id("viewMemActivity")
        tr_tag = a.find_elements_by_tag_name("tr")
        for tr in tr_tag:
            print(tr)
            if(tr.get_attribute('tabindex') == '-1'):
                tdtag = tr.find_elements_by_tag_name('td')
                if(tdtag[1].get_attribute("aria-describedby") == "viewMemActivity_type"):
                    print(tdtag[1].text)
                    if(tdtag[1].text.strip() == "Individual Registration"):
                        inputt = tr.find_elements_by_tag_name('input')
                        for inn in inputt:
                            inn.get_attribute('value').strip()
                            if(inn.get_attribute('value').strip() == 'Approve' ):
                                print("clicking clicking approve",inn)
                                inn.click()
                                time.sleep(2)
                                myprint(str(username)," Successfully click in Approve Button")
                                browser.switch_to.alert.accept()
    except:
        err = browser.find_element_by_id("divPendingRecords")
        err2 = err.find_element_by_class_name("panel-body")
        err_text = err2.text
        err_text = err_text.lstrip()
        print("Approve Error",err_text)
        myprint(str(username),"Approve Error  **  "+str(err_text))
                            




def drop_register_individual(browser ,username,pwd ):
    try:
        ddict = database(username,pwd) # call data in epfo file in json format
    except Exception as e:
        print("Exception in database",e)
    saveLocation = "./Images_epfo/loginsuccess.png"
    browser.save_screenshot(saveLocation)
    # main page member dropdown select register-individual
    myprint(str(username),str(username)+" Login is successful")
    for l_k in range(0,len(ddict)):
        print("waiting..............")
        time.sleep(4)
        try:
            drop = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a')
            drop.click()
            #men_menu.click()
            print(str(ddict[l_k]['Name'])+" Click on MEMBER drop down")
            saveLocation = "./Images_epfo/registerindiv.png"
            browser.save_screenshot(saveLocation)
            time.sleep(2)
            rgstr_in = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[2]/a')
            rgstr_in.click()
            print(str(ddict[l_k]['Name'])+" then select REGISTER_INDIVIDUAL")
            time.sleep(2)
            dict_s = ddict[l_k]
            empname= ddict[l_k]['Name']
            uan_no = dict_s['UAN']
            print("Register individual going ")
            register_individual(dict_s,browser , empname,uan_no) # user select no or yes
            login=True
            
        except Exception as e:
            login=False
            time.sleep(4)
            print('390',e)
            url=browser.current_url
            browser.get(url)
            pass
            
    print('waiting now')
    time.sleep(2)
    try:
        print('in approvals page going')
        approvals(browser ,username)
    except Exception as e:
        print(e)
    time.sleep(2)
    print("dashboard")
    for l_k in range(0,len(ddict)):
        try:
            dict_s=ddict[l_k]
            dashboard(dict_s,browser,username)
        except Exception as e:
            url=driver.current_url
            driver.get(url)
            print(e)






def epfo_stop(browser):
    time.sleep(2)
    saveLocation = "./Images_epfo/stopimage.png"
    browser.save_screenshot(saveLocation)
    browser.find_element_by_xpath("/html/body/header/nav/div/div[3]/div[2]/span/a").click()
    time.sleep(2)
    browser.quit()


def driver_epfo():
    global dict_drivers
    print("")
    return dict_drivers

def login(browser,cred_user):
    user_n = cred_user["username"]
    pwd = cred_user["password"]
    user = browser.find_element_by_id("username")
    passwd = browser.find_element_by_id("password")
    try:
        user.send_keys(Keys.CONTROL + "a")
        user.send_keys(Keys.DELETE)

        passwd.send_keys(Keys.CONTROL + "a")
        passwd.send_keys(Keys.DELETE)
    except:
        pass
    # username
    user = browser.find_element_by_id("username")
    passwd = browser.find_element_by_id("password")
    time.sleep(1)
    #user.send_keys("bvgindia34784")
    #passwd.send_keys("Bngbvgkar@34784*")
    user.send_keys(user_n)
    print("Pass username "+str(user_n)+" into text field")
    time.sleep(2)
    passwd.send_keys(pwd)
    print("Pass password into text field")
    time.sleep(2)
    saveLocation = "./Images_epfo/login.png"
    browser.save_screenshot(saveLocation)
    signup = browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[2]/form/div[4]/div[1]/button").click()
    time.sleep(6)
    print(str(user_n)+" Click SignUp Button")
    
    try:
        drop = browser.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a')
        try:
            drop_register_individual(browser,user_n,pwd)
        except:
            print("5677 drop_register_individual")
        try:
            epfo_stop(browser)
        except Exception as e:
            print('492')
            browser.quit()
            print(e)
            print("epfo stop is called")
    except:
        empid=str(user_n)
        myprint(empid,"Login unsuccessful for "+str(user_n))
        saveLocation = "./Images_epfo/loginagain.png"
        browser.save_screenshot(saveLocation)
        #login(browser,cred_user)



def epfo_login(cred_user):
    print("cred_user----",cred_user)
    global dict_drivers
    time_start= datetime.now()
    user_n = cred_user["username"]
    pwd = cred_user["password"]
    options = FirefoxOptions()
    options.add_argument("--headless")
    browser = webdriver.Firefox(executable_path='./geckodriver' ,firefox_options=options)
    print("Firefox Browser started")
    browser.get('https://unifiedportal-emp.epfindia.gov.in/epfo/')
    driver_name = str("driver")+str(user_n)
    print("driver name-------------------******",driver_name)
    dict_drivers[driver_name]=browser
    saveLocation = "./Images_epfo/epfoportal.png"
    browser.save_screenshot(saveLocation)
    browser.maximize_window()
    print("Open EPFO website into browser")
    login(browser,cred_user)

    


