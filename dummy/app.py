import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')  
jwt = JWTManager(app)

@app.route('/dummyservice', methods=['POST'])
@jwt_required()
def dummy_service():
    current_user = get_jwt_identity()
    
    print("dummy_function")
    x1 = request.json.get("x1")
    x2 = request.json.get("x2")
    y = x1**2 + x2*0.5

    return jsonify(msg=f"Hello, {current_user}. This is a dummy service response.", y=y), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
