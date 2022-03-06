from flask import Flask,request,jsonify
from flask_restful import Api,Resource
from pymongo import MongoClient
import bcrypt
import uuid

app=Flask(__name__)
api=Api(app)

client=MongoClient("mongodb://db:27017")
db=client.BankAPI
users=db["Users"]

def UserExist(username):
    if users.count_documents({"Username":username})==0:
        return False
    return True

class Register(Resource):
    def post(self):
        postedData=request.get_json()
        fullname=postedData["fullname"]
        username=postedData["username"]
        password=postedData["password"]
        phoneno=postedData["phoneno"]

        if UserExist(username):
            retJson={
            "message":"Username already exists",
            "Status":"301"
            }
            return jsonify(retJson)
        hashed_pwd=bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
        users.insert_one({
        "Fullname":fullname,
        "Username":username,
        "Password":hashed_pwd,
        "Phoneno":phoneno,
        "Own":0,
        "Debt":0
        })
        retJson={
        "message":"Successfully Signed Up",
        "Status":200
        }
        return jsonify(retJson)

def verifyPw(username,password):
    if not UserExist(username):
        return False
    hashed_pw=users.find({"Username":username})[0]["Password"]
    if hashed_pw==bcrypt.hashpw(password.encode('utf8'),hashed_pw):
        return True
    return False
def cashWithUser(username):
    cash=users.find({
    "Username":username
    })[0]["Own"]
    return cash
def debtWithUser(username):
    debt=users.find({
    "Username":username
    })[0]["Debt"]
    return debt
def generateReturnDictionary(status,msg):
    retJson={
    "message":msg,
    "status":status
    }
    return retJson
    #ErrorDictionary, True/False
def verifyCredentials(username,password):
    if not UserExist(username):
        return generateReturnDictionary(301,"Invalid Username"),True
    correct_pw=verifyPw(username,password)

    if not correct_pw:
        return generateReturnDictionary(302,"Incorrect Password"),True
    return None,False

def updateAccount(username,balance):
    users.update_one({
    "Username":username
    },{"$set":{
    "Own":balance
    }})

def updateDebt(username,balance):
    users.update_one({
    "Username":username
    },{
    "$set":{"Debt":balance}
    })

class Add(Resource):
    def post(self):
        postedData=request.get_json()
        username=postedData["username"]
        password=postedData["password"]
        money=postedData["amount"]

        retJson,error=verifyCredentials(username,password)
        if error:
            return jsonify(retJson)
        if money<=0:
            return jsonify(generateReturnDictionary(304,"The money amount entered must be greater than zero"))
        cash=cashWithUser(username)
        money-=1
        bank_cash=cashWithUser("BANK")
        updateAccount("BANK",bank_cash+1)
        updateAccount(username,cash+money)
        retJson={
        "Transaction_Id":str(uuid.uuid4()),
        "message":"Amount added successfully to account",
        "status":200
        }
        return jsonify(retJson)
class Transfer(Resource):
    def post(self):
        postedData=request.get_json()
        username=postedData["username"]
        password=postedData["password"]
        to=postedData["to"]
        money=postedData["amount"]
        retJson,error=verifyCredentials(username,password)

        if error:
            return jsonify(retJson)

        cash=cashWithUser(username)
        if cash<=0:
            return jsonify(generateReturnDictionary(304,"You're out of money, please add or take a loan"))
        if not UserExist(to):
            return jsonify(generateReturnDictionary(301,"Receiver Username is invalid"))
        cash_from=cashWithUser(username)
        cash_to=cashWithUser(to)
        bank_cash=cashWithUser("BANK")
        updateAccount("BANK",bank_cash+1)
        updateAccount(to,cash_to+money-1)
        updateAccount(username,cash_from-money)
        retJson={
        "Transaction_Id":str(uuid.uuid4()),
        "message":"Amount Transferred successfully",
        "status":200
        }
        return jsonify(retJson)

class Balance(Resource):
    def post(self):
        postedData=request.get_json()
        username=postedData["username"]
        password=postedData["password"]

        retJson,error=verifyCredentials(username,password)

        if error:
            return jsonify(retJson)

        retJson=users.find({
        "Username":username
        },{
        "Password":0,
        "_id":0
        })[0]
        return jsonify(retJson)

class TakeLoan(Resource):
    def post(self):
        postedData=request.get_json()
        username=postedData["username"]
        password=postedData["password"]
        money=postedData["amount"]

        retJson,error=verifyCredentials(username,password)

        if error:
            return jsonify(retJson)
        cash=cashWithUser(username)
        debt=debtWithUser(username)
        updateAccount(username,cash+money)
        updateDebt(username,debt+money)
        retJson={
        "Transaction_Id":str(uuid.uuid4()),
        "message":"Loan added to your account",
        "status":200
        }
        return jsonify(retJson)

class PayLoan(Resource):
    def post(self):
        postedData=request.get_json()
        username=postedData["username"]
        password=postedData["password"]
        money=postedData["amount"]

        retJson,error=verifyCredentials(username,password)
        if error:
            return jsonify(retJson)

        cash=cashWithUser(username)

        if cash<money:
            return jsonify(generateReturnDictionary(303,"Not enough cash in your account"))

        debt=debtWithUser(username)

        updateAccount(username,cash-money)
        updateDebt(username,debt-money)
        retJson={
        "Transaction_Id":str(uuid.uuid4()),
        "message":"You've successfully paid your loan",
        "status":200
        }
        return jsonify(retJson)




api.add_resource(Register,"/register")
api.add_resource(Add,"/add")
api.add_resource(Transfer,"/transfer")
api.add_resource(Balance,"/balance")
api.add_resource(TakeLoan,"/takeloan")
api.add_resource(PayLoan,"/payloan")
if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
