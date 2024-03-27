from waitress import serve
from index import app
print("Server running")
serve(app, host='0.0.0.0', port=8080)