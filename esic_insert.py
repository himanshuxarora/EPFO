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

from esic_commonfunction import ScreenShotTake ,GetDownloadFolder,RaiseException

from esic_api import MyPrint,UpdateApi,BucketUpload,EsicData,ErrorApi,EsicLogin
from esic_adddate import FoundDate


def lnkInsertIPDetails(driver):
    print("Clicking on insert ip details")
    time.sleep(8)
    driver.find_element_by_id("lnkInsertIPDetails").click()

    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    time.sleep(4)
    print("Clicking on insert")

    time.sleep(8)
    driver.find_element_by_id("ctl00_HomePageContent_ctrlInsert").click()
    return driver
def InsertInsuranceNumber(driver,esdata):
    print("handling window")
    window_after2 = driver.window_handles[1]
    driver.switch_to.window(window_after2)
    time.sleep(7)
    #driver.maximize_window()
    print("Typing insurance number")
    driver.find_element_by_id("ctl00_HomePageContent_txtInsuranceNumber").send_keys(esdata["Insurance Number"])
    time.sleep(5)
    print("Clicking on insurance name")
    driver.find_element_by_id("ctl00_HomePageContent_txtInsuranceName").click() 
    return driver

def AddAppointementDate(driver,esdata):
    span = driver.find_element_by_id("ctl00_HomePageContent_lblWarning2")
    test = str(span.text)
    
    print("span text if error present",test)
    if(test):
        print("If error present:",span.text)
        if(span.get_attribute("style") == "color:Red;"):
            MyPrint( str(esdata["Id"]),str(driver.title)+" :-"+ str(span.text))
    else:
        print("No warning",span)
        date_data = esdata["Date of Appointment"]
        print("Date of apt",date_data)
        tag="ctl00_HomePageContent_txtpdcfdcDate"
        tag_name ="calFromTxt"
        try:
            FoundDate(driver ,tag, tag_name ,date_data)
        except:
            time.sleep(7)
            try:
                FoundDate(driver ,tag, tag_name ,date_data)
            except:
                pass
    time.sleep(8)
    driver.find_element_by_id('ctl00_HomePageContent_btnSubmit').click()
    return driver

def InsertError(driver,esicdata,registerdata):
    try:
        print(" save part")
        data_save =  driver.find_element_by_id("ctl00_HomePageContent_lblWarning2")
        empname = esicdata["Insurance Person Name"].strip()
        if(data_save.get_attribute("style") == "color:Green;"):
            if(data_save.text.strip() == "Data saved successfully"):
                print( "No error! ",data_save.text)
            MyPrint(  str(esdata["Id"]),str(driver.title)+" :-"+str(data_save.text))
            MyPrint( str(esdata["Id"]),str(driver.title)+":- Insert IP successfully for "+str(empname))
    except:
        time.sleep(2)
        print("Error or warning is there insert not successful")
        span_tag = driver.find_elements_by_class_name("errordisplay")
        for sp in span_tag:
            print("Error is:",sp.text)
            if(sp.get_attribute("style") == "color: red; display: inline;"):
                MyPrint(  str(esdata["Id"]),str(driver.title)+" :-"+ str(sp.text))
                MyPrint( str(esdata["Id"]),str(driver.title)+":- Insert IP unsuccessfully for "+str(esicdata["Insurance Person Name"]))
                registerdata=True

            elif(sp.get_attribute("style") == "color: red; visibility: visible;"):
                print( "Error is:",sp.text)
                MyPrint(  str(esdata["Id"]),str(driver.title)+" :-"+ str(sp.text))
                registerdata=True
                MyPrint( str(esdata["Id"]),str(driver.title)+":- Insert IP successfully for "+str(esicdata["Insurance Person Name"]))
            else:
                print(" else in insert part error found")
    return driver,registerdata

def InsertData(driver,esdata ,username,insertcount):
    time.sleep(5)
    parent_window = driver.window_handles[0]
    registerdata=False
    try:
        driver= lnkInsertIPDetails(driver)
        driver= InsertInsuranceNumber(driver,esdata)
        driver=AddAppointementDate(driver,esdata)
        driver,registerdata=InsertError(driver,esdata,registerdata)
        driver.close()
        time.sleep(2)
        print("Switch to Parent Window")
        driver.close()
        driver.switch_to.window(parent_window)
        if(registerdata==True):
            print("Insurance Number not Fount so Register again",registerdata)
            #Register(driver ,esdata,username)
    except Exception as e:
        print("Error in insertdata",e)
        MyPrint(str(username),"Excepton in insert data"+str(e))
        driver.close()
        driver.switch_to.window(parent_window)
        if(insertcount<3):
            insertcount=insertcount+1
            InsertData(driver,esdata ,username,insertcount)
    return driver
        
