from flask import Flask, render_template
from flask import request, redirect
import pickle
import os
import re

app = Flask(__name__)
filename = 'todo.py'


if (int(os.stat(filename).st_size) == 0):
    todo_items = []
else:
    filehandler = open(filename,'rb')
    todo_items= pickle.load(filehandler)
    filehandler.close()


@app.route('/')
def hello_world():
    return render_template('index.html', todo_items=todo_items)



@app.route('/submit',  methods=['POST'])
def submit():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    if priority not in ['high', 'medium', 'low']:
        return redirect('/')

    if not re.match('(\w+[.|\w])*@(\w+[.])*\w+',email):
        return redirect('/')

    if len(task.strip()) < 1:
        return redirect('/')

    task = { "task": task, "email":email, "priority": priority}
    todo_items.append(task)
    return redirect('/')


@app.route('/clear',  methods=['POST'])
def clear():
    todo_items.clear()
    return redirect('/')


@app.route('/remove',  methods=['POST'])
def remove():
    item_id = request.form['item_id']
    item_id = int(item_id)
    del todo_items[item_id]
    return redirect('/')


@app.route('/save')
def save():
    filehandler = open(filename,"wb")
    pickle.dump(todo_items,filehandler)
    filehandler.close()
    return redirect('/')


if __name__ == '__main__':
    app.run()
