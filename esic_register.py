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


from esic_commonfunction import ScreenShotTake,StateDistrict ,GetDownloadFolder,PdfMerge,AlertAccept,RaiseException
from esic_api import MyPrint,UpdateApi,BucketUpload,EsicData,ErrorApi,EsicLogin
from esic_adddate import FoundDate
from esic_regnominee import DetailsOfNominee
from esic_reginsured import InsuredPerson
from esic_regbank import BankAccount

def Delete(user_name):
    print("remove previous field data")
    user_name.send_keys(Keys.CONTROL + "a")
    user_name.send_keys(Keys.DELETE)

def FourPart(driver,esicdata,fcount):
    try:
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

        print("Typing permanent address",esicdata["Permanant Address 1"])
        if(fcount>1):
            field=driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentAddress1")
            Delete(field)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentAddress1").send_keys(esicdata["Permanant Address 1"])
        time.sleep(6)
    except Exception as e:
        print("Error four part raise",e)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal four error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                FourPart(driver,esicdata,fcount)
def ThirdRemove(fcount,driver):
    if(fcount>1):
        field=driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPresentAddress1")
        Delete(field)
        field2=driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPresentAddress2")
        Delete(field2)
        field3=driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPresentAddress3")
        Delete(field3)
        field4=driver.find_element_by_id("ctl00_HomePageContent_ctrlTxtPresentPinCode")
        Delete(field4)
        field5=driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPresentMobileNo")
        Delete(field6)

def ThirdPart(driver,esicdata,fcount):
    try:
        print("Typing Address")
        ThirdRemove(fcount,driver)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPresentAddress1").send_keys(esicdata["Present Address 1"])
        time.sleep(2)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPresentAddress2").send_keys(esicdata["Present Address 2"])
        time.sleep(4)
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
    except Exception as e:
        print("Error third raise",e)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal third error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                ThirdPart(driver,esicdata,fcount)

def SecondPart(driver,esicdata,fcount):
    try:
        date_data = esicdata["DOB"]
        time.sleep(2)
        tag= "ctl00_HomePageContent_ctrlTxtIpDate"
        tag_name ="CalendarExtenderCtrlTxtEndDate"
        print("Typing DOB",date_data)
        time.sleep(5)
        FoundDate(driver ,tag, tag_name ,date_data)

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
    except Exception as e:
        print("Error second raise",e)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal second error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                SecondPart(driver,esicdata,fcount)

def FirstPart(driver,esicdata,fcount):
    try:
        time.sleep(5)
        driver.find_element_by_id("ctl00_HomePageContent_btnContinue").click() 
        AlertAccept(driver)   
        name_p = esicdata["Insurance Person Name"].strip()
        print("Finally on registeration page")
        time.sleep(20)
        if(fcount>1):
            field=driver.find_element_by_id("ctl00_HomePageContent_ctrlTextEmpName")
            Delete(field)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextEmpName").send_keys(name_p)
        time.sleep(5)
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
        time.sleep(2)
        if(fcount>1):
            field2=driver.find_element_by_id("ctl00_HomePageContent_ctrlTextFatherHusName")
            Delete(field2)
        relationname = esicdata["Father Husband Name"].strip()
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextFatherHusName").send_keys(relationname)
        time.sleep(4)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextFatherHusName").click()
        time.sleep(4)
    except Exception as e:
        print("Error first raise",e)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal first error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                FirstPart(driver,esicdata,fcount)


def FivePart(driver,esicdata,fcount):
    try:
        pstate = Select(driver.find_element_by_id('ctl00_HomePageContent_ctrlTextPermanentState'))
        ps_text = esicdata["Permanant Address State"]
        ps_text=ps_text.strip()
        print("entering permanent state:",ps_text)
        for ns in pstate.options:
            ns1text = ns.text
            ns1text=ns1text.strip()
            if(ns1text.upper() == ps_text.upper()):
                x = ns.click()
        time.sleep(5)
        print("Entering permant address")
        if(fcount>1):
            field=driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentAddress2")
            Delete(field)
            field2=driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentAddress3")
            Delete(field2)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentAddress2").send_keys(esicdata["Permanant Address 2"])
        time.sleep(4)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentAddress3").send_keys(esicdata["Permanant Address 3"])
        time.sleep(4)
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
    except Exception as e:
        print("Error five raise",e)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal five error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                FivePart(driver,esicdata,fcount)

