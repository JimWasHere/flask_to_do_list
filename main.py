from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import os
from datetime import date

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    timestamp = db.Column(db.String(100))


db.create_all()


@app.get('/')
def home():
    to_do_list = db.session.query(ToDo).all()
    return render_template('index.html', to_do_list=to_do_list)


@app.post('/add')
def add():
    title = request.form.get('title')
    time = date.today().strftime("%B %d, %Y")
    new_todo = ToDo(title=title, timestamp=time, complete=False)

    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))


@app.get("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(ToDo).filter(ToDo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))


@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(ToDo).filter(ToDo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
