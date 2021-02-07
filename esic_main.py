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

#call different classes
from esic_commonfunction import ScreenShotTake ,RaiseException
from esic_api import MyPrint,UpdateApi,BucketUpload,EsicData,ErrorApi,EsicLogin
from esic_insert import InsertData
from esic_pechancard import PehchanCard
from esic_adddate import FoundDate
from esic_register import Register
global dict_drivers
dict_drivers={}
                
def DriverEsic():
    global dict_drivers
    print("driver info ",dict_drivers)
    return dict_drivers

# *************************** main *************************************
def LoopOverData(driver,data,cred_user):
     for i in range(0,len(data)):
        print( " data found",i)
        ip= data[i]["Insurance Number"]
        cnt = i+1
        username=cred_user["username"]
        print("insurance number",ip,"Employee numbr:",str(cnt))
        insertdata = data[i]
        insertcount=1
        pcount=1
        retrycount=1
        if(ip):
            driver = InsertData(driver,insertdata,username,insertcount)
            driver= PehchanCard(driver,insertdata,username,pcount)
        else:
            #register()
            print("register")
            Register(driver,insertdata,username,retrycount)


def LoginSuccess(driver,username,checklogin):
    time.sleep(15)
    print("login success function")
    deriversuccess=driver
    try:
        deriversuccess.find_element_by_id("div1_close").click()
        print("Closing message box")
        time1=random.randint(5,8)
        time.sleep(time1)
        print("Closing next alert")
        time1=random.randint(5,8)
        time.sleep(time1)
        deriversuccess.find_element_by_id("btnClose").click()
        time.sleep(4)
        print("closing next alert")
        deriversuccess.find_element_by_id("btnCloseMsg").click()
        MyPrint(str(username),"Login Successful")
        checklogin=True
        driver=deriversuccess
    except Exception as e:
        print("error in login success",e)
        MyPrint(str(username),str(e))
        checklogin=False
    return driver,checklogin

def LoginUnsuccess(driver,username):
    time.sleep(5)
    print("unsuccess function")
    span_tag = driver.find_elements_by_id("lblChallanMessage")
    error_txt =''
    for sp in span_tag:
        #print("p tab means error tag",sp.text)
        if(sp.text):
            print( "Error ",sp.text)
            MyPrint( str(username),str(sp.text))
    auth_span_tag = driver.find_elements_by_id("lblMessage")
    for asp in auth_span_tag:
        print("error tag",asp.text)
        if(asp.text):
            print( "Error ",asp.text)
            MyPrint(str(username),":- Username And Password must be correct " + str(asp.text))      
    time.sleep(2)
    if(error_txt):
        ErrorApi(str(username),error_txt)
    MyPrint(str(username),":- Unsuccessful Login")
    MyPrint(str(username),":- Try to Login again")
    return driver


def CaptchaFill(driver):
    print("captcha function")
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
    driver.find_element_by_id("txtChallanCaptcha").send_keys(av)
    print("captcha entered")
    time1=random.randint(9,12)
    time.sleep(time1)
    return driver

def Login(driver,cred_user):
    print("loginfunction function")
    user_name = driver.find_element_by_id("txtUserName")
    pwd = driver.find_element_by_id("txtPassword")
    captcaha = driver.find_element_by_id("txtChallanCaptcha")
    username = cred_user["username"]
    try:
        user_name.send_keys(Keys.CONTROL + "a")
        user_name.send_keys(Keys.DELETE)

        pwd.send_keys(Keys.CONTROL + "a")
        pwd.send_keys(Keys.DELETE)

        captcaha.send_keys(Keys.CONTROL + "a")
        captcaha.send_keys(Keys.DELETE)
        time.sleep(5)
    except Exception as e:
        print("Error ",e)
        RaiseException(str(e))
        MyPrint(str(username),"Excepton in typing credentials"+str(e))
    pwdd = cred_user["password"]
    user_name.send_keys(username)
    MyPrint(str(username),"Username entered")
    print("username enetered",username)
    time.sleep(1)
    pwd.send_keys(pwdd)
    MyPrint(str(username),"Password entered")
    print("passwrd enetered",pwdd)
    driver = CaptchaFill(driver)
    driver.find_element_by_id('btnLogin').click()
    return driver

def CheckLogin(driver,cred_user,checklogin):
    print("checkfunction function")
    driver = Login(driver,cred_user)
    username=cred_user["username"]
    driver,checklogin=LoginSuccess(driver,username,checklogin)
    print("check login variable==",checklogin)
    if(checklogin==False):
        driver=LoginUnsuccess(driver,username)
        driver,checklogin=CheckLogin(driver,cred_user,checklogin)
        print("checklogin,driver data-----",driver,checklogin)
    else:
        checklogin=True
        print("login success",checklogin)
    return driver ,checklogin

def OpenEsicPortal(driver,cred_user):
    global dict_drivers
    print("open esic portal function")
    driver.get('https://www.esic.in/ESICInsurance1/ESICInsurancePortal/Portal_Login.aspx')
    user=cred_user["username"]
    time.sleep(2)
    driver_name = str("driver")+str(user)
    ScreenShotTake(driver,"mainpage")
    print("driver name-------------------******",driver_name)
    dict_drivers[driver_name]=driver
    loginlink = driver.find_element_by_xpath('//*[@id="LinkLoginpage"]')
    loginlink.click()
    time1=random.randint(5,9)
    time.sleep(time1)
    clickhere = driver.find_element_by_xpath('//*[@id="lnklogin"]')
    clickhere.click()
    return driver

def OpenFirefox(count):
    try:
        print(" open OpenFirefox function")
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
    except Exception as e:
        print("Error OpenFirefox",e)
        if(count<3):
            count=count+1
            OpenFirefox(count)

    return driver

# main function handle all function
def MainEsic(cred_user):
    global dict_drivers
    print("main function of esic",cred_user)
    EsicLogin(cred_user["username"],cred_user["password"])
    print("*******************  "+ str(datetime.now())+" Start*************************")
    openFcount=1
    driver=OpenFirefox(openFcount)

    try:
        driver= OpenEsicPortal(driver,cred_user)
    except Exception as e:
        print("Error",e)
        driver=OpenEsicPortal(driver,cred_user)

    print("global dict_drivers",dict_drivers)
    checklogin=False
    driver,checklogin= CheckLogin(driver,cred_user,checklogin)
    print("driver ,checklogin==",checklogin)
    if(checklogin==True):
        print("Login successful--------",checklogin)
        data=EsicData(cred_user["username"],cred_user["password"])
        if(data):
            print("esic api data")
            LoopOverData(driver,data,cred_user)