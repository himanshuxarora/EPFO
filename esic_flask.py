from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import requests
#from captchafind import mainpage
from captchafind_path import mainpage # test in windows
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from PyPDF2 import PdfFileMerger
import sys,os 
from datetime import datetime
import json
import openpyxl
import csv
from excel2json import convert_from_file
global banklogin
import json
import requests
import boto3
import random

global dict_drivers,dict_company,tokenfinal
dict_drivers={}
dict_company={}
tokenfinal=""

def myprint(emp_id,status):
    global tokenfinal
    dataesic = {"emp_id":emp_id,"log_text":status} 
    headers = {'Authorization': tokenfinal}
    url="http://52.15.230.9/api/Employee/addlogesi"
    response = requests.post(url, data=dataesic, headers=headers)
    a=json.loads(response.text)

    
def bucket_upload(emp_id ,comp_name,pdf_name ):
    global tokenfinal
    print("inside bucket upload")
    ACCESS_ID="AKIAJ3VLARDR5HBZ6ZSA"
    ACCESS_KEY="jBav0NCBFnRjzg3Td6WeR+yb6sUJ5kiLz3ccRCeR"
    s3 = boto3.resource('s3',aws_access_key_id=ACCESS_ID,aws_secret_access_key= ACCESS_KEY)
    print(" company"+str(comp_name)+', emp'+str(emp_id)+' pdf_name'+str(pdf_name))
    s3.Object('workzdata', 'company/'+str(comp_name)+'/employee/'+str(emp_id)+'/'+str(pdf_name)+'.pdf').upload_file('./Output_esic/'+str(pdf_name)+'.pdf')
    myprint(str(emp_id),"Add pdf into Bucket")
    url="https://workzdata.s3.amazonaws.com/company/"+str(comp_name)+"/employee/"+ str(emp_id)+"/"+ str(pdf_name)+".pdf"
    print(url)
    dataesic = {"emp_id":emp_id,"esi_no":pdf_name,"tic_letter":url} 
    headers = {'Authorization': tokenfinal}
    url="http://52.15.230.9/api/Employee/update_employee_esi"
    response = requests.post(url, data=dataesic, headers=headers)
    a=json.loads(response.text)
    time.sleep(4)

def esic_sheet(username,pwd):
    global tokenfinal,dict_company
    try:
        data = {'email':'super.admin@workz.in','password':'Admin@Workz19'} 
        response = requests.post('http://52.15.230.9/api/Authentication/Login', data) 
        login = json.loads(response.text)
        token = login["Token"]
        tokenfinal= token
        company_id=login["Result"]["company_id"]
        dict_company[username]=company_id
        # epfo api call
        dataesic = {"username":username,"password":pwd}
        headers = {'Authorization': token}
        url="http://52.15.230.9/api/Employee/DataForESI"
        response = requests.post(url, data=dataesic, headers=headers)
        a=json.loads(response.text)
    except Exception as e:
        myprint(str(username),str(e))
    # response result key
    try:
        datastore = a["Result"]
    except:
        datastore=[]
        myprint(str(username),"Data is empty")
        pass

    return datastore

def CompInitial(error):
    initial = 'Message: [Exception... "Component not initialized"  nsresult: "0xc1f30001 (NS_ERROR_NOT_INITIALIZED)"  location: "JS frame :: chrome://marionette/content/modal.js :: get window :: line 199"  data: no]'
    if(error==initial):
        print(" error in component Component not initialized it will Raise exception")
        raise Exception(error)
def found_date(driver ,tag, tag_name ,date_data):
    #send_day = "12-03-2009" # day-month-year
    try:
        s_list = date_data.split('-')
    except:
        s_list = date_data.split('/')
    print("ADd date--",date_data)
    try:
        dy_format = datetime.strptime(date_data,'%d-%m-%Y')
    except:
        dy_format = datetime.strptime(date_data,'%m-%d-%Y')
    try:
        time.sleep(2)
        a=driver.find_element_by_id(str(tag)).click()
        print("tag:",tag,"tag_name:",tag_name,"date_data:",date_data)
        for i in range(0,5):
            to_day = datetime.now()
            cal_today = to_day.strftime('%d-%m-%Y')
            cal_list = cal_today.split('-')
            match = []
            year_text = dy_format.strftime('%Y')
            first = driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_title").click()
            time.sleep(2)
            second = driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_title").click()
            time.sleep(2)
            for j in range(0,25):
                try:
                    year_series= driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_title").text
                    y_series = year_series.split("-")
                    if( y_series[0] <= year_text  and y_series[1]>= year_text ):
                        # between 2000-2010
                        year_find = driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_yearsBody")
                        tr_year =  year_find.find_elements_by_tag_name("tr")
                        fnd=False
                        for tr_y in range(0,len(tr_year)):
                            td_year = tr_year[tr_y].find_elements_by_tag_name("td")
                            for td_y in range(0,len(td_year)):
                                div_year = td_year[td_y].find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_year_"+str(tr_y)+"_"+str(td_y))
                                if(year_text == div_year.text):
                                    div_year.click()
                                    time.sleep(2)
                                    match.append(div_year.text)
                                    break
                    else:
                        prev = driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_prevArrow").click()
                        time.sleep(2)
                except Exception as e:
                    print('here man')
                    print(e)
                    break
                
            time.sleep(2)
            month_text = dy_format.strftime('%b')
            time.sleep(1)

            mont = driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_monthsBody")
            tr_tag = mont.find_elements_by_tag_name("tr")
            for t_tr in range(0,len(tr_tag)):
                td_tag = tr_tag[t_tr].find_elements_by_tag_name("td")
                for t_td in range(0, len(td_tag)):# month names
                    div_month = td_tag[t_td].find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_month_"+str(t_tr)+"_"+str(t_td))
                    #print("month div test found",div_month.text)
                    if(month_text == div_month.text):
                        #print("tr count=",t_tr,"== Td count",t_td)
                        #print(" month_text",month_text,"== div_month",div_month.text)
                        div_month.click()
                        time.sleep(2)
                        match.append(s_list[1])
                        break
            
            time.sleep(2)
            day_text = dy_format.strftime('%d')
            print(day_text)

            tbdy = driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_daysBody")
            tr_tbdy =tbdy.find_elements_by_tag_name("tr")
            for t_r in range(0,len(tr_tbdy)):
                td_tbdy =tr_tbdy[t_r].find_elements_by_tag_name("td")
                for t_d in range(0,len(td_tbdy)):
                    if(td_tbdy[t_d].get_attribute("class")):
                        pass
                    else:
                        div_day =  td_tbdy[t_d].find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_day_"+str(t_r)+"_"+str(t_d))
                        day_a=div_day.text
                        if(len(day_a)==1):
                            day_a = "0"+str(day_a)
                        if(day_text == day_a):
                            div_day.click()
                            match.append(day_a)
                            break

            try:
                time.sleep(2)
                driver.find_element_by_id("ctl00_HomePageContent_btnAgree").click()
                time.sleep(3)
            except:
                print(" not found agree popup")
                pass
            break
    except Exception as e:
        print(" Exception in add date ",e)
        initial = 'Message: [Exception... "Component not initialized"  nsresult: "0xc1f30001 (NS_ERROR_NOT_INITIALIZED)"  location: "JS frame :: chrome://marionette/content/modal.js :: get window :: line 199"  data: no]'
        if(e==initial):
            print(" error in component Component not initialized it will Raise exception")
            raise Exception(e)
