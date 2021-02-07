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

from esic_adddate import FoundDate
from esic_api import MyPrint,UpdateApi,BucketUpload,EsicData,ErrorApi,EsicLogin
from esic_commonfunction import RaiseException

def nomineepart4(driver,detail):
    time.sleep(3)
    driver.find_element_by_id("ctl00_HomePageContent_Save").click()
    time.sleep(3)
    print("Save button clicked")
    try:
        span_tag = driver.find_elements_by_class_name("errordisplay")
        if(span_tag):
            for sp in span_tag:
                if(sp.get_attribute("style") == "color: red; display: inline;"):
                    print( "Error in nominee details",sp.text)
                    ErrorApi(str(detail["Id"]),str(sp.text))
                    MyPrint(str(detail["Id"]), str(driver.title)+" :-"+ str(sp.text))
                elif(sp.get_attribute("style") == "color: red; visibility: visible;"):
                    print( "Error in nominee details",sp.text)
                    ErrorApi(str(detail["Id"]),str(sp.text))
                    MyPrint(str(detail["Id"]), str(driver.title)+" :-"+ str(sp.text))
                

        save_tag = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelSaved") 
        if(save_tag):
            if( save_tag.text == "Data saved successfully"):
                print("Save data successfully ",save_tag.text)
                sv= save_tag.text
                MyPrint(str(detail["Id"]),str(driver.title)+" :-"+ str(sv))

    except Exception as e:
        print("Error in detail of nominee",e)
        #RaiseException(str(e))

def nomineepart3(driver,detail):
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
    print("Selecting whether nominee a family member")
    time.sleep(4)
    if(non_val.upper()=="YES"):
        driver.find_element_by_id('ctl00_HomePageContent_rbtnlistNomneeAkaFamily_0').click()
    elif(non_val.upper()=="NO"):
        driver.find_element_by_id('ctl00_HomePageContent_rbtnlistNomneeAkaFamily_1').click()
    time.sleep(3)

def nomineepart2(driver,detail):
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


def Nomineepart1(driver,detail):
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

def DetailsOfNominee(driver,detail):
    try:
        time.sleep(6)
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
        Nomineepart1(driver,detail)
        nomineepart2(driver,detail)
        nomineepart3(driver,detail)
        nomineepart4(driver,detail)
        try:
            driver.close()
            driver.switch_to.window(reg_window)
            time.sleep(2)
        except:
            driver.close()
            driver.switch_to.window(reg_window)
            time.sleep(2)

    except Exception as e:
        print("insured Error",e)
        #RaiseException(str(e))
        
    

