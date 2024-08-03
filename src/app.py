from flask import Flask
from flask_jwt_extended import JWTManager
from upload import upload_bp
from user import user_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
jwt = JWTManager(app)

app.register_blueprint(upload_bp)
app.register_blueprint(user_bp)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def main():
    app.run(host="0.0.0.0", port=5000)
    
if __name__ == '__main__':
    main()