# ******************** Register function for npominee or three ******************
def Insured_Person(driver , esicdata):
    global tokenfinal
    time.sleep(5)
    e_error=''
    print("Clicking on insured person details")
    Insured = driver.find_element_by_id("Tr12")
    str3=driver.title
    list_add_in = esicdata["Insured person details"]
    print("Fetched ip_person")
    reg_window = driver.window_handles[1]
    time.sleep(6)
    name_p=esicdata["Insurance Person Name"]
    Insured_td = Insured.find_element_by_class_name("lastFormValue")
    Insured_td.find_element_by_tag_name('a').click()
    time.sleep(3)
    insured_window = driver.window_handles[2]
    driver.switch_to.window(insured_window)
    time.sleep(5)
    count = 1
    for i_l in list_add_in:
        print("count in insured person",count)
        count=count+1
        try:
            nametxt=driver.find_element_by_id("ctl00_HomePageContent_txtName")
            nametxt.send_keys(Keys.CONTROL + "a")
            nametxt.send_keys(Keys.DELETE)
        except Exception as e:
            e_error=''
            pass
        driver.find_element_by_id("ctl00_HomePageContent_txtName").send_keys(i_l['Person Name'])
        time.sleep(2)
        date_data = i_l["DOB"]
        div_id_tag ="ctl00_HomePageContent_CtrlDOB"
        div_id_name ="cEDOA"
        time.sleep(4)
        try:
            found_date(driver  ,div_id_tag, div_id_name ,date_data)
        except Exception as e:
            e_error=''
            try:
                time.sleep(10)
                found_date(driver  ,div_id_tag, div_id_name ,date_data)
            except Exception as e:
                e_error=''
                pass

        time.sleep(4)
        relationship = Select(driver.find_element_by_id('ctl00_HomePageContent_CtrlRelation'))
        rtext = i_l["Relation"]
        
        for nsr in relationship.options:
            gntext = nsr.text
            if(gntext.upper().strip() == rtext.upper().strip()):
                x = nsr.click()
                break
        try:
            rttext = i_l["Gender"]
            time.sleep(5)
            gender = Select(driver.find_element_by_id("ctl00_HomePageContent_CtrlTrans"))
            for nr in gender.options:
                nstt= nr.text
                if(nstt.upper() == rttext.upper()):
                    sx = nr.click()
                    break
                time.sleep(2)
            time.sleep(4)
            driver.find_element_by_id("ctl00_HomePageContent_dec_chkbox").click()
        except Exception as e:
            e_error=''
            pass
        checkstate=False
        try:
            res_val = i_l["Whether Residing with"]
            print(" Whether Residing with",res_val)
            if(res_val.upper() =="YES"):
                driver.find_element_by_id('ctl00_HomePageContent_ctrlRDIpDisable_0').click()
            else:
                checkstate=True
                driver.find_element_by_id('ctl00_HomePageContent_ctrlRDIpDisable_1').click()
        except Exception as e:
            e_error=''
            pass
        try:                        
            saveLocation = "./Images_esic/Insured-1"+str(name_p)+".png"
            driver.save_screenshot(saveLocation)
        except:
            pass
        if(checkstate==True):
            try:
                time.sleep(4)
                statedata = Select(driver.find_element_by_id('ctl00_HomePageContent_ctrlTextPermanentState'))
                stext = i_l["State"]
                stext=stext.strip()
                print("Entering Insured person State",stext)
                if(stext):
                    for nsd in statedata.options:
                        nsdtext = nsd.text
                        if(nsdtext.upper().strip() == stext.upper()):
                            x = nsd.click()
                            break
                time.sleep(4)
                
                distictdata = Select(driver.find_element_by_id('ctl00_HomePageContent_ctrlTextPermanentDistrict'))
                d_text = i_l["District"]
                print("Entering Insured person State",d_text)
                if(d_text):
                    for nsd in distictdata.options:
                        nm=nsd.text
                        if(nm.upper().strip() == d_text.upper().strip()):
                            x = nsd.click()
                            break
            except Exception as e:
                e_error=''
                pass
        else:
            pass
        time.sleep(4)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlButtonSave").click()
        error_txt=""
        try:
            time.sleep(5)
            span_tag = driver.find_elements_by_class_name("errordisplay")
            for sp in span_tag:
                if(sp.get_attribute("style") == "color: red; display: inline;"):
                    print( "Error insured person",sp.text)
                    error_txt=sp.text
                    myprint(str(esicdata["Id"]), str(i_l["ID"])+" Error:- "+ sp.text)
                elif(sp.get_attribute("style") == "color: red; visibility: visible;"):
                    print( "Error insured person",sp.text)
                    error_txt=sp.text
                    myprint(str(esicdata["Id"]), str(i_l["ID"])+" Error:- "+ sp.text)
        except:
            pass

        try:
            time.sleep(4)
            save_tag = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelSaved") 
            if( save_tag.text == "Details are saved successfully"):
                print("Saved data successfully ",save_tag.text)
                sv= save_tag.text
                myprint(str(esicdata["Id"]),str(driver.title)+" :-"+str(sv))  
            time.sleep(2)
        except:
            print("error insured person")
            time.sleep(2)
            pass
        try:
            time.sleep(4)
            save_tag = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelSaved") 
            if(save_tag.get_attribute("style")=="color:Red;font-weight:bold;"):
                print("error in insured details ",save_tag.text)
                sv= save_tag.text
                error_txt=save_tag.text
                myprint(str(esicdata["Id"]),str(driver.title)+" :-"+ str(sv))
            time.sleep(2)
        except:
            print("error insured person")
        try:                        
            saveLocation = "./Images_esic/Insured-submit"+str(name_p)+".png"
            driver.save_screenshot(saveLocation)
            if(error_txt):
                emp_id= str(esicdata["Id"])
                dataes = {"emp_id":emp_id,"reason":str(error_txt)} 
                headers = {'Authorization': tokenfinal}
                url="http://52.15.230.9/api/Employee/error_employee_esi"
                response = requests.post(url, data=dataes, headers=headers)
                a=json.loads(response.text)
                print(a)
            else:
                pass
        except:
            pass
    if(e_error):
        print("call exception ")
        CompInitial(e_error)
        
