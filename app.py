from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

task_details = {}

task_id=1

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
        task_details[task_id] = {"title":task_title,"description":description,"time":time}
        task_id +=1
    return redirect(url_for('home'))

@app.route("/task/<int:task_id>")
def task_detail(task_id):
    task = task_details.get(task_id)
    if not task:
        return "Task not Found", 404
    return render_template("details.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
