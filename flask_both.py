import flask
from flask import request,current_app,render_template,send_from_directory
from flask_cors import CORS
from epfo_flask import epfo_login,driver_epfo
#from esic_main import main_esic,driver_esic
from esic_main import MainEsic,DriverEsic
from trello import TrelloClient
from esic_api import MyPrint
client = TrelloClient(
    api_key='7cca21f3fe0e4b4dc32abdedcc35c9fd',
    token='fce0aca9948aa07b1c3856b71097102f360e8f2d9ef133c0978283ad022f99b5')

def trellocheckepfo():
    check=""
    all_boards = client.list_boards()
    board=all_boards[0]
    all_lists=board.list_lists()
    for lst in all_lists:
        if(lst.name =="DataKund EPFO/ESIC Automation"):
            all_cards=lst.list_cards()
            for card in all_cards:
                if(card.name =="EPFO"):
                    print("fol")
                    if card.closed == False:
                        desc=card.description
                        check = desc.upper()
    return check
def trellocheckesic():
    check=""
    all_boards = client.list_boards()
    board=all_boards[0]
    all_lists=board.list_lists()
    for lst in all_lists:
        if(lst.name =="DataKund EPFO/ESIC Automation"):
            all_cards=lst.list_cards()
            for card in all_cards:
                if(card.name =="ESIC"):
                    print("fol")
                    if card.closed == False:
                        desc=card.description
                        check = desc.upper()
    return check


app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

@app.route('/startesic', methods=['POST'])
def startesic():
    cred_user={}
    status_es=''
    checkstatus=True
    try:
        data=request.get_json()
        user=data["username"]
    except:
        status_es='Please provide username and password'
        checkstatus=False
    if(checkstatus==True):
        check= trellocheckesic()
        print("check trello value",check)
        if(check == "TRUE"):
            try:
                MainEsic(data)
                status_es='True'
            except Exception as e:
                print("exception in startesic api",e)
                MyPrint(str(user),"Excepton in esic start api"+str(e))
                status_es='True'
        else:
            status_es='Check your permissions'
            print("Check your permissions")
    else:
        print("empty username")
    response = flask.jsonify({'status': status_es})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/stopesic', methods=['POST'])
def stopesic():
    status_es=''
    checkstatus=True
    try:
        driver=''
        data=request.get_json()
        user=data["username"]
    except:
        status_es='Please provide username field'
        checkstatus=False
    if(checkstatus==True):
        dict_drivers= DriverEsic()
        print("DRIVER INFO*********************ESIC",dict_drivers)
        d_name = str("driver")+ str(user)
        print(" stop username",d_name)
        try:
            driver=dict_drivers[d_name]
        except:
            status_es='True'
        if(driver):
            print("driver is present")
            driver.quit()
            status_es='True'
    else:
        print(" not present username")
    response = flask.jsonify({'status': status_es})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route('/startepfo', methods=['POST'])
def startepfo():
    cred_user={}
    status_epfo=''
    checkstatus=True
    try:
        data=request.get_json()
        user=data["username"]
    except Exception as e:
        checkstatus=False
        print("exception error",e)
        status_epfo='Please provide username and password'
    if(checkstatus==True): 
        check= trellocheckepfo()
        print(check)
        if(check == "TRUE"):
            try:
                epfo_login(data)
                status_epfo='True'
            except Exception as e:
                status_epfo='True'
                print(e)
        else:
            print(" Check is ",check)
            status_epfo="Check your permissions"
            print("Check your permissions")
    else:
        print("Username error")

    response = flask.jsonify({'status': status_epfo})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/stopepfo', methods=['POST'])
def stopepfo():
    status=''
    checkstatus=True
    try:
        data=request.get_json()
        user=data["username"]
    except:
        status='Please provide username field'
        checkstatus=False
    if(checkstatus==True):
        driver=''
        try:
            dict_drivers=driver_epfo()
            print("DRIVER INFO-------------------EPFO",dict_drivers)
            d_name = str("driver")+ str(user)
            print(" stop username",d_name)
            driver=dict_drivers[d_name]
        except:
            status='True'
        if(driver):
            print("driver is present")
            driver.quit()
            status='True'
    
    else:
        print("not present username")
        
    response = flask.jsonify({'status': status})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
   
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
    app.run()

