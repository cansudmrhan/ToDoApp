import requests
from flask import Flask, render_template, request, url_for, redirect
from bson.objectid import ObjectId
import pymongo

app = Flask(__name__, template_folder='templates')

url="127.0.0.1:5001/ps_facade"

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
my_database = myclient['CANSU']
my_collection = my_database['TODO']


@app.route('/')
def index():
    saved_todos = my_collection.find()
    return render_template('index.html', todos=saved_todos)


@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    my_collection.insert_one({'text': new_todo, 'complete': False})
    # my_collection.insert({"todo": new_todo})
    return redirect(url_for('index'))


@app.route('/complete/<oid>')
def complete(oid):
    todo_item = my_collection.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = True
    my_collection.save(todo_item)
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    # requests.post(f"{url}/delete_data/cansu/admin", json=complete)
    my_collection.delete_many({'complete' : True})
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    # requests.post(f"{url}/delete_db/cansu/admcin", json= {})
    my_collection.delete_many({})
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()