def Details_of_Nominee(driver,detail):
    global tokenfinal
    time.sleep(3)
    e_error=""
    print("Clicking on enetre nominee details")
    detail_nomini = driver.find_element_by_id("Tr11")
    reg_window = driver.window_handles[1]
    detail_td = detail_nomini.find_element_by_class_name("lastFormValue")
    detail_td.find_element_by_tag_name('a').click()
    time.sleep(3)
    name_p=detail["Insurance Person Name"]
    nominee_window = driver.window_handles[2]
    time.sleep(5)
    driver.switch_to.window(nominee_window)
    time.sleep(5)
    print("Entering username",detail["Nominee Name"])
    try:
        mm = detail["Nominee Name"].strip()
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextUserName").send_keys(mm)
        time.sleep(4)
        print("Selecting relation")
        relationn = Select(driver.find_element_by_id('ctl00_HomePageContent_RelationShipWithIp'))
        r_text =  detail["Relationship with IP"]
        r_text=r_text.strip()
        for nsd in relationn.options:
            nsdtext = nsd.text
            nsdtext=nsdtext.strip()
            if(nsdtext.upper() == r_text.upper()):
                x = nsd.click()
        time.sleep(3)
        print("Entering nominee addresses")
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextAddress1").send_keys(detail["Nominee Address 1"])
        time.sleep(2)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextAddress2").send_keys(detail["Nominee Address 2"])
        time.sleep(4)
        state = Select(driver.find_element_by_id('ctl00_HomePageContent_States'))
        stext = detail["Nominee State"]
        stext=stext.strip()
        print("Entering nominee state:",stext)
        for nsd in state.options:
            nsxt = nsd.text
            if(nsxt.upper() == stext.upper()):
                x = nsd.click()
        time.sleep(3)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextAddress3").send_keys(detail["Nominee Address 3"])
        time.sleep(8)
        
        distictdata = Select(driver.find_element_by_id('ctl00_HomePageContent_Districts'))
        d_text = detail["Nominee District"]
        d_text=d_text.strip()
        print("Entering nominee Dist",d_text)
        for nsd in distictdata.options:
            nsdext = nsd.text
            nsdext=nsdext.strip()
            if(nsdext.upper() == d_text.upper()):
                print("ENTER DISTYRICT IN Nominee")
                x = nsd.click()
        time.sleep(4)
        try:
            print("Entering pincode of nominee",detail["Nominee PinCode"])
            driver.find_element_by_id('ctl00_HomePageContent_ctrlTextPin').send_keys(detail["Nominee PinCode"])
        except:
            pass
        try:
            print("Entering mobile number of nominee",detail["Nominee Mobile Number"])
            driver.find_element_by_id('ctl00_HomePageContent_ctrlTextMobileNumber').send_keys(detail["Nominee Mobile Number"])
        except:
            pass
        non_val = detail["Is Nominee a Family Member"]
        non_dict = {0:'Yes' , 1:'No' }
        print("Selecting whether nominee a family member")
        time.sleep(4)
        for key in non_dict:
            if(non_dict[key] == non_val):
                pre =driver.find_element_by_id('ctl00_HomePageContent_rbtnlistNomneeAkaFamily_'+str(key))
                pre.click()
        time.sleep(3)
        try:
            for nsd in distict.options:
                nsdext = nsd.text
                nsdext=nsdext.strip()
                if(nsdext.upper() == d_text.upper()):
                    x = nsd.click()
        except:
            pass
        try:
            saveLocation = "./Images_esic/Nominee-1"+str(name_p)+".png"
            driver.save_screenshot(saveLocation)
        except:
            pass
    except Exception as e:
        e_error=''
        pass
    time.sleep(3)
    driver.find_element_by_id("ctl00_HomePageContent_Save").click()
    time.sleep(3)
    error_txt=''
    print("Save button clicked")
    try:
        span_tag = driver.find_elements_by_class_name("errordisplay")
        if(span_tag):
            for sp in span_tag:
                if(sp.get_attribute("style") == "color: red; display: inline;"):
                    print( "Error in nominee details",sp.text)
                    error_txt=sp.text
                    myprint(str(detail["Id"]), str(driver.title)+" :-"+ str(sp.text))
                elif(sp.get_attribute("style") == "color: red; visibility: visible;"):
                    print( "Error in nominee details",sp.text)
                    error_txt=sp.text
                    myprint(str(detail["Id"]), str(driver.title)+" :-"+ str(sp.text))
                

        save_tag = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelSaved") 
        if(save_tag):
            if( save_tag.text == "Data saved successfully"):
                print("Save data successfully ",save_tag.text)
                sv= save_tag.text
                myprint(str(detail["Id"]),str(driver.title)+" :-"+ str(sv))

    except:
        print("Error in detail of nominee")
        time.sleep(4)
    try:
        saveLocation = "./Images_esic/Nominee-submit"+str(name_p)+".png"
        driver.save_screenshot(saveLocation)
        if(error_txt):
            emp_id= str(detail["Id"])
            dataes = {"emp_id":emp_id,"reason":str(error_txt)} 
            headers = {'Authorization': tokenfinal}
            url="http://52.15.230.9/api/Employee/error_employee_esi"
            response = requests.post(url, data=dataes, headers=headers)
            a=json.loads(response.text)
            print(a)
        else:
            pass
    except:
        pass
    try:
        driver.close()
        driver.switch_to.window(reg_window)
        time.sleep(2)
    except:
        driver.close()
        driver.switch_to.window(reg_window)
        time.sleep(2)
    if(e_error):
        print("call exception ")
        CompInitial(e_error)
        
def bank_account(driver,esicdata):
    global banklogin,tokenfinal
    e_error=""
    try:
        name_p=esicdata["Insurance Person Name"]
        try:
            time.sleep(15)
            print("Clicking on bank details ")
            Bank = driver.find_element_by_id("Tr18")
            reg_window = driver.window_handles[1]
            Bank_td = Bank.find_element_by_class_name("lastFormValue")
            Bank_td.find_element_by_tag_name('a').click()
            time.sleep(4)
            bank_window = driver.window_handles[2]
            driver.switch_to.window(bank_window)
            time.sleep(5)
            count = 3 # row count
            banklogin=True
        except:
            banklogin=False
        if(banklogin==True):
            timeout = 120
            element_present = EC.presence_of_element_located((By.ID, "ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_CheckBox"))
            WebDriverWait(driver, timeout).until(element_present)
            time.sleep(4)
            driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_CheckBox").click()
            time.sleep(4)
            #account_no = driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_AccountNumber").send_keys(int(esicdata['Account Number']))
            time.sleep(4)

            saveLocation = "./Images_esic/Bank-1"+str(name_p)+".png"
            driver.save_screenshot(saveLocation)
            type_acc = Select(driver.find_element_by_id('ctl00_HomePageContent_gdvBankDetails_ctl0'+str(count)+'_TypeOfAccount'))
            type_text = esicdata["Account Type"]
            type_text=type_text.strip()
            time.sleep(4)
            for nsd in type_acc.options:
                sel = nsd.text
                sel=sel.strip()
                if(sel.upper() == type_text.upper()):
                    x = nsd.click()
            time.sleep(4)
            account_no = driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_AccountNumber")
            print("accttext",account_no.text)
            try:
                acc = str(account_no.text)
                if(acc!=""):
                    pass
                else:
                    driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_AccountNumber").send_keys(esicdata['Account Number'])
            except:
                pass
            time.sleep(4)
            driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_BankName").send_keys(esicdata['Bank Name'])
            time.sleep(4)
            driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_BranchName").send_keys(esicdata['Branch'])
            time.sleep(4)
            if(esicdata['MICR']):
                driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_MICRCode").send_keys(esicdata['MICR'])
            if(esicdata['IFSC']):
                driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_IFSCCode").send_keys(esicdata['IFSC'])
            time.sleep(2)
            driver.find_element_by_id("ctl00_HomePageContent_ctrlButtonSave").click()
            time.sleep(3)
            error_txt=''
            try:
                time.sleep(4)
                span_tag = driver.find_elements_by_class_name("errordisplay")
                for sp in span_tag:
                    if(sp.get_attribute("style") == "color: red; display: inline;"):
                        print( "Error in bank details",sp.text)
                        error_txt=sp.text
                        myprint(  str(esicdata["Id"]),str(driver.title)+" :-"+ str(sp.text))
                    elif(sp.get_attribute("style") == "color: red; visibility: visible;"):
                        print( "Error in bank details",sp.text)
                        error_txt=sp.text
                        myprint(  str(esicdata["Id"]),str(driver.title)+" :-"+ str(sp.text))
                    
            except:
                pass
            try:
                time.sleep(3)
                save_tag = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelSaved") 
                if( save_tag.text == "Details are saved successfully"):
                    print("save data successfully ",save_tag.text)
                    sv= save_tag.text
                    myprint(str(esicdata["Id"]),str(driver.title)+" :-"+str(sv))

            except:
                print("error detail of bank details")
                pass
            try:
                saveLocation = "./Images_esic/Bank-submit"+str(name_p)+".png"
                driver.save_screenshot(saveLocation)
                if(error_txt):
                    emp_id= str(esicdata["Id"])
                    dataes = {"emp_id":emp_id,"reason":str(error_txt)} 
                    headers = {'Authorization': tokenfinal}
                    url="http://52.15.230.9/api/Employee/error_employee_esi"
                    response = requests.post(url, data=dataes, headers=headers)
                    a=json.loads(response.text)
                    print(a)
                else:
                    pass
            except:
                pass
        else:
            pass
    except Exception as e:
        print("call exception ")
        CompInitial(e)
        
    
