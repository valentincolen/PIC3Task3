import ConfigParser
import sys

from flask import Flask, jsonify, make_response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_declarative import User, Keg, Base

app = Flask(__name__)


# Function to check if there is a file with given name and create new template or read given file.
def check_cfg(file_name):
    import os.path
    config = crear_plantilla()
    if os.path.isfile(file_name):
        read_cfg(file_name, config)
    else:
        write_config(config, file_name)
        print('Config file {} not found. Update the new template: '.format(file_name))
        sys.exit()
    return config


def get_value(config, section, option):
    return config.get(section, option)


# Function that give information about which field you have to fill
def read_cfg(file_name, config):
    config.read(file_name)
    write_config(config, file_name)
    remaining = get_remaining(config)
    if len(remaining) != 0:
        for section, option in remaining:
            print('Fill option {} in section {}.Update file {}'.format(option, section, file_name))
        sys.exit()


# Check if in given configuration all values are filled, return a list with empty ones
def get_remaining(config):
    return [(k, k1) for k, v in config._sections.items() for k1, v1 in v.items() if v1 == '']


# Function that create a template to store configuration
def crear_plantilla():
    config = ConfigParser.RawConfigParser()
    config.add_section('WebService')
    config.set('WebService', 'Port', '')
    return config


# Function that write in a given file the given configuration
def write_config(config, file_name='template.cfg'):
    with open(file_name, 'wb') as configfile:
        config.write(configfile)


def connection():
    path_to_db = database
    engine = create_engine('sqlite:///' + path_to_db)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def save(table, info):
    session = connection()
    try:
        if table == User:
            new_user = User(username=info[0], fullname=info[1], email=info[2], password=info[3], nfc_id=info[4],
                            user_flow=info[5])
            session.add(new_user)
        elif table == Keg:
            new_keg = Keg(keg_id=info[0], keg_flow=info[1])
            session.add(new_keg)
        session.commit()
        return True
    except:
        return False


def get_data(table):
    session = connection()
    user = session.query(table).all()
    list_of_dict = []
    if table == User:
        list_of_dict = [{'username': row.username,
                         'fullname': row.fullname,
                         'email': row.email,
                         'password': row.password,
                         'nfc_id': row.nfc_id,
                         'user_flow': row.user_flow} for row in user]

    elif table == Keg:
        list_of_dict = [{'keg_id': row.keg_id,
                         'keg_flow': row.keg_flow} for row in user]
    return jsonify(list_of_dict)


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/show_users', methods=['GET'])
def get_users():
    return get_data(User)


@app.route('/show_users/<username>', methods=['GET'])
def get_user(username):
    session = connection()
    user = session.query(User).filter(User.username == username).all()
    dictionary = {}
    for row in user:
        dictionary = {'username': row.username,
                      'fullname': row.fullname,
                      'email': row.email,
                      'password': row.password,
                      'nfc_id': row.nfc_id,
                      'user_flow': row.user_flow}
    return jsonify(dictionary)


@app.route('/show_users/<username>/delete_update', methods=['PUT'])
def update_user(username):
    session = connection()
    user = session.query(User).filter(User.username == username).first()

    user.fullname = request.json['fullname']
    user.email = request.json['email']
    user.password = request.json['password']
    user.nfc_id = request.json['nfc_id']
    user.user_flow = request.json['user_flow']

    session.commit()
    return jsonify({'post': request.json}), 201


@app.route('/show_users/<username>/delete_update', methods=['DELETE'])
def delete_user(username):
    session = connection()
    session.query(User).filter(User.username == username).delete()
    session.commit()
    return jsonify({'post': request.json}), 201


@app.route('/insert_user', methods=['POST'])
def insert_user():
    session = connection()
    try:
        new_user = User(username=request.json['username'], fullname=request.json['fullname'],
                        email=request.json['email'], password=request.json['password'], nfc_id=request.json['nfc_id'],
                        user_flow=request.json['user_flow'])
        session.add(new_user)
        session.commit()
        return jsonify({'post': request.json}), 201
    except:
        return False


@app.route('/show_kegs', methods=['GET'])
def get_kegs():
    return get_data(Keg)


@app.route('/show_kegs/<keg_id>', methods=['GET'])
def get_keg(keg_id):
    session = connection()
    kegs = session.query(Keg).filter(Keg.keg_id == keg_id).all()
    dictionary = {}
    for row in kegs:
        dictionary = {'keg_id': row.keg_id,
                      'keg_flow': row.keg_flow}
    return jsonify(dictionary)


@app.route('/show_kegs/<keg_id>/delete_update', methods=['PUT'])
def update_keg(keg_id):
    session = connection()
    keg = session.query(Keg).filter(Keg.keg_id == keg_id).first()

    keg.keg_flow = request.json['keg_flow']
    session.commit()
    return jsonify({'post': request.json}), 201


@app.route('/show_kegs/<keg_id>/delete_update', methods=['DELETE'])
def delete_keg(keg_id):
    session = connection()
    session.query(Keg).filter(Keg.keg_id == keg_id).delete()
    session.commit()
    return jsonify({'post': request.json}), 200


@app.route('/insert_keg', methods=['POST'])
def insert_keg():
    session = connection()
    try:
        new_user = Keg(keg_id=request.json['keg_id'], keg_flow=request.json['keg_flow'])
        session.add(new_user)
        session.commit()
        return jsonify({'post': request.json}), 201
    except:
        return False


if __name__ == '__main__':
    configuration = check_cfg('ConfigWebService.cfg')
    if configuration:
        port = int(get_value(configuration, 'WebService', 'Port'))
        database = 'database_task3.db'
        app.run(debug=True, port=port)