def SixPart(driver,esicdata,fcount):
    try:
        time.sleep(25)
        ta_id ="ctl00_HomePageContent_ddlDispensaryState"
        dis_text = esicdata["IP Dispensary State"]
        dis_text=dis_text.strip()
        err_text ="IP Dispensary State"
        print("Entering Dispensary state",dis_text)
        StateDistrict(driver,ta_id ,dis_text,err_text)
        time.sleep(14)
        if(fcount>1):
            field=driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentPinCode")
            Delete(field)
            time.sleep(10)
        print("Entering permannt pincode",esicdata["Permanant Pincode"])
        ppincode = driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanentPinCode").send_keys(esicdata["Permanant Pincode"])
        time.sleep(13)
    except Exception as e:
        print("Error six raise",e)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal six error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(30)
                SixPart(driver,esicdata,fcount)

def SevenPart(driver,esicdata,fcount):
    try:
        try:
            print("Entering permnnt mobile number",esicdata["Permanant Mobile Number"])
            driver.find_element_by_id("ctl00_HomePageContent_ctrlTextPermanantMobileNo").send_keys(esicdata["Permanant Mobile Number"])
        except Exception as e:
            print("Error permanent mobile raise",e)
            RaiseException(str(e))
        time.sleep(13)
        element = driver.find_element_by_id('ctl00_HomePageContent_ctrlTextPermanentPinCode')
        time.sleep(12)
        element.location_once_scrolled_into_view
        time.sleep(14)
        ta_idd ="ctl00_HomePageContent_ddlDispensaryDistrict"
        dis_textd = esicdata["IP Dispensary District"]
        dis_textd=dis_textd.strip()
        err_textd ="IP Dispensary District"
        print("Entering dispensary district-----",dis_textd)
        StateDistrict(driver,ta_idd ,dis_textd,err_textd)
        time.sleep(30)
    except Exception as e:
        print("Error seven raise",e)
        time.sleep(30)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal seven error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                SevenPart(driver,esicdata,fcount)
def EightPart(driver,esicdata,fcount):
    try:
        time.sleep(15)
        element = driver.find_element_by_id('ctl00_HomePageContent_ctrlTextDispensary')
        element.location_once_scrolled_into_view
        print("Scrolling")
        time.sleep(10)
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
        StateDistrict(driver,ta_idd ,dis_textd,err_textd)
        time.sleep(12)
    except Exception as e:
        time.sleep(30)
        print("Error eight raise",e)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal eight error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                EightPart(driver,esicdata,fcount)

def NinePart(driver,esicdata,fcount):
    try:
        time.sleep(14)
        ta_ids ="ctl00_HomePageContent_ddldependantDispensaryState"
        dis_texts = esicdata["Family Members Dispensary State"]
        dis_texts=dis_texts.strip()
        err_texts ="Family Members Dispensary State"
        print("entering dispenseray dependent state-----",dis_texts)
        StateDistrict(driver ,ta_ids ,dis_texts,err_texts)
        time.sleep(16)
        ta_id ="ctl00_HomePageContent_ddldependantDispensaryDistrict"
        dis_texd = esicdata["Family Members Dispensary District"]
        dis_texd=dis_texd.strip()
        print("Entering family member dispensary district-----",dis_texd)
        err_texd ="Family Members Dispensary District"
        time.sleep(14)
        StateDistrict(driver ,ta_id ,dis_texd,err_texd)
    except Exception as e:
        print("Error nine raise",e)
        time.sleep(30)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal nine error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                NinePart(driver,esicdata,fcount)

def TenPart(driver,esicdata,fcount):
    try:
        time.sleep(15)
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
    except Exception as e:
        time.sleep(30)
        print("Error ten raise",e)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal ten error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                TenPart(driver,esicdata,fcount)

