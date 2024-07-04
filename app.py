from flask import Flask, render_template, request, redirect, url_for
import json, os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    date_created =  db.Column(db.DateTime, default=datetime.now)


@app.route('/')
def home():
    tasks = Task.query.order_by(Task.date_created).all()
    return render_template('home.html', tasks=tasks)

@app.route('/add-task', methods=["POST"])
def add_task():
    global task_id
    task_title = request.form.get('title')
    description = request.form.get('description')
    time = request.form.get('time')

    if task_title and description and time:
        task = Task(title=task_title, description=description, time=time)
        db.session.add(task)
        db.session.commit()

    return redirect(url_for('home'))

@app.route("/task/<int:task_id>")
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template("details.html", task=task)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
