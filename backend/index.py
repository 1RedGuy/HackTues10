from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, jsonify
from utils.decorators import HandleResponse


app = Flask(__name__)

@app.route('/')

def home():
    return "Home"

@app.route('/sign-up', methods=['POST'])

@HandleResponse
def sign_up():
    return 

if __name__ == '__main__':
    app.run(debug=True)
