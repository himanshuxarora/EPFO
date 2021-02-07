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

global dict_drivers
dict_drivers={}
from esic_adddate import FoundDate
from esic_commonfunction import ScreenShotTake ,RaiseException
from esic_api import MyPrint,UpdateApi,BucketUpload,EsicData,ErrorApi,EsicLogin

def NomineePart6(driver,edata,count,esicdata):
    time.sleep(4)
    try:
        save_tag = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelSaved") 
        if(save_tag.get_attribute("style")=="color:Red;font-weight:bold;"):
            print("error in insured details ",save_tag.text)
            sv= save_tag.text
            ErrorApi(str(esicdata["Id"]),str(sv))
            MyPrint(str(esicdata["Id"]),str(driver.title)+" :-"+ str(sv))
        time.sleep(2)
    except Exception as e:
        print(e)


def NomineePart5(driver,edata,count,esicdata):
    time.sleep(4)
    driver.find_element_by_id("ctl00_HomePageContent_ctrlButtonSave").click()
    try:
        time.sleep(5)
        span_tag = driver.find_elements_by_class_name("errordisplay")
        for sp in span_tag:
            if(sp.get_attribute("style") == "color: red; display: inline;"):
                print( "Error insured person",sp.text)
                error_txt=sp.text
                ErrorApi(str(esicdata["Id"]),str(sv))
                MyPrint(str(esicdata["Id"]), str(edata["ID"])+" Error:- "+ sp.text)
            elif(sp.get_attribute("style") == "color: red; visibility: visible;"):
                print( "Error insured person",sp.text)
                error_txt=sp.text
                MyPrint(str(esicdata["Id"]), str(edata["ID"])+" Error:- "+ sp.text)
    except:
        pass

    try:
        time.sleep(4)
        save_tag = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelSaved") 
        if( save_tag.text == "Details are saved successfully"):
            print("Saved data successfully ",save_tag.text)
            saveLocation = "./Images_esic/savedsuccessfully.png"
            driver.save_screenshot(saveLocation)
            sv= save_tag.text
            MyPrint(str(esicdata["Id"]),str(driver.title)+" :-"+str(sv))  
        time.sleep(2)
    except:
        print("error insured person")
        time.sleep(2)
        pass


def NomineePart4(driver,edata,count):
    checkstate=False
    res_val = edata["Whether Residing with"]
    print(" Whether Residing with",res_val)
    if(res_val.upper() =="YES"):
        driver.find_element_by_id('ctl00_HomePageContent_ctrlRDIpDisable_0').click()
    else:
        checkstate=True
        driver.find_element_by_id('ctl00_HomePageContent_ctrlRDIpDisable_1').click()

    if(checkstate==True):
        try:
            time.sleep(4)
            statedata = Select(driver.find_element_by_id('ctl00_HomePageContent_ctrlTextPermanentState'))
            stext = edata["State"]
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
            d_text = edata["District"]
            print("Entering Insured person State",d_text)
            if(d_text):
                for nsd in distictdata.options:
                    nm=nsd.text
                    if(nm.upper().strip() == d_text.upper().strip()):
                        x = nsd.click()
                        break
        except Exception as e:
            print("nominee part 4exception",e)


def NomineePart3(driver,edata,count):
    time.sleep(4)
    relationship = Select(driver.find_element_by_id('ctl00_HomePageContent_CtrlRelation'))
    rtext = edata["Relation"]
    for nsr in relationship.options:
        gntext = nsr.text
        if(gntext.upper().strip() == rtext.upper().strip()):
            x = nsr.click()
            break
    try:
        rttext = edata["Gender"]
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
        #RaiseException(str(e))
        print("nominee 3 exception",e)
        

def NomineePart2(driver,edata,count):
    try:
        nametxt=driver.find_element_by_id("ctl00_HomePageContent_txtName")
        nametxt.send_keys(Keys.CONTROL + "a")
        nametxt.send_keys(Keys.DELETE)
    except Exception as e:
        pass
    driver.find_element_by_id("ctl00_HomePageContent_txtName").send_keys(edata['Person Name'])
    time.sleep(2)
    date_data = edata["DOB"]
    div_id_tag ="ctl00_HomePageContent_CtrlDOB"
    div_id_name ="cEDOA"
    time.sleep(6)
    FoundDate(driver  ,div_id_tag, div_id_name ,date_data)


def Nomineepart1(driver,esicdata,data,Insured):
    print("inside nomineepart1")
    name_p=esicdata["Insurance Person Name"]
    Insured_td = Insured.find_element_by_class_name("lastFormValue")
    Insured_td.find_element_by_tag_name('a').click()
    time.sleep(3)
    insured_window = driver.window_handles[2]
    driver.switch_to.window(insured_window)
    time.sleep(5)
    count = 1
    for i_l in data:
        count=count+1
        NomineePart2(driver,i_l,count)
        NomineePart3(driver,i_l,count)
        NomineePart4(driver,i_l,count)
        #NomineePart5(driver,data,count,esicdata)
        #NomineePart6(driver,data,count,esicdata)
        NomineePart5(driver,i_l,count,esicdata)
        NomineePart6(driver,i_l,count,esicdata)
    print("nominee part completed")
def InsuredPerson(driver,esicdata):
    try:
        time.sleep(6)
        saveLocation = "./Images_esic/fetchedip.png"
        driver.save_screenshot(saveLocation)
        print("Clicking on insured person details")
        Insured=""
        Insured = driver.find_element_by_id("Tr12")
        str3=driver.title
        print("driver title",str3)
        list_add_in = esicdata["Insured person details"]
        print("Fetched ip_person")
        reg_window = driver.window_handles[1]
        time.sleep(6)
        Nomineepart1(driver,esicdata,list_add_in,Insured)
    except Exception as e:
        print("insured Error",e)
        #RaiseException(str(e))
        
    

