from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from utils.decorators import HandleResponse, ValidateRequest, ValidateSignUp, Create, SignUpAccess, VerifyRole, VerifyToken
from utils.functions.token import generate_token
from database.index import get_by_val
from utils.functions.controllers import GetByModel
from utils.functions.info import can_sign_up
from flask import Flask, request, jsonify
from utils.decorators import HandleResponse


app = Flask(__name__)

@app.route('/')

def home():
    return "Home"


@app.route("/info", methods=["GET"])

@HandleResponse
def info():
    return can_sign_up(), 200

@app.route('/sign-up', methods=['POST'])
@HandleResponse
@SignUpAccess
@ValidateRequest
@ValidateSignUp
@Create("profile")
def sign_up():
    id = GetByModel("profile").id
    return generate_token({"profileId": id}), 200

@app.route('/subjects', methods=['POST'])
@HandleResponse
@ValidateRequest
@VerifyToken
@VerifyRole("admin")
@Create("subject")
def create_subject():
    return GetByModel("subject")
    

@app.route('/profiles', methods=['GET'])
@HandleResponse
@ValidateRequest
@VerifyToken
@VerifyRole("admin")



if __name__ == '__main__':
    app.run(debug=True)
