import time
import requests
from PyPDF2 import PdfFileMerger
import sys,os 
from datetime import datetime
import json
import csv
import json
import requests
import random

from esic_commonfunction import ScreenShotTake ,RaiseException

def YearSeries(driver,tag,tag_name,date_data, dy_format,match,year_text):
    for j in range(0,25):
        try:
            year_series= driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_title").text
            y_series = year_series.split("-")
            if( y_series[0] <= year_text  and y_series[1]>= year_text ):
                # between 2000-2010
                year_find = driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_yearsBody")
                tr_year =  year_find.find_elements_by_tag_name("tr")
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
            print('here man error year loop raise',e)
            RaiseException(str(e))
            break

def SelectYear(driver,tag,tag_name,date_data, dy_format,match):
    try:
        a=driver.find_element_by_id(str(tag)).click() 
        for i in range(0,5):
            to_day = datetime.now()
            cal_today = to_day.strftime('%d-%m-%Y')
            cal_list = cal_today.split('-')      
            year_text = dy_format.strftime('%Y')
            first = driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_title").click()
            time.sleep(2)
            second = driver.find_element_by_id("ctl00_HomePageContent_"+str(tag_name)+"_title").click()
            time.sleep(2)
            YearSeries(driver,tag,tag_name,date_data, dy_format,match,year_text)
    except Exception as e:
        print("error Year raise",e)
        RaiseException(str(e))
        

def SelectMonth(driver,tag,tag_name,date_data, dy_format,match,s_list):
    try:
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
    except Exception as e:
        print("error month raise",e)
        RaiseException(str(e))
def SelectDay(driver,tag,tag_name,date_data, dy_format,match,s_list):
    try:
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
    except Exception as e:
        print("error day raise",e)
        RaiseException(str(e))

def FoundDate(driver ,tag, tag_name ,date_data):
    #send_day = "12-03-2009" # day-month-year
    try:
        s_list = date_data.split('-')
        print("ADd date--",date_data)
        dy_format = datetime.strptime(date_data,'%d-%m-%Y')
        print("tag:",tag,"tag_name:",tag_name,"date_data:",date_data)
        match = []
        SelectYear(driver,tag,tag_name,date_data, dy_format,match)
        SelectMonth(driver,tag,tag_name,date_data, dy_format,match,s_list)
        SelectDay(driver,tag,tag_name,date_data, dy_format,match,s_list)
    except Exception as e:
        print("error year month,day,year raise",e)
        RaiseException(str(e))      
    try:
        time.sleep(2)
        driver.find_element_by_id("ctl00_HomePageContent_btnAgree").click()
        time.sleep(3)
    except Exception as e:
        print(" not found agree popup raise",e)
        

           
        


