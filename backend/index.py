from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from utils.decorators import HandleResponse, ValidateRequest, ValidateSignUp, Create, SignUpAccess, VerifyRole, VerifyToken, GetBy, Exists
from utils.functions.token import generate_token
from database.index import get_by_val
from utils.functions.controllers import GetByModel, GetMySubjects, AttachStudents
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
@VerifyToken
@VerifyRole("admin")
@GetBy("profile", "role", "args")
def get_profiles():
    return GetByModel("profiles"), 200


@app.route("/profiles", methods=["POST"])
@HandleResponse
@ValidateRequest
@VerifyToken
@VerifyRole("admin")
@Create("profile")
def create_profile():
    return True, 201

@app.route('/subjects/me', methods=['GET'], endpoint="get_my_subject")
@HandleResponse
@VerifyToken
def get_my_subjects():
    return GetMySubjects()

@app.route("/subjects", methods=["POST"])
@HandleResponse
@ValidateRequest
@VerifyToken
@VerifyRole("admin")
@Create("subject")
def create_subject():
    return True, 201

@app.route("/subject/<int:subject_id>/students", methods=["POST"])
@HandleResponse
@ValidateRequest
@VerifyToken
@VerifyRole("admin")
@Exists("subject")
def attach_students(subject_id): 
    return AttachStudents(subject_id)

if __name__ == '__main__':
    app.run(debug=True)
