from my_app import app
from flask import render_template, jsonify, request
import pyodbc
import hashlib
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
secret_key = "password"
returnCode = {
    'wrongToken':{"code":-222,"msg":'Wrong Token'},
    'InternalError':{"code:":-224,"msg":'Internal Error'},
    'loginSuccess':{"code":-225,"msg":'Login success'},
    'wrongIdOrPasswd':{"code":-226,"msg":'wrongIdOrPasswd'}
}
def querySqlGetLoginInfo(cardId):
    server = '11.11.11.16,9433'
    database = 'CRM'
    username = 'rk7'
    password = 'rk7'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    myfile = cnxn.cursor()
    return myfile.execute("""select 
                                CARD_PEOPLES.TEXT_PASSWORD,
                                CARD_CARDS.CARD_CODE
                                from CARD_PEOPLES
                                left join CARD_CARDS on CARD_CARDS.PEOPLE_ID = CARD_PEOPLES.PEOPLE_ID
                                WHERE ((CARD_CODE = {}))
                             """.format(cardId))


@auth.verify_password
def verify_password(token,password):
    print(request.headers)
    if token == "fuckubitch":
        return True
    else:
        return False

@app.route('/api/v1')
def hello_world():
    return "<h1>HYG CRM APIs</h1>"

@app.route('/api/v1/cardinfo/<cardId>/<inputPasswd>')
@auth.login_required
def checkCardLoginPassword(cardId,inputPasswd):
    queryResults = querySqlGetLoginInfo(cardId)
    results = {}
    # If database have 2 record it definitely an error
    try:
        results['passwordHash'],results['cardId'] = [x for x in queryResults.fetchall()[0]]
    except:
        return jsonify(returnCode['InternalError'])
    # If not continue to check MD5 checksum of password
    md5Object = hashlib.md5()
    md5Object.update(inputPasswd.encode('utf-8'))
    inputPasswdInMD5= md5Object.hexdigest().upper()
    if inputPasswdInMD5 == results['passwordHash']:
        return jsonify(returnCode['loginSuccess'])
    else:
        return jsonify(returnCode['wrongIdOrPasswd'])


@app.errorhandler(404)
def page_not_found(error):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404