def ElevenPart(driver,esicdata,fcount):
    try:
        time.sleep(15)
        ta_id ="ctl00_HomePageContent_ddldependantdispensary"
        dis_texd =esicdata["Select Place Dispensary Or IMP or mEUD for Family Members"]
        dis_texd=dis_texd.strip()
        err_texd ="Select Place Dispensary Or IMP or mEUD for Family Members"
        print("Select Place Dispensary Or IMP or mEUD for Family Members",dis_texd)
        StateDistrict(driver,ta_id ,dis_texd,err_texd)
        time.sleep(3)
        date_data = esicdata["Date of Appointment"]
        tag ="ctl00_HomePageContent_ctrlDIDateOfAppointmentDy"
        tag_name ="cEDOA"
        print("Typing date of appointment",date_data)
        time.sleep(5)
        FoundDate(driver ,tag, tag_name ,date_data)
        time.sleep(12)
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
        except Exception as e:
            print("Error raise have pervioud ",e)
            RaiseException(str(e))
    except Exception as e:
        time.sleep(30)
        print("Error eleven raise",e)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal eight error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                ElevenPart(driver,esicdata,fcount)

def NomineeBankInsured(driver,esicdata):
    try:
        current_window = driver.window_handles[1]
        print("Entering details of nominee")
        DetailsOfNominee(driver, esicdata)
        time.sleep(12)
        print("Entering IP details")
        try:
            InsuredPerson(driver,esicdata )
            driver.close()
            driver.switch_to.window(current_window)
        except Exception as e:
            saveLocation = "./Images_esic/errinsured.png"
            driver.save_screenshot(saveLocation)
            driver.close()
            driver.switch_to.window(current_window)
            print("error in insured person raise",e)
            #RaiseException(str(e))
        time.sleep(2)
        print("Entering bank details")
        banklogin=False
        try:
            saveLocation = "./Images_esic/WHENBANK.png"
            driver.save_screenshot(saveLocation)
            banklogin= BankAccount(driver ,esicdata,banklogin)
        except Exception as e:
            print("error in bankn raise",e)
            RaiseException(str(e))
        if(banklogin==True):
            driver.close()
            time.sleep(2)
            driver.switch_to.window(current_window)
        else:
            pass
    except Exception as e:
        print("Error nominee,bank,insured raise",e)
        #RaiseException(str(e))


def SubmitButton(driver,esicdata):
    submitclicked=True
    print("Clicking on i agree button")
    time.sleep(8)
    #declare = driver.find_element_by_id("Tr17")
    #declare_td =declare.find_element_by_class_name("sectionHeader")
    #time.sleep(10)
    #declare_td.find_element_by_tag_name('input').click() 

    driver.find_element_by_id("ctl00_HomePageContent_dec_chkbox").click()
    print("button clciked")
    time.sleep(2)
    try:
        saveLocation = "./Images_esic/clickagree.png"
        driver.save_screenshot(saveLocation)
    except:
        pass
    try:
        print("inside try of submitbutton")
        msg = AlertAccept(driver)
        if(msg=='' or msg==""):
            submitclicked=True
        elif(msg=='unknown'):
            msg='Unable to fetch alert text, when clicked on i agree'
            submitclicked=False
        else:
            submitclicked=False
        print("submitclicked",submitclicked)
        MyPrint(str(esicdata["Id"]),str(driver.title)+" :-"+ str(msg))
        ErrorApi(str(esicdata["Id"]),str(msg))
        print("errrrr")
    except Exception as e:
        print("Exception in end of login",e)
        try:
            driver.switch_to.alert.accept()
        except:
            pass
        print("handled ")
        #RaiseException(str(e))
    return submitclicked
