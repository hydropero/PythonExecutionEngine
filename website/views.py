from flask import Blueprint, render_template, request, flash, jsonify, url_for, session, redirect
# Blueprint allows you to break out your views into separate files instead of just one
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import os
import ast
import sys
import subprocess

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    metadata = db.MetaData()
    metadata.reflect(db.engine)
    alltables = metadata.tables
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user, tables=alltables)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    #loads request data into dictionary object
    note = json.loads(request.data)
    noteId = note['noteId']
    # uses SQLAlchemy to find note associated with the provided noteId
    note = Note.query.get(noteId)
    # check if note exists
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})


@views.route('/execute-code', methods=['GET', 'POST'])
def execute_code():
    if request.method == 'POST':
        f = open("codeblock.py", "w")
        f.write(request.form['code-block'])
        f.close()
        # loc, glob = {}, {}
        # exec(userPythonCode, glob, loc)
        # if bool(loc):
        #     executedCode = loc
        # else:
        #     executedCode = glob

        process = subprocess.call(['python', 'codeblock.py'])
        process = subprocess.Popen(['python', 'codeblock.py'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout, stderr)

        executedCode = stdout

        return redirect(url_for('views.rendered_response', executedCode=executedCode))
    else:
        print('no')
        return render_template("execute_code.html", user=current_user)


@views.route('/rendered-response', methods=['GET', 'POST'])
def rendered_response():
    executedCode = request.args['executedCode']
    return render_template("rendered_response.html", resultOfExecution=executedCode, user=current_user)





