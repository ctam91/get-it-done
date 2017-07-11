from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done' #connecting string
app.config['SQLALCHEMY_ECHO'] = True #echo SQL commands generated by SQL Alchemy
db = SQLAlchemy(app) #create db object. Our app will have properties as established by SQLAlchemy class. 

class Task(db.Model): 
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    #store tasks. create persistent class to represent tasks to put data in db. Persistent classes are classes that are stored in databases. Each one needs an unique id (primary key). A name variable is also created to represent the name of the task. 'Completed" is also create to represent if a task is completed or not. 
    def __init__(self, name):
        self.name = name
        self.completed = False

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password 

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()
    
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html', title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)

@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()