import os
from flask import Flask, render_template, request
from google.cloud import datastore
from markupsafe import escape

app = Flask(__name__)


datastore_client = datastore.Client()

@app.route('/')
def root():
    return render_template('index.html', context=NotImplemented)

@app.route('/upload')
def upload():
    try:
        name = escape(request.args['name'])
    except:
        name = ""

    try:
        address = escape(request.args['address'])
    except:
        address = ""
    
    try:
        city = escape(request.args['city'])
    except:
        city = ""

    try:
        state = escape(request.args['state'])
    except:
        state = ""

    try:
        zip_c = escape(request.args['zip'])
    except:
        zip_c = ""

    if name == "" and address == "" and city == "" and state == "" and zip_c == "":
        root()
        
    kind = 'Contacts'
    uqID = hash(name + address + city + state + zip_c)
    contact_key = datastore_client.key(kind, uqID)
    contact = datastore.Entity(key=contact_key)

    contact['name'] = name
    contact['address'] = address
    contact['city'] = city
    contact['state'] = state
    contact['zip'] = zip_c

    datastore_client.put(contact)

    attributes = [name, address, city, state, zip_c]

    return render_template('upload.html', contact=attributes)

@app.route('/view/<user>')
def view(user):
    query = datastore_client.query(kind='Contacts')

    contact_list = query.fetch()

    return render_template('view.html', contacts=contact_list)

if __name__ == '__main__':
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

    