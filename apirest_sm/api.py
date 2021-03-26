from states import *
import jwt
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import requests
import json
from subprocess import *
#### Build DataBase ########
'''
python
from movies import db
db.create_all()
'''
@app.route('/apicall',methods=['GET'])
def apicall():

    url = "http://127.0.0.1:1235/userlogin"

    payload="{\n    \"username\": \"test2\",\"password\": \"test2\"\n}"
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


    url = "http://127.0.0.1:1234/state"
    header = {}
    # Pass from dictionary to a json object.
    header['Authorization'] = 'Bearer  '+ response.json()['access_token']
    json.dumps(header)
    print(header)
    resp = requests.request("GET", url, headers=header, data=payload)

    return resp.text

@app.route('/userregistration', methods=['POST'])

def UserRegistration():

    request_data = request.get_json()  # getting data from client
    
    if UserModel.find_by_username(request_data['username']):
        return {'message': 'User {} already exists'.format(request_data['username'])}
    
    new_user = UserModel(
        username = request_data['username'],
        password = UserModel.generate_hash(request_data['password'])
    )
    
    try:
        new_user.save_to_db()
        return {
            'message': 'User {} was created'.format(request_data['username']),
            }
    except:
        return {'message': 'Something went wrong'}, 500

@app.route('/userlogin', methods=['POST'])

def userlogin():
    request_data = request.get_json()  # getting data from client
    current_user = UserModel.find_by_username(request_data['username'])
    print(request_data['username'])
    if not current_user:
        return {'message': 'User {} doesn\'t exist'.format(data['username'])}
    
    if UserModel.verify_hash(request_data['password'], current_user.password):
        access_token = create_access_token(identity = request_data['username'])
        refresh_token = create_refresh_token(identity = request_data['username'])
        return {
            'id': current_user.username,
            'access_token': access_token,
            'refresh_token': refresh_token
            }
    else:
        return {'message': 'Wrong credentials'}

# route to get all devices
@app.route('/devices', methods=['GET'])
@jwt_required
def get_device():
    '''Function to get all the devices in the database'''
    return jsonify({'Devices': Device.get_devices()})


# route to get device by id
@app.route('/devices/<int:id>', methods=['GET'])
@jwt_required
def get_device_by_id(id):
    return_value = Devices.get_device(id)
    return jsonify(return_value)


# route to add new device
@app.route('/devices', methods=['POST'])
@jwt_required
def add_device():
    '''Function to add new device to the database'''
    request_data = request.get_json()  # getting data from client
    Device.add_device(request_data["name"])
    response = Response("Device added", 201, mimetype='application/json')
    return response


# route to update device with PUT method
@app.route('/devices/<int:id>', methods=['PUT'])
@jwt_required
def update_device(id):
    '''Function to edit movie in our database using movie id'''
    request_data = request.get_json()
    Device.update_device(id, request_data['name'])
    response = Response("Device Updated", status=200, mimetype='application/json')
    return response


# route to delete device using the DELETE method
@app.route('/devices/<int:id>', methods=['DELETE'])
@jwt_required
def remove_movie(id):
    '''Function to delete movie from our database'''
    Devices.delete_devices(id)
    response = Response("Device Deleted", status=200, mimetype='application/json')
    return response





##########################################################################################

# route to get all parameter
@app.route('/parameter', methods=['GET'])

def get_parameter():
    '''Function to get all the Parameter in the database'''
    return jsonify({'Parameter': Parameter.get_all_parameter()})


# route to get parameter by id
@app.route('/parameter/<int:id>', methods=['GET'])
@jwt_required
def get_parameter_by_id(id):
    return_value = Parameter.get_movie(id)
    return jsonify(return_value)


# route to add new parameter
@app.route('/parameter', methods=['POST'])
@jwt_required
def add_parameter():
    '''Function to add new parameter to our database'''
    request_data = request.get_json()  # getting data from client
    Parameter.add_parameter(request_data["name"], request_data["unit"])
    response = Response("Parameter added", 201, mimetype='application/json')
    return response


# route to update parameter with PUT method
@app.route('/parameter/<int:id>', methods=['PUT'])
@jwt_required
def update_parameter(id):
    '''Function to edit parameter in our database using parameter id'''
    request_data = request.get_json()
    Parameter.update_parameter(id, request_data['name'], request_data['unit'])
    response = Response("Parameter Updated", status=200, mimetype='application/json')
    return response


# route to delete parameter using the DELETE method
@app.route('/parameter/<int:id>', methods=['DELETE'])
@jwt_required
def remove_parameter(id):
    '''Function to delete movie from our database'''
    Movie.delete_parameter(id)
    response = Response("Parameter Deleted", status=200, mimetype='application/json')
    return response
#########################################################


# route to get all srates
@app.route('/state', methods=['GET'])
@jwt_required
def get_state():
    '''Function to get all the Parameter in the database'''
    return_value = State.get_state2()
    return jsonify(return_value)


# route to get state by id
@app.route('/state/<int:id>', methods=['GET'])
@jwt_required
def get_state_by_id(id):
    return_value = State.get_state_by_id(id)
    return jsonify(return_value)

@app.route('/state/<int:id>', methods=['GET'])
@jwt_required
def get_state_by_datetime(date):
    return_value = State.get_state_by_datetime(id)
    return jsonify(return_value)

# route to add new state
@app.route('/state', methods=['POST'])
@jwt_required
def add_state():
    '''Function to add new parameter to our database'''
    request_data = request.get_json()  # getting data from client
    State.add_state(request_data["value"], request_data["state"],request_data["state_n"], request_data["parameter_id"], request_data["device_id"])
    response = Response("state added", 201, mimetype='application/json')
    return response


# route to update state with PUT method
@app.route('/state/<int:id>', methods=['PUT'])
@jwt_required
def update_state(id):
    '''Function to edit parameter in our database using parameter id'''
    request_data = request.get_json()
    State.update_state(id, request_data['value'], request_data['state_1'], request_data['state_n'])
    response = Response("Parameter Updated", status=200, mimetype='application/json')
    return response


# route to delete state using the DELETE method
@app.route('/state/<int:id>', methods=['DELETE'])
@jwt_required
def remove_state(id):
    '''Function to delete movie from our database'''
    Movie.delete_state(id)
    response = Response("State Deleted", status=200, mimetype='application/json')
    return response



def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output


def get_ip():
    result = run_cmd( 'ip addr' )
    print(type(result))
    
    lines = result.decode().split('\n')
    skip = True
    ip = ''
    for line in lines:
        if 'BROADCAST' in line:
            skip = False
        if skip:
            continue
        if 'inet' in line:
            a, address, b, mask, c, d, interface = line.split()[:7]
            ip, net = address.split('/')
            break
    return ip



if __name__ == "__main__":

    ip = get_ip()
    if not len( ip ):
        exit ()


    app.run(host= ip,port=1234, debug=True)
