from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
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
from excel2json import convert_from_file
global banklogin
import json
import requests
import boto3
import random


def RaiseException(fullstring):
    substring = "Component not initialized"
    if substring.upper() in fullstring.upper():
        print("Found!")
        raise Exception(fullstring)

def AlertAccept(driver):
    print("Alert accept fun()")
    try:
        msg=''
        time.sleep(2)
        print("wait")
        try:
            WebDriverWait(driver,20).until(cond.alert_is_present())
        except:
            pass
        print("switch")
        obj = driver.switch_to.alert
        print("switched")
        msg=obj.text
        print("text")
        print ("Alert shows following message: "+ msg )
        obj.accept()
        print("accepted")
        time.sleep(15)
    except Exception as e:
        print("Error alertbox raise",e)
        msg='unknown'
        try:
            driver.switch_to.alert.accept()
        except:
            pass
        print("handled by alertaccept")
        RaiseException(str(e))
    return msg

def ScreenShotTake(driver,name):
    saveLocation = "./Images_esic/"+str(name)+".png"
    driver.save_screenshot(saveLocation)



def GetDownloadFolder(user_key):
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

def PdfMerge(user_key ,esicdata):
    print("call get downloder pdf path")
    pdfs = GetDownloadFolder(user_key)
    time.sleep(5)
    merger = PdfFileMerger()
    print(pdfs)
    for pdf in pdfs:
        merger.append(pdf)

    merger.write("./Output_esic/"+str(user_key)+".pdf")
    print("create merge pdf")
    #myprint(str(esicdata["Id"]),str(user_key)+"PDF created successfully in /Output_esic/ Folder")
    merger.close() 

def StateDistrict(driver ,tag_id, data, error_text):
    try:
        time.sleep(13)
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
                    time.sleep(10)
                    break
        else:
            print(str(driver.title)+" :-"+"Error Fill data into  "+str(error_text)) 
    except Exception as e:
        print("Error StateDistrict raise",e)
        RaiseException(str(e))