# ********************* Insert_part **************************
def insert_data(driver,esdata ,comp_name):
    global tokenfinal
    print("Inside insert_data")
    time.sleep(5)
    try:
        parent_window = driver.window_handles[0]
        print("Clicking on insert ip details")
        #driver.maximize_window()
        try:
            time.sleep(3)
            driver.find_element_by_id("lnkInsertIPDetails").click()
        except:
            time.sleep(8)
            driver.find_element_by_id("lnkInsertIPDetails").click()
        print("Handling window to window 1")
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        time.sleep(4)
        print("Clicking on insert")
        time.sleep(2)
        try:
            driver.find_element_by_id("ctl00_HomePageContent_ctrlInsert").click()
        except:
            time.sleep(8)
            driver.find_element_by_id("ctl00_HomePageContent_ctrlInsert").click()
        print("handling window")
        window_after2 = driver.window_handles[1]
        driver.switch_to.window(window_after2)
        time.sleep(7)
        #driver.maximize_window()
        print("Typing insurance number")
        driver.find_element_by_id("ctl00_HomePageContent_txtInsuranceNumber").send_keys(esdata["Insurance Number"])
        time.sleep(5)
        saveLocation = "./Images_esic/Insertpart-1"+str(esdata["Insurance Number"])+".png"
        driver.save_screenshot(saveLocation)
        print("Clicking on insurance name")
        driver.find_element_by_id("ctl00_HomePageContent_txtInsuranceName").click()  
        span = driver.find_element_by_id("ctl00_HomePageContent_lblWarning2")
        date_data = esdata["Date of Appointment"]
        tag="ctl00_HomePageContent_txtpdcfdcDate"
        tag_name ="calFromTxt"
        test = str(span.text)
        print("span text if error present",test)
        if(test):
            print("If error present:",span.text)
            if(span.get_attribute("style") == "color:Red;"):
                myprint( str(esdata["Id"]),str(driver.title)+" :-"+ str(span.text))
        else:
            print("No warning",span)
            date_data = esdata["Date of Appointment"]
            print("Date of apt",date_data)
            tag="ctl00_HomePageContent_txtpdcfdcDate"
            tag_name ="calFromTxt"
            try:
                found_date(driver ,tag, tag_name ,date_data)
            except:
                time.sleep(7)
                try:
                    found_date(driver ,tag, tag_name ,date_data)
                except:
                    pass
            time.sleep(4)

        time.sleep(3)
        try:
            driver.find_element_by_id('ctl00_HomePageContent_btnSubmit').click()
            saveLocation = "./Images_esic/Insertpart-2"+str(esdata["Insurance Number"])+".png"
            driver.save_screenshot(saveLocation)
        except:
            time.sleep(8)
            driver.find_element_by_id('ctl00_HomePageContent_btnSubmit').click()
            pass
        try:
            saveLocation = "./Images_esic/Insert-submit-1"+str(esdata["Insurance Number"])+".png"
            driver.save_screenshot(saveLocation)
        except:
            pass
        try:
            error_text=''
            time.sleep(5)
            try:
                print(" save part")
                data_save =  driver.find_element_by_id("ctl00_HomePageContent_lblWarning2")
                nmm = esicdata["Insurance Person Name"].strip()
                if(data_save.get_attribute("style") == "color:Green;"):
                    if(data_save.text.strip() == "Data saved successfully"):
                        print( "No error! ",data_save.text)
                    myprint(  str(esdata["Id"]),str(driver.title)+" :-"+str(data_save.text))
                    myprint( str(esdata["Id"]),str(driver.title)+":- Insert IP successfully for "+str(nmm))
            except:
                time.sleep(2)
                
                print("Error or warning is there insert not successful")
                span_tag = driver.find_elements_by_class_name("errordisplay")
                for sp in span_tag:
                    print("Error is:",sp.text)
                    if(sp.get_attribute("style") == "color: red; display: inline;"):
                        myprint(  str(esdata["Id"]),str(driver.title)+" :-"+ str(sp.text))
                        myprint( str(esdata["Id"]),str(driver.title)+":- Insert IP unsuccessfully for "+str(esicdata["Insurance Person Name"]))
                        error_text=str(sp.text)

                    elif(sp.get_attribute("style") == "color: red; visibility: visible;"):
                        print( "Error is:",sp.text)
                        myprint(  str(esdata["Id"]),str(driver.title)+" :-"+ str(sp.text))
                        error_text=str(sp.text)
                        myprint( str(esdata["Id"]),str(driver.title)+":- Insert IP successfully for "+str(esicdata["Insurance Person Name"]))
                    else:
                        print(" else in insert part error found")
                
                try:
                    print(" insert ---------------------------register")
                    register(driver ,esicdata,comp_name)
                except:
                    print(" register error into insert")
            try:
                emp_id= str(esdata["Id"])
                dataesic = {"emp_id":emp_id,"reason":str(error_text)} 
                headers = {'Authorization': tokenfinal}
                url="http://52.15.230.9/api/Employee/error_employee_esi"
                response = requests.post(url, data=dataesic, headers=headers)
                a=json.loads(response.text)
                print(a)
            except:
                print(" error in error_employee_esi")

        except:
            print("Inside insert except in last")
            pass
        try:
            driver.close()
            time.sleep(2)
            driver.switch_to.window(parent_window)

        except Exception as e:
            print("Exception in closing driver and shifting to window is:",e)
            myprint( str(esdata["Id"]),e)
        
    except exception as e:
        print("call exception ")
        CompInitial(e)
    


# **************** Register Part **************************
def get_download_folder(user_key):
    list_pdf = []
    #ids= "3121275541"
    user_key=str(user_key)
    try:
        list_pdf.append( "../Downloads/" + user_key +".pdf")
        list_pdf.append("../Downloads/" + user_key +"_MedicalCard.pdf")
    except Exception as e:
        home = os.path.expanduser("~")
        list_pdf.append(os.path.join(home, "Downloads\\") + user_key +".pdf")
        list_pdf.append(os.path.join(home, "Downloads\\") + user_key +"_MedicalCard.pdf")
     
    print("list of pdf merge",list_pdf)
    return list_pdf

def pdfmerge(user_key ,esicdata):
    print("call get downloder pdf path")
    user_key=user_key
    pdfs = get_download_folder(user_key)
    time.sleep(5)
    merger = PdfFileMerger()
    print(pdfs)
    for pdf in pdfs:
        merger.append(pdf)

    merger.write("./Output_esic/"+str(user_key)+".pdf")
    print("create merge pdf")
    myprint(str(esicdata["Id"]),str(user_key)+"PDF created successfully in /Output_esic/ Folder")
    merger.close() 

def state_tt(driver ,tag_id, data, error_text):
    if(data):
        dispancry = Select(driver.find_element_by_id(str(tag_id)))
        print("state,district added ")
        for ns in dispancry.options:
            nsext =ns.text
            nsext = nsext.upper()
            data = data.upper()
            if(nsext.strip() == data.strip().upper()):
                print("click data in state,district_palce",)
                x = ns.click()
                break
    else:
        print(str(driver.title)+" :-"+"Error Fill data into  "+str(error_text)) 

