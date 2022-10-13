#creates an instance of the Flask class. 
# The first argument is the name of the application's module or package.
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

# This is the model for the database table that will be created by SQLAlchemy 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# This line defines a route for the application. The route is what Flask uses to match the URL to the view function, 
# which is the function that is called to handle requests to that URL. 
@app.route("/")
def home():
    #db.create_all()
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

# This route is for adding new items to the todo list
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

# This route is for toggling the complete variable
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

# This route is for deleting items from the todo list
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/about")
def about():
    return  "<p>About Page</p>"

if __name__ == "__main__":
    # show all todos
    db.create_all()
    
    #- Demo - Adding a todo
    # new_todo = Todo(title="This is a new todo", complete=False)
    # db.session.add(new_todo)
    # db.session.commit()

    # This line starts the development server with the run() method. 
    # The debug parameter is set to True, which will activate the debugger and reloader. 
    app.run(debug=True)


