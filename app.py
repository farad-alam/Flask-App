from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

def load_tasks():
    if not os.path.exists('tasks.json'):
        return {}
    
    with open('tasks.json', 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_task(task):
    with open("tasks.json", "w") as f:
        json.dump(task, f, indent=4)

task_details = load_tasks()
# print(task_details)

task_id = max(map(int, task_details.keys()), default=0) + 1 if task_details else 1

@app.route('/')
def home():
    return render_template('home.html', task_details=task_details)

@app.route('/add-task', methods=["POST"])
def add_task():
    global task_id
    task_title = request.form.get('title')
    description = request.form.get('description')
    time = request.form.get('time')

    if task_title and description and time:
        task_details[str(task_id)] = {"title":task_title,"description":description,"time":time}
        task_id +=1
        # print(task_details)
        save_task(task_details)

    return redirect(url_for('home'))

@app.route("/task/<int:task_id>")
def task_detail(task_id):
    task = task_details.get(str(task_id))
    # print(task_details)
    # print(task)
    if not task:
        return "Task not Found", 404
    return render_template("details.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