def PechanCardDowbload(driver,esicdata,username):
    try:
        window_pechan = driver.window_handles[1]
        driver.switch_to.window(window_pechan)
        time.sleep(7)
        ip_no  = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelIPNumber")
        MyPrint(str(esicdata["Id"]),str(driver.title)+" :-"+"Save data Successfully")
        user_key = ip_no.text
        MyPrint(str(esicdata["Id"]),str(driver.title)+" :-"+str(esicdata["Insurance Person Name"])+ " person Insurance Number == "+ str(ip_no.text))
        print("Clicking on medical link")
        time.sleep(5)
        driver.find_element_by_id("ctl00_HomePageContent_DeclForm").click()
        #empname= driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelName").text 
        emp_no = str(ip_no.text)
        emp_id= esicdata["Id"]
        print(" emp number",emp_no)
        #url="https://workzdata.s3.amazonaws.com/company/"+str(company_id)+"/employee/"+ str(emp_id)+"/"+ str(emp_no)+".pdf"
        time.sleep(5)
        printf = driver.find_element_by_id('ctl00_HomePageContent_print').click()
        print("Clicking on print link")
        time.sleep(2)
        print("call pdf merge function")
        PdfMerge(user_key,esicdata)
        print("pdf merge complete")
        time.sleep(2)
        BucketUpload(emp_id ,username,emp_no )
    except Exception as e:
        print("Exception in downloading pdf functionregister raise",e)
        #RaiseException(str(e))

def ClickSubmitButton(driver,esicdata,username,submitclicked):
    try:
        print("click submit button",submitclicked)
        if(submitclicked==True):
            time.sleep(8)
            driver.find_element_by_id('ctl00_HomePageContent_Submit').click()
            print("submit button clicked")
            span_tag = driver.find_elements_by_class_name("errordisplay")
            for sp in span_tag:
                print("Error is:",sp.text)
                if(sp.get_attribute("style") == "color: red; display: inline;"):
                    MyPrint(  str(esicdata["Id"])," :-"+ str(sp.text))
 
                elif(sp.get_attribute("style") == "color: red; visibility: visible;"):
                    print( "Error is:",sp.text)
                    MyPrint(  str(esicdata["Id"])," :-"+ str(sp.text))
            print("doenload epachan card***")
            PechanCardDowbload(driver,esicdata,username)
    except Exception as e:
        print("Exception register submit button",e)
        #RaiseException(str(e))

 

def Register(driver,esicdata,username,retrycount):
    try:
        time.sleep(5)
        parent_window = driver.window_handles[0]
        print("Switched to register window")
        time.sleep(10)
        print("Clicking on register new ip")
        driver.find_element_by_id("lnkRegisterNewIP").click()
        reg_link_window = driver.window_handles[1]
        print("Switching to new window")
        driver.switch_to.window(reg_link_window)
        time.sleep(10)
        driver.find_element_by_id("ctl00_HomePageContent_rbtnlistIsregistered_1").click()
        count1,count2,count3,count4,count5,count6,count7,count8,count9,count10,count11=1,1,1,1,1,1,1,1,1,1,1
        msg=AlertAccept(driver)
        FirstPart(driver,esicdata,count1)
        print("waiting for scroll")
        time.sleep(9)
        SecondPart(driver,esicdata,count2)
        ThirdPart(driver,esicdata,count3)
        FourPart(driver,esicdata,count4)
        FivePart(driver,esicdata,count5)
        SixPart(driver,esicdata,count6)
        SevenPart(driver,esicdata,count7)
        EightPart(driver,esicdata,count8)
        NinePart(driver,esicdata,count9)
        TenPart(driver,esicdata,count10)
        ElevenPart(driver,esicdata,count11)
        NomineeBankInsured(driver,esicdata)
        submitclicked=SubmitButton(driver,esicdata)
        ClickSubmitButton(driver,esicdata,username,submitclicked)

        driver.close()
        driver.switch_to.window(parent_window ) # first page control
    except Exception as e:
        print("exception in register try again register",e)
        try:
            print("check driver close")
            driver.find_element_by_id("lnkRegisterNewIP")
        except:
            print("check driver not close close driver")
            driver.close()
            driver.switch_to.window(parent_window )
        print("retry not happen check retry count",retrycount)
        # if(retrycount<4):
        #     myprint(str(esicdata["Id"]),"Retry Register again"+str(e))
        #     print("Retry for register count==",retrycount)
        #     time.sleep(5)
        #     retrycount=retrycount+1
        #     Register(driver,esicdata,username,retrycount)
        # else:
        #     print("count is greater",retrycount)


            

