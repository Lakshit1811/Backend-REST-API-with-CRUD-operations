from flask import Flask
from flask_pymongo import PyMongo

app = Flask(_name_)
app.config["MONGO_URI"] = "mongodb://localhost:27017/todo_db"
mongo = PyMongo(app)
@app.route("/tasks", methods=["GET", "POST"])
def task():
    if request.method == "POST":
        task = request.json["task"]
        is_completed = request.json["is_completed"]
        end_date = request.json["end_date"]
        mongo.db.tasks.insert_one({"task": task, "is_completed": is_completed, "end_date": end_date})
        return "Task added successfully!"
    else:
        tasks = mongo.db.tasks.find()
        return jsonify([task for task in tasks])

@app.route("/tasks/<id>", methods=["GET", "PUT", "DELETE"])
def task_by_id(id):
    task = mongo.db.tasks.find_one({"_id": ObjectId(id)})
    if request.method == "GET":
        return jsonify(task)
    if request.method == "PUT":
        task = request.json["task"]
        is_completed = request.json["is_completed"]
        end_date = request.json["end_date"]
        mongo.db.tasks.update_one({"_id": ObjectId(id)}, {"$set": {"task": task, "is_completed": is_completed, "end_date": end_date}})
        return "Task updated successfully!"
    if request.method == "DELETE":
        mongo.db.tasks.delete_one({"_id": ObjectId(id)})
        return "Task deleted successfully!"
        @app.route("/tasks/<page_num>")
def task_by_page(page_num):
    tasks = mongo.db.tasks.find().skip((int(page_num) - 1) * 10).limit(10)
    return jsonify([task for task in tasks])
    @app.route("/tasks/csv")
def export_tasks_csv():
    tasks = mongo.db.tasks.find()
    csv = "task,is_completed,end_date\n"
    for task in tasks:
        csv += f"{task['task']},{task['is_completed']},{task['end_date']}\n"
    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=tasks.csv"
    response.m