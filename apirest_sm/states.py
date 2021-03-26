from settings import *
import json
import time
import datetime
from passlib.hash import pbkdf2_sha256 as sha256
# Initializing our database
db = SQLAlchemy(app)


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    
    def find_by_username(_username):
        return UserModel.query.filter_by(username = _username).first()
        
    def return_all():
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    
    def delete_all():
        try:
            num_rows_deleted = db.session.query().delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    def generate_hash(password):
        return sha256.hash(password)
    
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

# the class Movie will inherit the db.Model of SQLAlchemy

class Parameter(db.Model):
    __tablename__ = 'parameter'  # creating a table name
    parameter_id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    parameter_name = db.Column(db.String(80), unique = True, nullable=False)
    # nullable is false so the column can't be empty
    unit = db.Column(db.String(80), nullable=False)
    def json(self):
        return {'id': self.parameter_id, 'name': self.parameter_name,
                'unit': self.unit}
        # this method we are defining will convert our output to json

    def add_parameter( _name,_unit):
        '''function to add movie to database using _title, _year, _genre
        as parameters'''
        # creating an instance of our Movie constructor
        new_parameter = Parameter(parameter_name=_name, unit=_unit)
        db.session.add(new_parameter)  # add new movie to database session
        db.session.commit()  # commit changes to session

    def get_all_parameter():
        '''function to get all movies in our database'''
        return [Parameter.json(parameter) for parameter in Parameter.query.all()]

    def get_parameter(_id):
        '''function to get movie using the id of the movie as parameter'''
        return [Parameter.json(Parameter.query.filter_by(parameter_id=_id).first())]
        # coverts our output to json
        # the filter_by method filters the query by the id
        # the .first() method displays the first value

    def update_parameter(_id, _name,_unit):
        '''function to update the details of a movie using the id, title,
        year and genre as parameters'''
        parameter_to_update = Parameter.query.filter_by(parameter_id=_id).first()
        parameter_to_update.parameter_name = _name
        parameter_to_update.unit = _unit
        db.session.commit()

    def delete_parameter(_id):
        '''function to delete a movie from our database using
           the id of the movie as a parameter'''
        Parameter.query.filter_by(parameter_id=_id).delete()
        # filter by id and delete
        db.session.commit()  # commiting the new change to our database

class State(db.Model):
    __tablename__ = 'states'  # creating a table name
    state_id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    value = db.Column(db.Integer, nullable=False)
   
    time=db.Column(db.String(80), nullable=False)
    state_1 = db.Column(db.String(80), nullable=False)
    state_n = db.Column(db.String(80), nullable=False)
    
    #foreign keys
    parameter_id = db.Column(db.Integer,db.ForeignKey("parameter.parameter_id"))
    parameters = db.relationship("Parameter")

    device_id = db.Column(db.Integer, db.ForeignKey("device.device_id"))
    devices = db.relationship("Device")
    
    def json(self):
        print('##############')
        return {'id': self.state_id, 'value': self.value,'date': self.time, 'state_id': self.state_1,'state_n': self.state_n, 'parameter': self.parameter_id, 'device': self.device_id}
        # this method we are defining will convert our output to json


    def json2():
       
        
        new_data = []
        
        not_found = True
        for item in State.query.all():
            print('##############')
            for Device in new_data:
                print('##############')
                not_found = True
                if item.device_id == Device['Dispositivo']:
                    not_found = False
                    Device['Parametros'].append({'nombre':item.parameter_id, 'valor':item.value, 'estado_1':item.state_1, 'estado_n':item.state_n})
                    break
                
            if not_found:
                print('-------Not Found----------')
                new_data.append({'Dispositivo':item.device_id, 'Parametros':[{'nombre':item.parameter_id, 'valor':item.value, 'estado_1':item.state_1, 'estado_n':item.state_n}]})
    
        print('----------Sale FOr-----')
        '''
        for sel in State.query.all():
             new_data.append({'id': sel.state_id, 'value': sel.value,'date': sel.time, 'state_id': sel.state_1,'state_n': sel.state_n, 'parameter': sel.parameter_id, 'device': sel.device_id})
        '''
        return  new_data




        
        # this method we are defining will convert our output to json

    def add_state( _value,_state,_state_n,_parameter_id,_device_id):
        '''function to add movie to database using _title, _year, _genre
        as parameters'''
        # creating an instance of our constructor
        new_state = State( value=_value,time=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-0400") ,state_1=_state, state_n=_state_n,parameter_id=_parameter_id,device_id=_device_id)
        db.session.add(new_state)  # add new to database session
        db.session.commit()  # commit changes to session

    def get_state():
        '''function to get all movies in our database'''
        return [State.json(state) for state in State.query.all()]
    def get_state2():
        '''function to get all movies in our database'''
        return [State.json2()]
    def get_state_by_id(_id):
        '''function to get movie using the id of the movie as parameter'''
        return [State.json(State.query.filter_by(state_id=_id).first())]
        

    def update_state(_id,_value, _state_1, _state_n):
        '''function to update the details of a movie using the id, title,
        year and genre as parameters'''
        state_to_update = Movie.query.filter_by(state_id=_id).first()
        state_to_update.value = _value
        state_to_update.state_1 = _year
        state_to_update.state_n = _state_n
        db.session.commit()

    def delete_state(_id):
        '''function to delete a movie from our database using
           the id of the movie as a parameter'''
        State.query.filter_by(state_id=_id).delete()
        # filter by id and delete
        db.session.commit()  # commiting the new change to our database

# the class will inherit the db.Model of SQLAlchemy
class Device(db.Model):
    __tablename__ = 'device'  # creating a table name
    device_id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    device_name= db.Column(db.String(80), unique = True, nullable=False)
    # nullable is false so the column can't be empty
    
    def json(self):
        return {'id': self.device_id, 'name': self.device_name}
        # this method we are defining will convert our output to json
    
    def add_device(_name):
        '''function to add movie to database using _title, _year, _genre
        as parameters''' 
        # creating an instance of ourconstructor
        new_device=Device(device_name=_name)
        db.session.add(new_device)  # add new device
        db.session.commit()  # commit changes to session

    def get_devices():
        '''function to get all movies in our database'''
        return [Device.json(device) for device in Device.query.all()]

    def get_device_by_id(_id):
        '''function to get movie using the id of the movie as parameter'''
        return [Device.json(Device.query.filter_by(device_id=_id).first())]
        # Movie.json() coverts our output to json
        # the filter_by method filters the query by the id
        # the .first() method displays the first value

    def update_device(_id, _name):
        '''function to update the details of a movie using the id, title,
        year and genre as parameters'''
        device_to_update = Movie.query.filter_by(device_id=_id).first()
        device_to_update.device_name = _name
        
        db.session.commit()

    def delete_device(_id):
        '''function to delete a movie from our database using
           the id of the movie as a parameter'''
        Device.query.filter_by(device_id=_id).delete()
        # filter by id and delete
        db.session.commit()  # commiting the new change to our database