def register(driver ,esicdata,comp_name,retrycount ):
    global banklogin , tokenfinal,dict_company
    print("Inside register function")
    try:
        time1=random.randint(6,10)
        time.sleep(3)
        parent_window = driver.window_handles[0]
        print("Switched to register window")
        time.sleep(5)
        print("Clicking on register new ip")
        try:
            driver.find_element_by_id("lnkRegisterNewIP").click()
        except:
            try:
                time.sleep(time1)
                driver.find_element_by_id("lnkRegisterNewIP").click()
            except:
                pass 
        reg_link_window = driver.window_handles[1]
        print("Switching to new window")
        driver.switch_to.window(reg_link_window)
        time.sleep(10)
        print("Clicking on Is registered or not")
        try:
            driver.find_element_by_id("ctl00_HomePageContent_rbtnlistIsregistered_1").click()
        except:
            try:
                time.sleep(8)
                driver.find_element_by_id("ctl00_HomePageContent_rbtnlistIsregistered_1").click()
            except:
                pass
        time.sleep(4)
        try:
            print("Waiting until alert is present")
            WebDriverWait(driver,20).until(cond.alert_is_present())
            obj = driver.switch_to.alert
            msg=obj.text
            print ("Alert shows following message: "+ msg )
            obj.accept()
            time.sleep(20)
            print("clicking on continue button")
        except:
            pass
        try:
            driver.find_element_by_id("ctl00_HomePageContent_btnContinue").click() 
        except:
            try:
                time.sleep(10)
                driver.find_element_by_id("ctl00_HomePageContent_btnContinue").click() 
            except:
                try:
                    time.sleep(10)
                    driver.find_element_by_id("ctl00_HomePageContent_btnContinue").click()
                except:
                    pass
        try:
            WebDriverWait(driver,10).until(cond.alert_is_present())
            obj1 = driver.switch_to.alert
            msg1=obj1.text
            print ("Alert shows following message: "+ msg1 )
            obj1.accept()
                
        except:
            pass
        name_p = esicdata["Insurance Person Name"].strip()
        print("Finally on registeration page")
        time.sleep(15)
        try:
            driver.find_element_by_id("ctl00_HomePageContent_ctrlTextEmpName").send_keys(name_p)
        except:
            print("in except of name")
            time.sleep(40)
            driver.find_element_by_id("ctl00_HomePageContent_ctrlTextEmpName").send_keys(name_p)
            pass
        retryreg=True

        date_data = esicdata["DOB"]
        time.sleep(2)
        tag= "ctl00_HomePageContent_ctrlTxtIpDate"
        tag_name ="CalendarExtenderCtrlTxtEndDate"
        time.sleep(10)
        f_h = esicdata["Relation"]
        dict_hf = {0:"FATHER" , 1:"HUSBAND"}
        print("Clicking on radio button of father husband relation")
        for key in dict_hf:
            if(f_h.upper() == dict_hf[key]):
                try:
                    id="ctl00_HomePageContent_ctrlFatherOrHus_"+str(key)
                    relation=driver.find_element_by_id(id)
                    WebDriverWait(driver, 90).until(relation)
                    relation.click()
                except Exception as e:
                    time.sleep(8)
                    id="ctl00_HomePageContent_ctrlFatherOrHus_"+str(key)
                    inputs=driver.find_elements_by_tag_name("input")
                    for i in inputs:
                        if(i.get_attribute("id")==id):
                            i.click()
                     
        print("entering father name")
        time.sleep(4)
        relationname = esicdata["Father Husband Name"].strip()
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextFatherHusName").send_keys(relationname)
        time.sleep(4)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextFatherHusName").click()
        time.sleep(4)
        saveLocation = "./Images_esic/Register1-"+str(name_p)+".png"
        driver.save_screenshot(saveLocation)
        print("Typing DOB",date_data)
        try:
            found_date(driver ,tag, tag_name ,date_data)
        except:
            try:
                time.sleep(7)
                found_date(driver ,tag, tag_name ,date_data)
            except:
                pass
        time.sleep(4)

        m_status = Select(driver.find_element_by_id('ctl00_HomePageContent_ctrlRDMarried'))
        m_text = esicdata["Marital Status"]
        print("Entering marital status")
        for n in m_status.options:
            nn = n.text
            if(nn.upper() == m_text.upper()):
                x = n.get_attribute('value')
                m_status.select_by_value(x)
        print("Entering Gender")
        g_val = esicdata['Gender']
        gen_dict = {0:'Male' , 1:'Female' , 2:'Transgender'}
        for gkey in gen_dict:
            gn = gen_dict[gkey]
            if(gn.upper() == g_val.upper()):
                gen =driver.find_element_by_id('ctl00_HomePageContent_ctrlRDMale_'+str(gkey))
                gen.click()

        time.sleep(4)
        print("Typing Address")
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPresentAddress1").send_keys(esicdata["Present Address 1"])
        time.sleep(2)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPresentAddress2").send_keys(esicdata["Present Address 2"])
        time.sleep(4)
        saveLocation = "./Images_esic/Register2-"+str(name_p)+".png"
        driver.save_screenshot(saveLocation)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPresentAddress3").send_keys(esicdata["Present Address 3"])

        state = Select(driver.find_element_by_id('ctl00_HomePageContent_ctrlTxtPresentState'))
        s_text = esicdata["Present Address State"]
        print("Entering present state",s_text)
        for ns in state.options:
            ns_text =ns.text
            if(ns_text.upper() == s_text.upper()):
                x = ns.click()
        time.sleep(4)


        print("Entering pincode",esicdata["Present Pincode"])
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTxtPresentPinCode").send_keys(esicdata["Present Pincode"])

        time.sleep(3)

        print("Entering Mobile no:",esicdata["Present Mobile Number"])
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPresentMobileNo").send_keys(esicdata["Present Mobile Number"])


        time.sleep(4)
        distict = Select(driver.find_element_by_id('ctl00_HomePageContent_ctrlTextPresentDistrict'))
        d_text = esicdata["Present Address District"]
        d_text=d_text.strip()

        print("Present District:",d_text)
        for nsd in distict.options:
            nsd_ext= nsd.text
            nsd_ext=nsd_ext.strip()
            if(nsd_ext.upper() == d_text.upper()):
                print("Present distict name",d_text)
                x = nsd.click()
        time.sleep(3)

        saveLocation = "./Images_esic/Register3-"+str(name_p)+".png"
        driver.save_screenshot(saveLocation)
        print("Typing permanent address",esicdata["Permanant Address 1"])
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentAddress1").send_keys(esicdata["Permanant Address 1"])
        time.sleep(3)

        pstate = Select(driver.find_element_by_id('ctl00_HomePageContent_ctrlTextPermanentState'))
        ps_text = esicdata["Permanant Address State"]
        ps_text=ps_text.strip()
        print("entering permanent state:",ps_text)
        for ns in pstate.options:
            ns1text = ns.text
            ns1text=ns1text.strip()
            if(ns1text.upper() == ps_text.upper()):
                x = ns.click()
        time.sleep(3)

        pdistict = Select(driver.find_element_by_id('ctl00_HomePageContent_ctrlTextPermanentDistrict'))
        pd_text = esicdata["Permanant Address District"]
        pd_text=pd_text.strip()
        print("Entering permanent district :",pd_text)
        for nsd in pdistict.options:
            nsdtext= nsd.text
            nsdtext=nsdtext.strip()
            if(nsdtext.upper() == pd_text.upper()):
                x = nsd.click()
        time.sleep(2)

        time.sleep(5)
        ta_id ="ctl00_HomePageContent_ddlDispensaryState"
        dis_text = esicdata["IP Dispensary State"]
        dis_text=dis_text.strip()
        err_text ="IP Dispensary State"
        print("Entering Dispensary state",dis_text)
        try:
            state_tt(driver,ta_id ,dis_text,err_text)
        except:
            time.sleep(6)
            print(" Entering Dispensary statein exception")
            state_tt(driver,ta_id ,dis_text,err_text)

        time.sleep(4)
        print("Entering permant address")
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentAddress2").send_keys(esicdata["Permanant Address 2"])
        time.sleep(4)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentAddress3").send_keys(esicdata["Permanant Address 3"])
        time.sleep(4)
        print("Entering permannt pincode",esicdata["Permanant Pincode"])
        ppincode = driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentPinCode").send_keys(esicdata["Permanant Pincode"])

        time.sleep(3)

        try:
            print("Entering permnnt mobile number",esicdata["Permanant Mobile Number"])
            driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanantMobileNo").send_keys(esicdata["Permanant Mobile Number"])
        except:
            pass
        time.sleep(3)
        element = driver.find_element_by_id('ctl00_HomePageContent_ctrlTextPermanentPinCode')
        time.sleep(2)
        element.location_once_scrolled_into_view
        time.sleep(4)
        ta_idd ="ctl00_HomePageContent_ddlDispensaryDistrict"
        dis_textd = esicdata["IP Dispensary District"]
        dis_textd=dis_textd.strip()
        err_textd ="IP Dispensary District"
        print("Entering dispensary district-----",dis_textd)
        try:
            state_tt(driver,ta_idd ,dis_textd,err_textd)
        except:
            time.sleep(12)
            print("exception in entering dispenseray dependent district")
            state_tt(driver,ta_idd ,dis_textd,err_textd)
        element = driver.find_element_by_id('ctl00_HomePageContent_ctrlTextDispensary')
        element.location_once_scrolled_into_view
        print("Scrolling")
        dis_val = esicdata["Select Dispensary Or IMP or mEUD For IP"]
        dis_val=dis_val.strip()
        print("Selecting Dispensary imp meud----- ",dis_val)
        dis_dict = {0:'Dispensary' , 1:'IMP' , 2:'mEUD'}
        if(dis_val.upper() =="DISPENSARY"):
            pass
        else:
            time.sleep(3)
            for gkey in dis_dict:
                dtext =dis_dict[gkey]
                if(dtext.upper() == dis_val.upper()):
                    dis =driver.find_element_by_id('ctl00_HomePageContent_ctrlRBDispensaryIMP_'+str(gkey))
                    dis.click()
        time.sleep(8)
        ta_idd ="ctl00_HomePageContent_ctrlTextDispensary"
        dis_textd =esicdata["Select Place Dispensary Or IMP or mEUD For IP"]
        dis_textd=dis_textd.strip()
        print("Selecting state for dispensary imp meud------ ",dis_textd)
        err_textd ="Select Place Dispensary Or IMP or mEUD For IP"
        try:
            state_tt(driver,ta_idd ,dis_textd,err_textd)    
        except:
            time.sleep(12)
            print("exception in entering g state for dispensary im")
            state_tt(driver,ta_idd ,dis_textd,err_textd)

    
        time.sleep(4)
        saveLocation = "./Images_esic/Register4-"+str(name_p)+".png"
        driver.save_screenshot(saveLocation)
        ta_ids ="ctl00_HomePageContent_ddldependantDispensaryState"
        dis_texts = esicdata["Family Members Dispensary State"]
        dis_texts=dis_texts.strip()
        err_texts ="Family Members Dispensary State"
        print("entering dispenseray dependent state-----",dis_texts)
        try:
            state_tt(driver ,ta_ids ,dis_texts,err_texts)
        except:
            time.sleep(10)
            print("exception in entering dispenseray dependent state")
            state_tt(driver ,ta_ids ,dis_texts,err_texts)

        time.sleep(6)

        ta_id ="ctl00_HomePageContent_ddldependantDispensaryDistrict"
        dis_texd = esicdata["Family Members Dispensary District"]
        dis_texd=dis_texd.strip()
        print("Entering family member dispensary district-----",dis_texd)
        err_texd ="Family Members Dispensary District"
        time.sleep(4)
        try:
            state_tt(driver ,ta_id ,dis_texd,err_texd)
        except:
            time.sleep(12)
            print("exception in entering dispenseray dependent District")
            state_tt(driver ,ta_id ,dis_texd,err_texd) 
        
        dis_va9 = esicdata["Select Dispensary Or IMP or mEUD for Family Members"]
        dis_va9=dis_va9.strip()
        print("Selecing dispensary,imp,meud for family-----",dis_va9)
        time.sleep(4)
        dis_dict9 = {0:'Dispensary' , 1:'IMP' , 2:'mEUD'}
        if(dis_va9.upper() =="DISPENSARY"):
            pass
        else:
            time.sleep(6)
            for gkey in dis_dict9:
                print(gkey)
                gtest = dis_dict[gkey]
                if(gtest.upper().strip() == dis_va9.upper().strip()):
                    dis =driver.find_element_by_id('ctl00_HomePageContent_ctrlRBDependantDispensaryIMP_'+str(gkey))
                    dis.click()
        time.sleep(8)
        
        ta_id ="ctl00_HomePageContent_ddldependantdispensary"
        dis_texd =esicdata["Select Place Dispensary Or IMP or mEUD for Family Members"]
        dis_texd=dis_texd.strip()
        err_texd ="Select Place Dispensary Or IMP or mEUD for Family Members"
        print("Select Place Dispensary Or IMP or mEUD for Family Members",dis_texd)
        try:
            state_tt(driver,ta_id ,dis_texd,err_texd)
        except:
            time.sleep(12)
            print(" exception place")
            state_tt(driver,ta_id ,dis_texd,err_texd)

    
        time.sleep(3)
        
        date_data = esicdata["Date of Appointment"]
        tag ="ctl00_HomePageContent_ctrlDIDateOfAppointmentDy"
        tag_name ="cEDOA"
        print("Typing date of appointment",date_data)
        time.sleep(3)
        try:
            found_date(driver ,tag, tag_name ,date_data)
        except:
            time.sleep(10)
            print(" exception place")
            try:
                found_date(driver ,tag, tag_name ,date_data)
            except:
                pass

        time.sleep(2)
        saveLocation = "./Images_esic/Register4-"+str(name_p)+".png"
        driver.save_screenshot(saveLocation)
        try:
            pre_emp_val = esicdata["Have Previous Employer"]
            pre_emp_dict = {0:'Yes' , 1:'No' }
            print("Entering have previous employee or not",pre_emp_val)
            for key in pre_emp_dict:
                pretext = pre_emp_dict[key]
                if(pretext.upper() == pre_emp_val.upper()):
                    pre_emp =driver.find_element_by_id('ctl00_HomePageContent_ctrlRDPrevEmployer_'+str(key))
                    pre_emp.click()
            time.sleep(2)
        except:
            pass
     
        current_window = driver.window_handles[1]
        detail =  esicdata
        print("Entering details of nominee")
        Details_of_Nominee(driver, detail)
        time.sleep(2)
        
        print("Entering IP details")
        try:
            Insured_Person(driver,detail )
            driver.close()
            driver.switch_to.window(current_window)
        except:
            driver.close()
            driver.switch_to.window(current_window)
            pass
        time.sleep(2)
        print("Entering bank details")
        try:
            bank_account(driver ,detail)
        except:
            pass
        if(banklogin==True):
            driver.close()
            time.sleep(2)
            driver.switch_to.window(current_window)
        else:
            pass
        try:
            submitclicked=True
            print("Clicking on i agree buttonn")
            time.sleep(3)
            declare = driver.find_element_by_id("Tr17")
            declare_td = declare.find_element_by_class_name("sectionHeader")
            time.sleep(10)
            try:
                declare_td.find_element_by_tag_name('input').click()
                print("click agree button clicked")
            except:
                print("click agree except")
                pass
            print("I agree clicked")
            try:
                time.sleep(2)
                saveLocation = "./Images_esic/Submit"+str(name_p)+".png"
                driver.save_screenshot(saveLocation)
                WebDriverWait(driver,10).until(cond.alert_is_present())
                obj = driver.switch_to.alert
                print("fetching alert text")
                msg=obj.text
                print ("Alert shows following message: "+ msg )
                submitclicked=False
                myprint(str(esicdata["Id"]),str(driver.title)+" :-"+ str(msg))
                obj.accept()

                time.sleep(8)
                emp_id= str(esicdata["Id"])
                dataes = {"emp_id":emp_id,"reason":str(msg)} 
                headers = {'Authorization': tokenfinal}
                url="http://52.15.230.9/api/Employee/error_employee_esi"
                response = requests.post(url, data=dataes, headers=headers)
                a=json.loads(response.text)
                print(a)

            except Exception as e:
                print("exception in alert",e)
                pass

        except:
            print("Exception in end of login")
            driver.switch_to.alert.accept()

        print("Submitbutton clicked or not",submitclicked)
        time.sleep(3)
        print("clicking on submit button")
        if(submitclicked==True):
            try:
                time.sleep(4)
                driver.find_element_by_id('ctl00_HomePageContent_Submit').click()
            except Exception as e:
                time.sleep(5)
                driver.find_element_by_id('ctl00_HomePageContent_Submit').click() 
                print("submit button clicked")
            try:
                error_text=""
                span_tag = driver.find_elements_by_class_name("errordisplay")
                for sp in span_tag:
                    print("Error is:",sp.text)
                    if(sp.get_attribute("style") == "color: red; display: inline;"):
                        myprint(  str(esicdata["Id"])," :-"+ str(sp.text))
                        error_text=str(sp.text)

                    elif(sp.get_attribute("style") == "color: red; visibility: visible;"):
                        print( "Error is:",sp.text)
                        myprint(  str(esicdata["Id"])," :-"+ str(sp.text))
                        error_text=str(sp.text)
                print("error",error_text)
                if(error_text):
                    emp_id= str(esicdata["Id"])
                    dataes = {"emp_id":emp_id,"reason":str(error_text)} 
                    headers = {'Authorization': tokenfinal}
                    url="http://52.15.230.9/api/Employee/error_employee_esi"
                    response = requests.post(url, data=dataes, headers=headers)
                    a=json.loads(response.text)
                    print(a)
                else:
                    pass
            except:
                pass
                    
            try:
                window_pechan = driver.window_handles[1]
                driver.switch_to.window(window_pechan)
                time.sleep(7)
                ip_no  = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelIPNumber")
                myprint(str(esicdata["Id"]),str(driver.title)+" :-"+"Save data Successfully")
                user_key = ip_no.text
                myprint(str(esicdata["Id"]),str(driver.title)+" :-"+str(esicdata["Insurance Person Name"])+ " person Insurance Number == "+ str(ip_no.text))
                print("Clicking on medical link")
                time.sleep(5)
                driver.find_element_by_id("ctl00_HomePageContent_DeclForm").click()
                try:
                    empname= driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelName").text
                except:
                    pass
                saveLocation = "./Images_esic/Card"+str(user_key)+".png"
                driver.save_screenshot(saveLocation)   
                emp_no = str(ip_no.text)
                emp_id= esicdata["Id"]
                company_id = dict_company[comp_name]
                print(" emp number",emp_no)
                #url="https://workzdata.s3.amazonaws.com/company/"+str(company_id)+"/employee/"+ str(emp_id)+"/"+ str(emp_no)+".pdf"
                time.sleep(5)
                printf = driver.find_element_by_id('ctl00_HomePageContent_print').click()
                print("Clicking on print link")
                time.sleep(2)
                print("call pdf merge function")
                pdfmerge(user_key,esicdata)
                print("pdf merge complete")
                time.sleep(2)
                bucket_upload(emp_id ,company_id,emp_no )
            except:
                print("Exception in downloading pdf page")
        else:
            pass
        time.sleep(5)
        try:
            driver.close()
            driver.switch_to.window(parent_window ) # first page control
        except:
            driver.close()
            driver.switch_to.window(parent_window)
    except Exception as e:
        try:
            driver.find_element_by_id("lnkRegisterNewIP")
        except:
            driver.close()
            driver.switch_to.window(parent_window )
        print("exception in register try again register",e)
        if(retrycount<4):
            myprint(str(esicdata["Id"]),"Retry Register again"+str(e))
            print("Retry for register count==",retrycount)
            time.sleep(5)
            retrycount=retrycount+1
            register(driver ,esicdata,comp_name,retrycount)
        else:
            print("count is greater",retrycount)
            

