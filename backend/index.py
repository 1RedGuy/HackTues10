from dotenv import load_dotenv
load_dotenv()


from flask import Flask, request
from utils.decorators import HandleResponse, ValidateRequest, ValidateSignUp, Create, SignUpAccess, VerifyRole, VerifyToken, GetBy, Exists, VerifyPassword, GeneratePassword, ValidateBodyRoles
from utils.functions.token import generate_token
from utils.functions.controllers import GetByModel, GetMySubjects, AttachStudents
from utils.functions.info import can_sign_up
from utils.decorators import HandleResponse
from mail.index import Email_Service
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/info", methods=["GET"], endpoint="info")
@HandleResponse
def info():
    return can_sign_up(), 200


@app.route('/sign-up', methods=['POST'], endpoint="sign_up")
@HandleResponse
@SignUpAccess
@ValidateRequest
@ValidateSignUp
@Create("profile")
def sign_up():
    id = GetByModel("profile")["id"]
    return generate_token({"profileId": id}), 200    

@app.route("/sign-in", methods=["POST"], endpoint="sign_in")
@HandleResponse
@ValidateRequest
@GetBy("profile", "email", "body", listed=False)
@VerifyPassword
def sign_in():
    return generate_token({"profileId": request.environ.get("profile")["id"]}), 200

@app.route('/profiles', methods=['GET'], endpoint="get_profiles")
@HandleResponse
@VerifyToken
@VerifyRole("admin")
@GetBy("profile", "role", "args", False)
def get_profiles():
    return GetByModel("profiles"), 200


@app.route("/profiles", methods=["POST"], endpoint = "create_profile")
@HandleResponse
@ValidateRequest
@VerifyToken
@VerifyRole("admin")
@GeneratePassword
@Create("profile")
def create_profile():
    return True, 201

@app.route('/subjects/me', methods=['GET'], endpoint="get_my_subject")
@HandleResponse
@VerifyToken
def get_my_subjects():
    return GetMySubjects()

@app.route("/subjects", methods=["POST"], endpoint = "create_subject")
@HandleResponse
@ValidateRequest
@VerifyToken
@VerifyRole("admin")
@Create("subject")
def create_subject():
    return True, 201

@app.route("/subject/<int:subject_id>/students", methods=["POST"], endpoint = "attach_students")
@HandleResponse
@ValidateRequest
@VerifyToken
@VerifyRole("admin")
@Exists("subject")
@ValidateBodyRoles("student")
def attach_students(subject_id): 
    return AttachStudents(subject_id)

@app.route("/email", methods=["GET"], endpoint="verify_email")
def verify_email():
    a = Email_Service()
    a.send_email("demirev2@hotmail.com", "<h1>Test</h1>", "HackTues10")
    return "okay", 200

@app.route("/profiles/me", methods=['GET'], endpoint="show_profile")
@HandleResponse
@VerifyToken
def show_profile():
    return GetByModel("ri_profile")

@app.route('/subjects/<int:subject_id>/posts', methods=['GET'], endpoint="show_posts")
@HandleResponse
@VerifyToken
@Exists("subject")
@GetBy("posts", "subject_id", "path", assertive=False)
def show_posts():
    return GetByModel("posts")

@app.route('/subject/<int:subject_id>/posts', methods=['POST'], endpoint="create_post")
@HandleResponse
@ValidateRequest
@VerifyToken
@VerifyRole("teacher")
@Create("posts")
def create_post():
    return


if __name__ == '__main__':
    app.run(debug=True)

