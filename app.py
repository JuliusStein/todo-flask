#creates an instance of the Flask class. 
# The first argument is the name of the application's module or package.
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


@app.route("/about")
def about():
    return  "<p>About Page</p>"

if __name__ == "__main__":
    # show all todos
    db.create_all()
    
    #- Demo - Adding a todo
    new_todo = Todo(text="This is a new todo", complete=False)
    db.session.add(new_todo)
    db.session.commit()

    # This line starts the development server with the run() method. 
    # The debug parameter is set to True, which will activate the debugger and reloader. 
    app.run(debug=True)


