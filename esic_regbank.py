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

from esic_api import MyPrint,ErrorApi
from esic_commonfunction import ScreenShotTake ,RaiseException

def BankPart1(driver,esicdata,count):
    timeout = 120
    element_present = EC.presence_of_element_located((By.ID, "ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_CheckBox"))
    WebDriverWait(driver, timeout).until(element_present)
    time.sleep(4)
    driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_CheckBox").click()
    time.sleep(4)
    #account_no = driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_AccountNumber").send_keys(int(esicdata['Account Number']))
    time.sleep(4)

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

def ThirdRemove(count,fcount,driver):
    if(fcount>1):
        field=driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_BankName")
        Delete(field)
        field2=driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_MICRCode")
        Delete(field2)
        field3=driver.find_element_by_id("ctl00_HomePageContent_gdvBankDetails_ctl0"+str(count)+"_IFSCCode")
        Delete(field3)
        

def BankPart2(driver,esicdata,count,fcount):
    try:
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
        ThirdRemove(count,fcount,driver)
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
    except Exception as e:
        print("Error eleven raise",e)
        #RaiseException(str(e))
        substring = "Component not initialized"
        if substring.upper() in str(e).upper():
            print("Found! not inintal eight error retry again")
            if(fcount<3):
                fcount=fcount+1
                time.sleep(15)
                ElevenPart(driver,esicdata,fcount)


def BankPart3(driver,esicdata):
    try:
        time.sleep(4)
        span_tag = driver.find_elements_by_class_name("errordisplay")
        for sp in span_tag:
            if(sp.get_attribute("style") == "color: red; display: inline;"):
                print( "Error in bank details",sp.text)
                ErrorApi(str(esicdata["Id"]),str(sp.text))
                MyPrint(  str(esicdata["Id"]),str(driver.title)+" :-"+ str(sp.text))
            elif(sp.get_attribute("style") == "color: red; visibility: visible;"):
                print( "Error in bank details",sp.text)
                ErrorApi(str(esicdata["Id"]),str(sp.text))
                MyPrint(  str(esicdata["Id"]),str(driver.title)+" :-"+ str(sp.text))
        time.sleep(3)
        save_tag = driver.find_element_by_id("ctl00_HomePageContent_ctrlLabelSaved") 
        if( save_tag.text == "Details are saved successfully"):
            print("save data successfully ",save_tag.text)
            sv= save_tag.text
            MyPrint(str(esicdata["Id"]),str(driver.title)+" :-"+str(sv))

    except:
        print("error detail of bank details")
        pass


def BankAccount(driver,esicdata,banklogin):
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
        count2=1
        if(banklogin==True):
            BankPart1(driver,esicdata,count)
            BankPart2(driver,esicdata,count,count2)
            BankPart3(driver,esicdata)
    except Exception as e:
        print("exception bank",e)
        #RaiseException(str(e))
        banklogin=False

    return banklogin
        
    




