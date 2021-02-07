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

from esic_api import MyPrint,UpdateApi,BucketUpload,EsicData,ErrorApi,EsicLogin
from esic_commonfunction import ScreenShotTake ,GetDownloadFolder,PdfMerge,RaiseException

def SecondPage(driver,esicdata,username):
    try:
        time.sleep(5)
        ip_no  = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelIPNumber")
        emp_no = str(ip_no.text)
        print(" emp number",emp_no)
        time.sleep(6)
        driver.find_element_by_id("ctl00_HomePageContent_DeclForm").click()
        print("Clciking on medical link")
        time.sleep(6)
        driver.find_element_by_id('ctl00_HomePageContent_print').click()
        print("Clicking on another link")
        time.sleep(2)
        print("calling pdf merge function")
        PdfMerge(emp_no,esicdata)
        pdf_name= emp_no
        print("pdf merge complete")
        time.sleep(2)
        emp_id=esicdata["Id"]
        BucketUpload(emp_id,username,pdf_name )
    except Exception as e:
        print("Error",e)
        MyPrint(str(username),"Excepton in pdf merge"+str(e))
        RaiseException(str(e))

def ErrorCode(driver,esicdata):
    try:
        time.sleep(4)
        span_tag = driver.find_element_by_id("ctl00_HomePageContent_ctrlLblError")
        if(span_tag.text == "No Records Found."):
            ErrorApi(str(esicdata["Id"]),str(span_tag.text))
            print( "Error in records:",span_tag.text)
            MyPrint( str(esicdata["Id"]),str(driver.title)+" :-Error "+ str(span_tag.text))
            error_msg="No Records Found."
        
    except:
        spa_tag = driver.find_element_by_id("ctl00_HomePageContent_RegularExpressionValidator3")
        print( "Regular expression error ",spa_tag.text)
        ErrorApi(str(esicdata["Id"]),str(span_tag.text))
        MyPrint(str(esicdata["Id"]), str(driver.title)+" :-Error "+ str(spa_tag.text))



def FirstPage(driver,user_key):
    try:
        time.sleep(10)
        driver.find_element_by_id("ctl00_HomePageContent_ctrlTextEmpeIPNo").send_keys(user_key)
        time.sleep(4)
        print("Clicking on view")
        driver.find_element_by_id("ctl00_HomePageContent_ctrlBtnShow").click()
        time.sleep(8)
        
        driver.find_element_by_id("ctl00_HomePageContent_gvEmployeList_ctl02_lnlViweCounterfolil").click()
        return driver
    except Exception as e:
        print("Error pcard raise",e)
        RaiseException(str(e))

def PehchanCard(driver,esicdata,username,pcount):
    user_key=str(esicdata["Insurance Number"])
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

        driver=FirstPage(driver,user_key)
        ErrorCode(driver,esicdata)
        SecondPage(driver,esicdata,username)
        driver.close()
        driver.switch_to_window(window_before)
    except Exception as e:
        driver.close()
        driver.switch_to_window(window_before)
        print(" pechan card error",e)
        if(pcount<2):
            pcount=pcount+1
            PehchanCard(driver,esicdata,username,pcount)

    return driver