def pehchan_card (driver ,user_key,esicdata ,comp_name):
    global dict_company
    print("Inside pehchan card")
    try:
        time1=random.randint(5,9)
        time.sleep(time1)
        window_before = driver.window_handles[0]
        print("clicking on pehchan card")
        driver.find_element_by_id("lnkCounterFoil").click()
        window_after = driver.window_handles[1]
        driver.switch_to_window(window_after)
        time2=random.randint(10,15)
        time.sleep(time2)
        print("Typing Insurance number:",user_key)
        try:
            driver.find_element_by_id("ctl00_HomePageContent_ctrlTextEmpeIPNo").send_keys(user_key)
        except Exception as e:
            time.sleep(20)
            driver.find_element_by_id("ctl00_HomePageContent_ctrlTextEmpeIPNo").send_keys(user_key)
        time.sleep(4)
        try:
            print("Clicking on view")
            driver.find_element_by_id("ctl00_HomePageContent_ctrlBtnShow").click()
            time.sleep(5)
            try:
                driver.find_element_by_id("ctl00_HomePageContent_gvEmployeList_ctl02_lnlViweCounterfolil").click()
                print("view counter click")
            except:
                time.sleep(8)
                driver.find_element_by_id("ctl00_HomePageContent_gvEmployeList_ctl02_lnlViweCounterfolil").click()
                pass
            saveLocation = "./Images_esic/InsertCard"+str(user_key)+".png"
            driver.save_screenshot(saveLocation)
            try:
                ip_no  = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelIPNumber")
            except:
                pass
            try:
                emp_no = str(ip_no.text)
                print(" emp number",emp_no)
                company_id = dict_company[comp_name]
                emp_id= esicdata["Id"]
            except:
                pass
            error_msg=''
            try:
                time.sleep(4)
                span_tag = driver.find_element_by_id("ctl00_HomePageContent_ctrlLblError")
                if(span_tag.text == "No Records Found."):
                    print( "Error in records:",span_tag.text)
                    myprint( str(esicdata["Id"]),str(driver.title)+" :-Error "+ str(span_tag.text))
                    error_msg="No Records Found."
                
            except:
                spa_tag = driver.find_element_by_id("ctl00_HomePageContent_RegularExpressionValidator3")
                print( "Regular expression error ",spa_tag.text)
                myprint(str(esicdata["Id"]), str(driver.title)+" :-Error "+ str(spa_tag.text))
                errpr_msg=str(spa_tag.text)
            if(error_msg):
                emp_id= str(esicdata["Id"])
                dataes = {"emp_id":emp_id,"reason":str(error_msg)} 
                headers = {'Authorization': tokenfinal}
                url="http://52.15.230.9/api/Employee/error_employee_esi"
                response = requests.post(url, data=dataes, headers=headers)
                a=json.loads(response.text)
                print(a)
            else:
                pass
        except:
            pass
        time.sleep(4)
        try:
            try:
                driver.find_element_by_id("ctl00_HomePageContent_DeclForm").click()
            except:
                time.sleep(4)
                driver.find_element_by_id("ctl00_HomePageContent_DeclForm").click()
            print("Clciking on medical link")
            time.sleep(5)
            try:
                driver.find_element_by_id('ctl00_HomePageContent_print').click()
            except:
                time.sleep(4)
                driver.find_element_by_id('ctl00_HomePageContent_print').click()
            print("Clicking on another link")
            time.sleep(2)
            print("calling pdf merge function")
            pdfmerge(user_key,esicdata)
            pdf_name= emp_no
            print("pdf merge complete")
            time.sleep(2)
            bucket_upload(emp_id ,company_id,pdf_name )
        except Exception as e:
            print(e)
            pass
        try:
            driver.close()
            driver.switch_to_window(window_before)
            print("Switching to previous window")

        except:
            time.sleep(2)
            print("Error in switching")
    except Exception as e:
        print(e)
        CompInitial(e)

