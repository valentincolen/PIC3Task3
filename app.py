import argparse

import requests
from flask import render_template, make_response, jsonify
from flask import request, Flask

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Receive the arguments for the program')
parser.add_argument('-ws', '--wslink', type=str, default='http://127.0.0.1:5001',
                    help='Link where is hosted the server')


@app.route('/')
def functionalities():
    return render_template('functionalities.html')


@app.route('/show_users', methods=['GET'])
def hist_users():
    print web_server_link
    to_json = requests.get(web_server_link + "/show_users")
    historical_users = []
    for dictionary in to_json.json():
        historical_users = historical_users + [(dictionary['username'], dictionary['fullname'], dictionary['email'],
                                                dictionary['password'], dictionary['nfc_id'], dictionary['user_flow'])]
    return render_template('show_users_table.html', historical_users=historical_users)


@app.route('/show_users/<username>', methods=['GET'])
def update_user(username):
    if request.method == 'GET':
        response = requests.get(web_server_link + "/show_users/" + username)
        a = response.json()
        user = [(a['username'], a['fullname'], a['email'], a['password'], a['nfc_id'], a['user_flow'])]
        return render_template('update_delete_user_form.html', user=user)


@app.route('/show_users/<username>/delete_update', methods=['GET', 'POST'])
def delete_user(username):
    if request.method == 'GET':
        requests.delete(web_server_link + "/show_users/" + username + "/delete_update")
    elif request.method == 'POST':
        info = get_user_form()
        requests.put(web_server_link + "/show_users/" + username + "/delete_update", json=info)
    return render_template('functionalities.html')


def check_user_available(info, additional_url, identification):
    response = requests.get(web_server_link + additional_url + info[identification])
    a = response.json()
    if info[identification] == '':
        return [False, {'error': identification + " not allowed"}]
    elif a != {}:
        return [False, {'error': identification + " already exist"}]
    else:
        return [True]


@app.route('/insert_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        return render_template('new_user_form.html')
    elif request.method == 'POST':
        info = get_user_form()
        is_ok = check_user_available(info, "/show_users/", 'username')
        if is_ok[0]:
            requests.post(web_server_link + "/insert_user", json=info)
            return render_template('functionalities.html')
        else:
            return make_response(jsonify(is_ok[1]), 400)


def get_user_form():
    username = request.form.get('user')
    fullname = request.form.get('fullname')
    email = request.form.get('mail')
    password = request.form.get('password')
    nfc_id = request.form.get('nfc_id')
    user_flow = request.form.get('user_flow')
    return {'username': username,
            'fullname': fullname,
            'email': email,
            'password': password,
            'nfc_id': nfc_id,
            'user_flow': user_flow}


@app.route('/show_kegs', methods=['GET', 'POST'])
def hist_kegs():
    to_json = requests.get(web_server_link + "/show_kegs")
    historical_kegs = []
    for dictionary in to_json.json():
        historical_kegs = historical_kegs + [(dictionary['keg_id'], dictionary['keg_flow'])]
    return render_template('show_kegs_table.html', historical_kegs=historical_kegs)


@app.route('/show_kegs/<keg_id>', methods=['GET'])
def update_keg(keg_id):
    if request.method == 'GET':
        response = requests.get(web_server_link + "/show_kegs/" + keg_id)
        a = response.json()
        keg = [(a['keg_id'], a['keg_flow'])]
        return render_template('update_delete_keg_form.html', keg=keg)

    print request.method


@app.route('/show_kegs/<keg_id>/delete_update', methods=['GET', 'POST'])
def delete_keg(keg_id):
    if request.method == 'GET':
        requests.delete(web_server_link + "/show_kegs/" + keg_id + "/delete_update")
    elif request.method == 'POST':
        info = get_keg_form()
        requests.put(web_server_link + "/show_kegs/" + keg_id + "/delete_update", json=info)
    return render_template('functionalities.html')


@app.route('/insert_keg', methods=['GET', 'POST'])
def new_keg():
    if request.method == 'GET':
        return render_template('new_keg_form.html')
    elif request.method == 'POST':
        info = get_keg_form()
        is_ok = check_user_available(info, "/show_kegs/", 'keg_id')
        if is_ok[0]:
            requests.post(web_server_link + "/insert_keg", json=info)
            return render_template('functionalities.html')
        else:
            return make_response(jsonify(is_ok[1]), 400)


def get_keg_form():
    keg_id = request.form.get('keg_id')
    keg_flow = request.form.get('keg_flow')
    return {'keg_id': keg_id,
            'keg_flow': keg_flow}


if __name__ == '__main__':
    args = parser.parse_args()
    web_server_link = args.wslink
    app.debug = False
    app.run(debug=True)
