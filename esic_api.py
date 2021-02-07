import time
from datetime import datetime
import requests
from PyPDF2 import PdfFileMerger
import sys,os 
import json
global banklogin
import json
import boto3
import random

global dict_company,tokenfinal
dict_company={} # insoide esicdata api to add data in a particular bucket
tokenfinal=""

from esic_commonfunction import RaiseException

def MyPrint(emp_id,status):
    global tokenfinal
    dataesic = {"emp_id":emp_id,"log_text":status} 
    headers = {'Authorization': tokenfinal}
    url="http://3.136.53.191/api/Employee/addlogesi"
    response = requests.post(url, data=dataesic, headers=headers)
    a=json.loads(response.text)
    status=status+'\n'
    with open('./esiclogs.txt','a') as b:
        b.write(str(status))
    print(status,"===",a)

def UpdateApi(url,dataesic):
    global tokenfinal
    headers = {'Authorization': tokenfinal}
    url="http://3.136.53.191/api/Employee/update_employee_esi"
    response = requests.post(url, data=dataesic, headers=headers)
    a=json.loads(response.text)
  
def BucketUpload(emp_id ,username,pdf_name ):
    global tokenfinal,dict_company
    print("inside bucket upload")
    comp_name=dict_company[str(username)]
    ACCESS_ID="AKIAJ3VLARDR5HBZ6ZSA"
    ACCESS_KEY="jBav0NCBFnRjzg3Td6WeR+yb6sUJ5kiLz3ccRCeR"
    s3 = boto3.resource('s3',aws_access_key_id=ACCESS_ID,aws_secret_access_key= ACCESS_KEY)
    print(" company"+str(comp_name)+', emp'+str(emp_id)+' pdf_name'+str(pdf_name))
    s3.Object('workzdata', 'company/'+str(comp_name)+'/employee/'+str(emp_id)+'/'+str(pdf_name)+'.pdf').upload_file('./Output_esic/'+str(pdf_name)+'.pdf')
    MyPrint(str(emp_id),"Add pdf into Bucket")
    url="https://workzdata.s3.amazonaws.com/company/"+str(comp_name)+"/employee/"+ str(emp_id)+"/"+ str(pdf_name)+".pdf"
    dataesic = {"emp_id":emp_id,"esi_no":pdf_name,"tic_letter":url} 
    UpdateApi(url,dataesic)

def EsicLogin(username,pwd):
    global tokenfinal,dict_company
    try:
        print("inside esiclogi fun")
        data = {'email':'super.admin@workz.in','password':'Admin@Workz19'} 
        response = requests.post('http://3.136.53.191/api/Authentication/Login', data) 
        login = json.loads(response.text)
        print("response from login",login)
        tokenfinal= login["Token"]
        company_id=login["Result"]["company_id"]
        dict_company[username]=company_id       
    except Exception as e:
        print("exception login api",e)
        MyPrint(str(username),"Excepton in esic login authentication"+str(e))

def EsicData(username,pwd):
    global tokenfinal,dict_company
    try:
        dataesic = {"username":username,"password":pwd}
        headers = {'Authorization': tokenfinal}
        url="http://3.136.53.191/api/Employee/DataForESI"
        response = requests.post(url, data=dataesic, headers=headers)
        a=json.loads(response.text)
    except Exception as e:
        MyPrint(str(username),"Exception in fetching esic data"+str(e))
    try:
        datastore = a["Result"]
    except:
        datastore=[]
        MyPrint(str(username),"Data is empty")

    return datastore

def ErrorApi(emp_id,error_txt):
    global tokenfinal
    dataes = {"emp_id":emp_id,"reason":str(error_txt)} 
    headers = {'Authorization': tokenfinal}
    url="http://3.136.53.191/api/Employee/error_employee_esi"
    response = requests.post(url, data=dataes, headers=headers)
    a=json.loads(response.text)
    error_txt=error_txt+'\n'
    with open('./esicerrors.txt','a') as w:
        w.write(str(error_txt))