# *****************login part  ********************************
def login(cred_user ,driver):
    global tokenfinal
    employer = cred_user["username"]
    pwdd = cred_user["password"]
    time.sleep(2)
    saveLocation = "./Images_esic/LoginPage.png"
    driver.save_screenshot(saveLocation)
    try:
        edata = esic_sheet(employer,pwdd)
    except Exception as e:
        print("Exception in data",e)
    user_name = driver.find_element_by_id("txtUserName")
    pwd = driver.find_element_by_id("txtPassword")
    captcaha = driver.find_element_by_id("txtChallanCaptcha")
    try:
        user_name.send_keys(Keys.CONTROL + "a")
        user_name.send_keys(Keys.DELETE)

        pwd.send_keys(Keys.CONTROL + "a")
        pwd.send_keys(Keys.DELETE)

        captcaha.send_keys(Keys.CONTROL + "a")
        captcaha.send_keys(Keys.DELETE)
        time.sleep(10)
    except:
        print("error")
    user_n = cred_user["username"]
    pwdd = cred_user["password"]
    user_name.send_keys(user_n)
    print("username enetered")
    time.sleep(1)
    pwd.send_keys(pwdd)
    print("Password enetered")
    down = driver.find_element_by_id("img1")
    location = down.location
    size = down.size
    png = driver.get_screenshot_as_png() 
    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot.png')
    print("Captcha image saved")

    av = mainpage("screenshot")
    print("Captcha extracted is:",av)

    prv_url = driver.current_url
    driver.find_element_by_id("txtChallanCaptcha").send_keys(av)
    print("captcha entered")
    time1=random.randint(9,12)
    time.sleep(time1)
    saveLocation = "./Images_esic/Captcha.png"
    driver.save_screenshot(saveLocation)
    driver.find_element_by_id('btnLogin').click()
    curr_url = driver.current_url
    print("Current url:",curr_url)
    try:
        time.sleep(4)
        saveLocation = "./Images_esic/click_login_button.png"
        driver.save_screenshot(saveLocation)
        driver.find_element_by_id("div1_close").click()
        print("Closing message box")
        time1=random.randint(5,8)
        time.sleep(time1)
        print("Closing next alert")
        time1=random.randint(5,8)
        time.sleep(time1)
        driver.find_element_by_id("btnClose").click()
        try:
            time.sleep(4)
            print("closing next alert")
            driver.find_element_by_id("btnCloseMsg").click()
        except:
            pass
        print("Fetching data from xl file")
        time.sleep(3)
        saveLocation = "./Images_esic/loginSuccess.png"
        driver.save_screenshot(saveLocation)

        myprint(str(user_n),"Login successful")
        parent = driver.window_handles[0]
        print("shifting to window 0")
        try:
            for i in range(0,len(edata)):
                print( " data found",i)
                ip= edata[i]["Insurance Number"]
                cnt = i+1
                comp_name=cred_user["username"]
                print("insurance number",ip,"Employee numbr:",str(cnt))
                try:
                    if(ip):
                        try:
                            data = edata[i]
                            try:
                                insert_data(driver,data ,comp_name)
                            except Exception as e:
                                print("Exception insert_data then retry",e)
                                insert_data(driver,data ,comp_name)
                            try:
                                pehchan_card (driver ,ip , data ,comp_name)
                            except Exception as e:
                                print("Exception pehchan_card then retry",e) 
                                pehchan_card (driver ,ip , data ,comp_name)
                        except Exception as e:
                            print("Trying again INSERT_IP",e)
                            myprint(str(edata[i]["Id"]),"Unknown Error Occur")
                            emp_id= str(edata[i]["Id"])
                            msg="Unknown Error Occur"
                            dataes = {"emp_id":emp_id,"reason":str(msg)} 
                            headers = {'Authorization': tokenfinal}
                            url="http://52.15.230.9/api/Employee/error_employee_esi"
                            response = requests.post(url, data=dataes, headers=headers)
                            a=json.loads(response.text)
                            print(a)
                            #driver.close()
                            try:
                                driver.find_element_by_id("ctl00_HomePageContent1_clickme").click()
                            except:
                                pass
                            driver.switch_to.window(parent)
                            try:
                                insert_data(driver,data ,comp_name)
                            except Exception as e:
                                print("Exception insert_data then retry",e)
                                
                            try:
                                pehchan_card (driver ,ip , data ,comp_name)
                            except Exception as e:
                                print("Exception pehchan_card then retry",e) 
                                
                            #insert_data(driver,data ,comp_name)
                            #pehchan_card (driver ,ip , data ,comp_name)
                    else:
                        try:
                            data = edata[i]
                            retrycount=1
                            register(driver ,data, comp_name,retrycount)
                        except Exception as e:
                            print("register exception",e)
                            try:
                                driver.find_element_by_id("lnkRegisterNewIP")
                            except:
                                driver.close()
                                driver.switch_to.window(parent)


                except Exception as e:
                    driver.close()
                    driver.switch_to.window(parent)
                    print('Inside exception of for loop:',e)

        except Exception as e:
                print(" first loop",e)


    except Exception as e:
        print("exception in login",e)
        time.sleep(5)
        span_tag = driver.find_elements_by_id("lblChallanMessage")
        error_message =''
        for sp in span_tag:
            #print("p tab means error tag",sp.text)
            if(sp.text):
                print( "Error ",sp.text)
                myprint( str(user_n),str(sp.text))
        auth_span_tag = driver.find_elements_by_id("lblMessage")
        for asp in auth_span_tag:
            print("error tag",asp.text)
            if(asp.text):
                print( "Error ",asp.text)
                myprint(str(user_n),":- Username And Password must be correct " + str(asp.text))      
        time.sleep(2)
        myprint(str(user_n),":- Unsuccessful Login")
        myprint(str(user_n),":- Try to Login again")
        print("inside except")
        saveLocation = "./Images_esic/login_again.png"
        driver.save_screenshot(saveLocation)
        login(cred_user ,driver)
        time.sleep(5)
                
def driver_esic():
    global dict_drivers
    print("driver info ",dict_drivers)
    return dict_drivers              
# *************************** main *************************************

def main_esic(cred_user):
    global dict_drivers
    print("*******************  "+ str(datetime.now())+"   *************************")
    options = webdriver.FirefoxOptions()
    #options.add_argument("--headless")
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 1)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    #profile.set_preference("browser.download.dir", 'C:\Users\Zebronics\Downloads\shikha\')
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/pdf")
    profile.set_preference("pdfjs.disabled", True)
    #driver = webdriver.Firefox(executable_path='./geckodriver',firefox_profile=profile,firefox_options=options)
    driver = webdriver.Firefox(executable_path='./geckodriver.exe',firefox_profile=profile)
    time.sleep(4)
    driver.get('https://www.esic.in/ESICInsurance1/ESICInsurancePortal/Portal_Login.aspx')
    #driver.maximize_window()
    user=cred_user["username"]
    time.sleep(2)
    saveLocation = "./Images_esic/MainPage.png"
    driver.save_screenshot(saveLocation)
    driver_name = str("driver")+str(user)
    print("driver name-------------------******",driver_name)
    dict_drivers[driver_name]=driver
    loginlink = driver.find_element_by_xpath('//*[@id="LinkLoginpage"]')
    loginlink.click()
    time1=random.randint(5,9)
    time.sleep(time1)
    clickhere = driver.find_element_by_xpath('//*[@id="lnklogin"]')
    clickhere.click()
    try:
        login(cred_user ,driver)
    except Exception as e:
        myprint(str(user), " :- *** Error "+ str(e))
        print(" error in login",e)



